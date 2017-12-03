#!/usr/bin/python
# flask main
# 2016-07-01 K.OHWADA

from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, jsonify
from sensor_db import SensorDb
from sensor_main import SensorMain
from sensor_post import SensorPost
from sensor_manage import SensorManage
from sensor_api import SensorApi
from sensor_status import SensorStatus
from sensor_util import SensorUtil
from server_conf import ServerConf

import logging

# Flask start	
app = Flask(__name__)
app.secret_key = 'koh6GaBo' # random characters
app.config['SESSION_TYPE'] = 'filesystem'

util = SensorUtil()
conf = ServerConf()

# global
g_db_param = None
g_conf = ''
g_secret = ''

# server_run
def server_run(host, port, basedir):
	global g_db_param, g_conf, g_secret
	debug_file_handler, error_file_handler = util.initLogFileHandler( basedir )
	app.logger.addHandler( debug_file_handler )
	app.logger.addHandler( error_file_handler )
	app.logger.setLevel( logging.DEBUG )
	g_conf = util.initConfig( basedir )
	# obj = util.readConf( g_conf )
	obj = conf.readConfFile( g_conf )
	if obj:
		g_db_param = {}
		g_db_param["db_name"] = obj["db_name"]
		g_db_param["user"] = obj["db_user"]
		g_db_param["passwd"] = obj["db_passwd"]	
		app.config['USERNAME'] = obj["login_username"]
		app.config['PASSWORD'] = obj["login_password"]
		g_secret = obj["sakura_secret"]
	app.run( host=str(host), port=int(port), use_reloader=True )

# route index
@app.route('/')
def route_main():		
	main = SensorMain( g_db_param, app.logger )
	conn = main.connect()
	if not conn:
		# not connect to DB
		if session.get('logged_in'):
			# if login
			return render_template('notice.html', conf=g_conf)
		else:
			# if not login
			msg = "Cannot connect to Database"
			param = { "datas":['', '', ''], "datetime":"", "error":msg }
	else:
		# connect to DB
		param = main.excute( request.args )
		main.close()
	return render_template('index.html', param=param)
	
# post
# header format
# EnvironHeaders([('Content-Length', u'345'), ('User-Agent', u'python-requests/2.10.0'), ('Connection', u'keep-alive'), ('Host', u'---'), ('Accept', u'*/*'), ('Content-Type', u'application/json'), ('Accept-Encoding', u'gzip, deflate'), ('X-Sakura-Signature', u'---')])
@app.route('/post', methods=['POST'])
def route_post():
	if request.method == 'POST':
		post = SensorPost( g_db_param, app.logger, g_secret )
		post.excute( request.headers.get("X-Sakura-Signature"), request.data )
	return ""

# manage
@app.route('/manage', methods=['GET', 'POST'])
def route_manage():
	if not session.get('logged_in'):
		# if not login
		return redirect(url_for('route_login'))	
	manage = SensorManage( g_db_param, app.logger )
	conn = manage.connect()
	if not conn:
		# not connect to DB
		return redirect(url_for('route_main'))	
	if request.method == 'GET':
		# get
		action = request.args.get('action', '')
		print "action " + action
		if action == "add_form":
			params = manage.makeAddForm( request.args )
			manage.close()
			return render_template( 'manage_add_form.html', params=params )
		elif action == "edit_form":
			params = manage.makeEditForm( request.args )
			manage.close()
			return render_template( 'manage_edit_form.html', params=params )
		else:
			rows = manage.makeList( request.args )
			manage.close()
	elif request.method == 'POST':
		# post
		rows = manage.post( request.form )			
		manage.close()
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

# api
@app.route('/api')
def route_api():
	api = SensorApi( g_db_param, app.logger )
	res = api.excute(None)
	return jsonify(res)

# status
@app.route('/status')
def route_status():
	status = SensorStatus( g_db_param, app.logger )
	res = status.excute()
	return res

# error 500
@app.errorhandler(500)
def error_500(exception):
	app.logger.error(exception)
	return render_template('error500.html'), 500
	
# Flask end
