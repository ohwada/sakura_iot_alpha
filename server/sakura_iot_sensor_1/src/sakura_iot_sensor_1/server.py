#!/usr/bin/python
# flask main
# 2016-07-01 K.OHWADA

from flask import Flask, render_template, request, redirect, url_for, session, flash
from sensor_db import SensorDb
from sensor_main import SensorMain
from sensor_post import SensorPost
from sensor_manage import SensorManage
from sensor_util import SensorUtil

# Flask start	
app = Flask(__name__)
app.secret_key = 'koh6GaBo'
app.config['SESSION_TYPE'] = 'filesystem'

util = SensorUtil()

# global
g_db = None
g_conf = ''

# server_run
def server_run(host, port, conf):
	global g_db, g_conf
	g_conf = conf
	obj = util.readConf( conf )
	if obj:
		g_db = util.connect( obj["db_name"], obj["db_user"], obj["db_passwd"], obj["db_timeout"] )
		app.config['USERNAME'] = obj["login_username"]
		app.config['PASSWORD'] = obj["login_password"]
	app.run(host=str(host), port=int(port))

# route index
@app.route('/', methods=['POST', 'GET'])
def route_main():
	if not g_db:
		return render_template('notice.html', conf=g_conf)
	main = SensorMain(g_db)		
	param = main.excute( request.args )
	return render_template('index.html', param=param)

# post
# header format
# EnvironHeaders([('Content-Length', u'345'), ('User-Agent', u'python-requests/2.10.0'), ('Connection', u'keep-alive'), ('Host', u'---'), ('Accept', u'*/*'), ('Content-Type', u'application/json'), ('Accept-Encoding', u'gzip, deflate'), ('X-Sakura-Signature', u'---')])
@app.route('/post', methods=['POST'])
def route_post():
	if not g_db:
		return ""
	if request.method == 'POST':
#		print request.headers.get("X-Sakura-Signature")	
		post = SensorPost( g_db )
		post.excute( request.data )
	return ""

# manage
@app.route('/manage', methods=['POST', 'GET'])
def route_manage():
	if not g_db:
		return redirect(url_for('route_main'))		
	if not session.get('logged_in'):
		return redirect(url_for('route_login'))	
	manage = SensorManage( g_db )
	if request.method == 'GET':
		# get
		action = request.args.get('action', '')
		print "action " + action
		if action == "add_form":
			params = manage.makeAddForm( request.args )
			return render_template( 'manage_add_form.html', params=params )
		elif action == "edit_form":
			params = manage.makeEditForm( request.args )
			return render_template( 'manage_edit_form.html', params=params )
		else:
			rows = manage.makeList( request.args )
	elif request.method == 'POST':
		# post
		rows = manage.post( request.form )			
	return render_template( 'manage_list.html', rows=rows )

@app.route('/login', methods=['GET', 'POST'])
def route_login():
	error = None
	if app.config['USERNAME'] is None:
		return redirect(url_for('route_main'))		
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('route_manage'))
	return render_template('login.html', error=error)

@app.route('/logout')
def route_logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('route_main'))
				
# Flask end
