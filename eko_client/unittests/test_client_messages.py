import random
import unittest
import sqlite3

from os.path import join

import eko.Util.DBSetup as DBSetup
import eko.WebService.ClientMessages as CMsgs

from datetime import datetime

import logging
logger = logging.getLogger('testcase')

class TestClientMessageUpload(unittest.TestCase):

	def setUp(self):
		# Create context
		self.ctx = {}
		self.ctx['config'] = 'unittests/config'
		self.ctx['output'] = 'unittests/data'
		self.ctx['json_api'] = 'http://v2.ekohub.org/api/json'
		self.ctx['serial'] = '123456'
		DBSetup.check_databases(self.ctx['config'])

	def _del_cmsgs_all(self):
		configpath = self.ctx['config']
		con = sqlite3.connect(join(configpath, 'sync.db'), detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
		c = con.cursor()
		try:
			c.execute("DELETE FROM clientmsg")
		except sqlite3.Error:
			logger.exception("Error deleting rows from sync.db.")
		finally:
			c.close()
			con.close()

	def test_add(self):
		message = "Hello World Test Case 1 Dorem Lorem Dolor Sit Amet"
		sessionref = "reference9"
		origin = "cloud9"
		origintime = datetime.now()

		self._del_cmsgs_all()

		# Add to database
		CMsgs.add_clientmessage(self.ctx, message, sessionref, origin, origintime)

		configpath = self.ctx['config']
		con = sqlite3.connect(join(configpath, 'sync.db'), detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
		c = con.cursor()
		try:
			c.execute("SELECT message, sessionref, origin, origintime, id FROM clientmsg WHERE synctime is NULL LIMIT 15")
			rows = c.fetchall()
		except sqlite3.Error:
			logger.exception("Error fetching rows from sync.db.")
			rows = None
		finally:
			c.close()
			con.close()

		self.assertEqual(message, rows[0][0])
		self.assertEqual(sessionref, rows[0][1])
		self.assertEqual(origin, rows[0][2])
		#self.assertEqual(origintime, rows[0][3])

	def test_upload(self):
		message = "Hello World Test Case 1 Dorem Lorem Dolor Sit Amet"
		sessionref = "reference9"
		origin = "cloud9"

		self._del_cmsgs_all()
		
		for i in range(1,5):
			CMsgs.add_clientmessage(self.ctx, message+str(i), str(i), origin+str(i), datetime.now())

		self.assertTrue(CMsgs.transmit_clientmessages(self.ctx))

if __name__=='__main__':
	unittest.main()