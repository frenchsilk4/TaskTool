# all the imports
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

''' ------------------------------- setup and initialize app ------------------------------- '''
#configuration
DATABASE = 'tmp/todos.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)

#connect to database
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db',None)
	if db is not None:
		db.close()

''' ------------------------------- your routes go here ------------------------------- '''
@app.route('/')
def show_entries():
    cur = g.db.execute('select id,title,done from todos order by id desc')
    todos = [dict(id=row[0],title=row[1],done=row[2]) for row in cur.fetchall()]
    return render_template('show_entries.html',todos=todos)

@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error = error)

@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))
	
# CODE to fire up the server
if __name__ == '__main__':
	app.run()
