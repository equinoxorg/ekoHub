#!/usr/bin/python
import logging
import sys
import time

from ConfigParser import ConfigParser

import eko.Util.DBSetup as DBSetup

import os.path

from os import makedirs

from eko.Sensors.ModbusInterface import Harvester, SensorConfigException

import eko.SystemInterface.OSTools as OSTools

import eko.SystemInterface.Beagleboard as Beagleboard

logging.basicConfig(format='%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

if __name__=="__main__":
    if len(sys.argv) != 4:
        print 'USAGE: configsingle.py CONFIG_FILE OUTPUT_PATH CONFIG_PATH'
        sys.exit(0)
    cfgpath = sys.argv[1]
    datapath = sys.argv[2]
    context = {'config': sys.argv[3]}
    hv = Harvester(cfgpath, datapath, context)
    hv.harvest()