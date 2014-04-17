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

@app.route('/add',methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into todos(title,done) values(?,?)',[request.form['title'],0])
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

@app.route('/update/<int:todo_id>')
def update_entry(todo_id):
    '''update todo with the id todo_id '''
    g.db.execute('UPDATE todos SET done=? WHERE id=?',[1,int(todo_id)])
    g.db.commit()
    flash('New entry was successfully updated')
    return redirect(url_for('show_entries'))

@app.route('/delete/<int:todo_id>')
def delete_entry(todo_id):
    '''delete todo with the id todo_id''' 
    g.db.cursor().execute('DELETE FROM todos WHERE rowid = ?', [int(todo_id)])
    g.db.commit()
    flash('Item was successfully deleted')
    return redirect(url_for('show_entries'))

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

