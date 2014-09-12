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
		if request.form['password'] != request.form['confirmpwd']:
			error = 'The New Password and Confirm New Password fields do not match.'
		else:
			g.db.execute('insert into user (username, password, email, role) values (?, ?, ?, ?)',
				[request.form['username'], request.form['password'], request.form['email'], app.config['ROLE_USER']])
			g.db.commit()
			print request.form['username'], request.form['password'], request.form['email'], app.config['ROLE_USER']
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run()