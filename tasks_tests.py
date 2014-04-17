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

	def removeDB(self):
		"""Delete after each test"""
		os.close(self.db_fd)
		os.unlink(tasks.app.config['DATABASE'])

	def emptyDB(self):
		rv = self.app.get('/')
		assert b'No entries here so far' in rv.data
		
# CODE to fire up the server
if __name__ == '__main__':
	unittest.main()