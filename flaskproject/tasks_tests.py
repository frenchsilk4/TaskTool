import os
import app
import unittest
import tempfile

class appTestCase(unittest.TestCase):

	def setUp(self):
		"""Setup a blank database for test"""
		self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
		flaskr.app.config['TESTING']= True
		self.app = flaskr.app.test_client()
		flaskr.init_db()
# CODE to fire up the server
if __name__ == '__main__':
	unittest.main()
