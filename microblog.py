# -*- coding:utf-8 -*-
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

app = Flask(__name__)
app.config.from_object('config')

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('db/schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()
	g.db.close()

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/signup')
def signup():
	return render_template('signup.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
	error = None
	if request.method == 'POST':
		print request.form['password'] , request.form['confirmpwd']
		print (request.form['password'] == request.form['confirmpwd'])
		if request.form['password'] == request.form['confirmpwd']:
			g.db.execute('insert into user (username, password, email, role) values (?, ?, ?, ?)',
				[request.form['username'], request.form['password'], request.form['email'], app.config['ROLE_USER']])
			g.db.commit()
			return redirect(url_for('index'))
		else:
			error = 'The New Password and Confirm New Password fields do not match.'
			return render_template('signup.html', error=error)

@app.route('/signin')
def signin():
	return render_template('signin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	cur = g.db.execute("select * from user where username='" + request.form['username'] 
		+ "' and password='" + request.form['password'] + "'")
	u = cur.fetchall()
	#print u
	if not u:
		print 'ERROR Incorrect username or password!'
		error = 'Incorrect username or password'
		return render_template(('signin.html'), error=error)
	else:
		session['logged_in'] = True
		session['username'] = u[0][1]
		return redirect(url_for('index'))

@app.route('/signout')
def signout():
	session.pop('logged_in', None)
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run()