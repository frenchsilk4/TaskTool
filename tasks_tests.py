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

	def test_emptyDB(self):
		rv = self.app.get('/')
		assert b'Unbelievable. No entries here so far' in rv.data

	def login(self, username, password):
		return self.app.post('/login',data=dict(username=username, password=password), follow_redirects=True)

	def logout(self):
		return self.app.get('/logout', follow_redirects=True)

	def test_login_logout(self):
		rv = self.login('admin','default')
		assert 'You were logged in' in rv.data

		rv = self.logout()
		assert 'You were logged out' in rv.data

		rv = self.login(tasks.app.config['USERNAME'] + 'x', tasks.app.config['PASSWORD'])
		assert b'Invalid username' in rv.data

		rv = self.login(tasks.app.config['USERNAME'], tasks.app.config['PASSWORD'] + 'x')
		assert b'Invalid password' in rv.data

	def test_add_to_DB(self):
		self.login('admin','default')
		rv = self.app.post('/add', data = dict(title='Pick up coffee'), follow_redirects=True)
		assert 'Tasks on hand' not in rv.data
		assert 'Pick up coffee' in rv.data

	def test_update_to_DB(self):
		self.login('admin','default')
		rv = self.app.get('/update/1',follow_redirects=True)
		print rv.data
		assert 'New entry was successfully updated' in rv.data


	def test_delete_in_DB(self):
		self.login('admin','default')
		rv = self.app.get('/delete/1', follow_redirects=True)
		assert 'Pick up coffee' not in rv.data

# CODE to fire up the server
if __name__ == '__main__':
	unittest.main()

