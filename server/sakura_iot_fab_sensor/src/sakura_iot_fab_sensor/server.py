#!/usr/bin/python
# flask main
# 2016-07-01 K.OHWADA

from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from sensor_db import SensorDb
from sensor_main import SensorMain
from sensor_post import SensorPost
from sensor_manage import SensorManage
from sensor_util import SensorUtil
import logging

# Flask start	
app = Flask(__name__)
app.secret_key = 'koh6GaBo' # random characters
app.config['SESSION_TYPE'] = 'filesystem'

util = SensorUtil()

# global
g_db = None
g_conf = ''

# future use
g_signature = ''

# server_run
def server_run(host, port, basedir):
	global g_db, g_conf, g_signature
	debug_file_handler, error_file_handler = util.initLogFileHandler( basedir )
	app.logger.addHandler( debug_file_handler )
	app.logger.addHandler( error_file_handler )
	app.logger.setLevel( logging.DEBUG )
	g_conf = util.initConfig( basedir )
	obj = util.readConf( g_conf )
	if obj:
		# set param, if the contents of the file is correct 
		g_db = util.connect( obj["db_name"], obj["db_user"], obj["db_passwd"], obj["db_timeout"], app.logger )
		app.config['USERNAME'] = obj["login_username"]
		app.config['PASSWORD'] = obj["login_password"]
		# future use
		g_signature = obj["sakura_secret"]
		if not g_db:
			# if can not connect db
			print "check " + g_conf
	app.run( host=str(host), port=int(port), use_reloader=True )

# route index
@app.route('/', methods=['GET'])
def route_main():
	if not g_db:
		# if db param are not set
		return render_template('notice.html', conf=g_conf)	
	main = SensorMain( g_db, app.logger )		
	param = main.excute( request.args )
	return render_template('index.html', param=param)

# post
# header format
# EnvironHeaders([('Content-Length', u'345'), ('User-Agent', u'python-requests/2.10.0'), ('Connection', u'keep-alive'), ('Host', u'---'), ('Accept', u'*/*'), ('Content-Type', u'application/json'), ('Accept-Encoding', u'gzip, deflate'), ('X-Sakura-Signature', u'---')])
@app.route('/post', methods=['POST'])
def route_post():
	if not g_db:
		# if db param are not set
		return ""
	if request.method == 'POST':
		# future use
		# if request.headers.get("X-Sakura-Signature") == g_signature
		post = SensorPost( g_db, app.logger )
		post.excute( request.data )		
	return ""

# manage
@app.route('/manage', methods=['POST', 'GET'])
def route_manage():
	if not g_db:
		# if db param are not set
		return redirect(url_for('route_main'))	
	if not session.get('logged_in'):
		# if not login
		return redirect(url_for('route_login'))	
	manage = SensorManage( g_db, app.logger )
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

# login
@app.route('/login', methods=['GET', 'POST'])
def route_login():
	error = None
	if app.config['USERNAME'] is None:
		# if password param are not set
		return redirect(url_for('route_main'))		
	if request.method == 'POST':
		# post
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			# login, if pass check 
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('route_manage'))
	# when not login		
	return render_template('login.html', error=error)

# logout
@app.route('/logout')
def route_logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('route_main'))

# error 500
@app.errorhandler(500)
def error_500(exception):
	app.logger.error(exception)
	return render_template('error500.html'), 500
	
# Flask end
