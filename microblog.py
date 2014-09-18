# -*- coding:utf-8 -*-
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from  datetime  import  * 

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
	if 'logged_in' in session:
		#print session['username']
		cur = g.db.execute("select * from user where username=?", [session['username']])
		u = cur.fetchall()
		cur = g.db.execute("select content, timestamp from post where user_id=?", [u[0][0]])
		posts = [dict(username=session['username'], content=row[0], timestamp=row[1]) for row in cur.fetchall()]
		
		return render_template('index.html', posts=posts)
	else:
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
		cur = g.db.execute("select content, timestamp from post where user_id=?", [u[0][0]])
		posts = [dict(username=u[0][1], content=row[0], timestamp=row[1]) for row in cur.fetchall()]
		
		return render_template('index.html', posts=posts)

@app.route('/signout')
def signout():
	session.pop('logged_in', None)
	return redirect(url_for('index'))

@app.route('/post', methods=['GET', 'POST'])
def post():
	if request.method == 'POST':
		cur = g.db.execute("select * from user where username=?", [request.form['username']])
		u = cur.fetchall()
		now = datetime.now()
		timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
		g.db.execute('insert into post (content, timestamp, user_id) values (?, ?, ?)',
				[request.form['content'], timestamp, u[0][0]])
		g.db.commit()
		cur = g.db.execute("select content, timestamp from post where user_id=?", [u[0][0]])
		posts = [dict(username=u[0][1], content=row[0], timestamp=row[1]) for row in cur.fetchall()]
		
		return render_template('index.html', posts=posts)

@app.route('/find')
def find():

	#the user that i followed
	cur = g.db.execute("select * from user where username=?", [session['username']])
	me = cur.fetchall()
	#print 'me' + str(me)
	cur = g.db.execute("select * from followers where follower_id=?", [me[0][0]])
	ifollowed = cur.fetchall()
	#print "i followed" + str(ifollowed)
	#i followed[(1, 2), (1, 3)]]
	ifos = []
	for ifo in ifollowed:
		ifos.append(ifo[1])
	#[2,3]

	# all user except me
	cur = g.db.execute("select * from user where username!=?", [session['username']])
	u = cur.fetchall()
	count = len(u)
	c = 0
	users_id = []

	while c < count:
		if u[c][0] in ifos:
			print str(u[c][0]) + "in ifos"
		else:
			users_id.append([u[c][0], u[c][1]])
			#print [u[c][0], u[c][1]]
		c += 1
	#print users_id
	#[[2, u'b'], [3, u'c'], [4, u'd']]

	posts = []
	for n in users_id:
		cur = g.db.execute("select content, timestamp from post where user_id=?", [n[0]])
		post = [dict(user_id=n[0], username=n[1], content=row[0], timestamp=row[1]) for row in cur.fetchall()]
		posts.append(post)
	#print posts
	return render_template('find.html', posts=posts)

@app.route('/tofollow', methods=['GET', 'POST'])
def tofollow():
	if request.method == 'POST':
		#followed
		#print 'username:'+request.form['uid']
		cur = g.db.execute("select * from user where id=?", [request.form['uid']])
		u_followed = cur.fetchall()
		#print u_followed
		#follower
		cur = g.db.execute("select * from user where username=?", [session['username']])
		u_follower = cur.fetchall()
		#print u_follower
		g.db.execute('insert into followers (follower_id, followed_id) values (?, ?)',
				[u_follower[0][0], u_followed[0][0]])
		g.db.commit()

		#return render_template('find.html', posts=posts)
		return redirect(url_for('find'))

@app.route('/following', methods=['GET', 'POST'])
def following():
	cur = g.db.execute("select * from user where username=?", [session['username']])
	u = cur.fetchall()	
	cur = g.db.execute("select * from followers where follower_id=?", [u[0][0]])
	followed_id = cur.fetchall()	
	#print followed_id
	posts = []
	for n in followed_id:
		cur = g.db.execute("select content, timestamp, username from user, post where user.id=post.user_id and user_id=?", [n[1]])
		post = [dict(user_id=n[1], content=row[0], timestamp=row[1], username=row[2]) for row in cur.fetchall()]
		posts.append(post)
	#print posts
	return render_template('following.html', posts=posts)

@app.route('/unfollow', methods=['GET', 'POST'])
def unfollow():
	if request.method == 'POST':
		g.db.execute('delete from followers where followed_id=?',[request.form['fid']])
		g.db.commit()
		return redirect(url_for('following'))


if __name__ == '__main__':
	app.run()