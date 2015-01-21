import argparse
import platform
from os import path

import sqlite3

from eko_logger import DataLogger

import eko.Util.DBSetup as DBSetup

import logging
import logging.config

if path.exists('ekologging.config'):
	logging.config.fileConfig('ekologging.config')
else:
	logging.basicConfig(format='%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

logger = logging.getLogger('eko.startup')

def _print_startup(args):
	print("EKOLogger Script Startup")
	print("-"*25+'\n')
	for key in args.keys():
		print("%s: %s" % (key, args[key]))
	print("")


def launch():
	# See the python 2.7 argparse documentation

	parser = argparse.ArgumentParser(description='The Energy Kiosk Observer datalogging process')

	parser.add_argument('-c', '--config', action='store', default='/etc/eko/', help="Path to config file", metavar="CONFIG")
	parser.add_argument('-o', '--output', action='store', default='/data', help="Path to output directory", metavar="OUTDIR")
	parser.add_argument('-z', '--zip', action='store', default='/tmp', help="Path to storage directory for zip payloads", metavar="ZIPDIR")
	parser.add_argument('--sensor_configs', action='store', default='configs/sensors', help="Path to Sensor Config files", metavar="SENSOR_CONFIGS")
	parser.add_argument('-p', '--poll', action='store', default=300, type=int, help="Seconds between sensor polls", metavar="SECONDS")
	parser.add_argument('-s', '--sync', action='store', default=60*60*1, type=int, help="Seconds between data synchronisations", metavar="SECONDS")
	parser.add_argument('serial', action='store', help='kiosk identifier', metavar="SERIAL")
	
	args = parser.parse_args()
	_print_startup(vars(args))
	return vars(args)
	#print args

def self_checks(ctx):
	# Check to see if we're in python 2.7
	pyver = platform.python_version_tuple()
	logger.info('Python %s.%s.%s detected' % pyver)
	if (pyver[0] != '2') and (pyver[1] != '7'):
		logger.warning('Python 2.7 is the reccomended platform. You may encounter errors.')

	# Check to see if paths exist
	if (not path.exists(ctx['config'])):
		logger.critical('Path %s does not exist !!' % ctx['config'])
		exit(-1)

	if (not path.exists(ctx['output'])):
		logger.critical('Path %s does not exist !!' % ctx['output'])
		exit(-2)

	# Check to see if key exists
	if (not path.exists(path.join(ctx['config'], 'privatekey.pem'))):
		logger.critical('Cannot find privatekey.pem in config path %s !!' % ctx['config'])
		exit(-4)

	# Test required modules
	try:
		import serial
	except ImportError:
		logger.critical('Required module pyserial not installed.')
		exit(-3)

	try:
		import Crypto
	except ImportError:
		logger.critical('Required module PyCrypto not installed.')
		exit(-3)

	from Crypto.PublicKey import RSA
	f = open(path.join(ctx['config'], 'privatekey.pem'), 'r')
	try:
		k = RSA.importKey(f.read())
	except:
		logger.exception('Cannot import RSA public key !!')
		exit(-5)
	f.close()


	try:
		import modbus_tk
	except ImportError:
		logger.critical('Required module modbus-tk not installed. See http://code.google.com/p/modbus-tk.')
		exit(-3)

	try:
		import poster
	except ImportError:
		logger.critical('Required module poster not installed. See http://pypi.python.org/pypi/poster/0.4.')
		exit(-3)

	# Test Databases
	try:
		# check integrity of sync and filelist dbs in output dir
		DBSetup.check_databases(ctx['config'])
	except (sqlite3.Error, IOError, OSError):
		self.logger.critical("Databases could not be opened.")
		exit(-4)

	return True


if  __name__=="__main__":
	# Get command line options on launch
	ctx = launch()

	ctx['json_api'] = 'http://v2.ekohub.org/api/json'
	ctx['upload_api'] = 'http://v2.ekohub.org/api/upload_request'
	ctx['sensorcfg'] = ctx['sensor_configs']
	# run self tests
	self_checks(ctx)

	# start the datalogger script
	dl = DataLogger(ctx)
	dl.run()

