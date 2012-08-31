#!/usr/bin/python
"""
The main logger application
"""

import sys
import time
import signal

import urllib2
import os
import sqlite3

import eko.Util.LogHelper as LogHelper
import eko.Util.DBSetup as DBSetup

from eko.Sensors.Dispatcher import EkoDispatcher

import eko.SystemInterface.OSTools as OSTools

import eko.WebService.Uploader as Uploader
import eko.WebService.ClientMessages as CMsgs
import eko.WebService.ServerMessages as SMsgs

import logging

import subprocess

from datetime import datetime, timedelta

VERSION = '1.2'

class DataLogger(object):
    logger = logging.getLogger('eko.DataLogger')
    
    def __init__(self, ctx):
        self.context = ctx
    
    def _try_network(self):
        google_req = urllib2.Request('http://v2.ekohub.org/')
        try:
            self.logger.debug("Pinging ekohub.org")
            return urllib2.urlopen(google_req, timeout=30)
        except urllib2.URLError:
            self.logger.exception("URL Error, unable to reach ekohub.org")
            return False
      
    def datalog(self):
        # instantiate a harvest dispatcher
        dispatch = EkoDispatcher(self.context)
        dispatch.import_configs()
        self.logger.info("Start polling sensors")
        dispatch.dispatch_all()
        self.logger.info("Finish polling sensors")
        return
    
    def upload_kiosk_messages(self):
        try:
            CMsgs.transmit_clientmessages(self.context)
            # FIXME
        except:
            self.logger.exception("Unable to transmit client messages to server.")
            return False
        return True
    
    def _download_server_messages(self):
        messages = SMsgs.get_messages(self.context)
        return messages
    
    def service_server_messages(self, ignore_sa=False):
        msgs = self._download_server_messages()
        if not msgs:
            return False
            
        for msg in msgs:
            self.logger.debug("Message %s." % str(msg))
            if 'msg_type' not in msg.keys():
                self.logger.warning("No message type specified.")
                continue
            if 'msg' not in msg.keys():
                self.logger.warning("No message specified.")
                continue
            if msg['msg_type'] == 'STAYALIVE':
                if not ignore_sa:
                    self.stay_alive_routine(msg['msg'])
            elif msg['msg_type'] == 'CMD':
                self._exec_process(msg['msg'])
            elif msg['msg_type'] == 'GIVELOGS':
                res = self.upload_logs()
                CMsgs.add_clientmessage(self.context, "Logs delivered.", res, "Command parser", datetime.utcnow())
            else:
                self.logger.warning("Unrecogised command.")
        return
        
    def _exec_process(self,message):
        self.logger.info("Executing message from server.")
        self.logger.debug("Command is %s." % message)
        try:
            proc = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            self.logger.exception("Subprocess could not be opened.")
            return False
        now = datetime.utcnow()
        start = datetime.utcnow() + timedelta(seconds=240)
        while now < start:
            now = datetime.now()
            if proc.poll() is not None:
                timeout = 0
                break;
            timeout = 1
        if timeout:
            self.logger.error("Process timed out.")
            return False
        ret_tuple = proc.communicate()
        self.logger.debug("Command returns: %s." % str(ret_tuple))
        CMsgs.add_clientmessage(self.context, "Command Executed:\n%s" % str(ret_tuple), '', "Command Executer", datetime.utcnow())
        return
    
    def stay_alive_routine(self,message_text):
        self.logger.info("Stay Alive for 30 minutes.")
        now = datetime.utcnow()
        stop = now + timedelta(seconds=1800)
        CMsgs.add_clientmessage(self.context, "Staying Alive.", '', "Command parser", datetime.utcnow())
        while now < stop:
            now = datetime.utcnow()
            time.sleep(20)
            try:
                self.upload_kiosk_messages()
            except:
                self.logger.exception("An error occured when uploading messages.")
            # ignore another call to stay alive
            try:
                self.service_server_messages(ignore_sa=True)
            except:
                self.logger.exception("An error occured when attempting to fetch new orders.")
        CMsgs.add_clientmessage(self.context, "Going to  die.", '', "Command parser", datetime.utcnow())
        try:
            self.upload_kiosk_messages()
        except:
            self.logger.exception("An error occured when uploading messages.")
        
    def upload_logs(self):
        upd = Uploader.DataUploader(self.context)
        ret = upd.zip_logfiles()
        if not ret:
            self.logger.info("Upload task exited. Error or nothing to sync.")
            return False
        (zipfile, manifest) = ret
        res = upd.upload_file(zipfile, manifest, upload_type="logs")
        if res:
            upd.create_sync_record(zipfile)
            return res
        
    def upload_data_messages(self):
        """Upload messages from datalogger to kiosk"""
        upd = Uploader.DataUploader(self.context)
        upd.get_filelist()
        ret = upd.build_zip_file()
        if not ret:
            self.logger.info("Upload task exited. Error or nothing to sync.")
            return False
        (zipfile, manifest) = ret
        res = upd.upload_file(zipfile, manifest)
        if res:
            upd.create_sync_record(zipfile)
            upd.update_filelist()
    
    def netsync(self):
        ## sync time if need be
        os.popen('ntpd -qg')
        time.sleep(5)
        
        try:
            self.logger.debug("Uploading kiosk messages")
            self.upload_kiosk_messages()
        except:
            self.logger.exception("Unable to upload kiosk messages")
        
        try:
            self.logger.debug("Uploading data")
            self.upload_data_messages()
        except:
            self.logger.exception('Network Synchronisation Failed!')
        
        try:
            self.logger.debug("Downloading server messages")
            self.service_server_messages()
        except:
            self.logger.exception("Unable to get commands from server.")
    
    def run(self):
        # time the datalogger started running
        starttime = datetime.utcnow()

        # the time the next internet sync should occur
        nextsync = starttime

        # the time the next sensor poll should occur
        nextpoll = starttime

        while True:
            # determine if we should poll
            if (datetime.utcnow() > nextpoll):
                # run the datalogging routine
                self.logger.info("Sensor poll commenced")
                self.datalog()

                # set the next poll to POLL_INTERVAL
                nextpoll = datetime.utcnow() + timedelta(seconds=10)

            # determine if we should do a network sync
            if (datetime.utcnow() > nextsync):
                # try the net connection
                if(not self._try_network()):
                    self.logger.warning("No net connectivity!")

                # run the netsync routine
                self.logger.info("Network sync commenced")
                self.netsync()

                # next sync is in SYNC_INTERVAL
                nextsync = datetime.utcnow() + timedelta(hours=6)

            # sleep for 10 seconds before looping
            time.sleep(10)