import os
import tasks
import unittest
import tempfile

class appTestCase(unittest.TestCase):

	def setUp(self):
		"""Setup a blank database for test"""
		self.db_fd, tasks.app.config['DATABASE'] = tempfile.mkstemp()
		tasks.app.config['TESTING']= True
		self.app = tasks.app.test_client()
		tasks.init_db()
# CODE to fire up the server
if __name__ == '__main__':
	unittest.main()
