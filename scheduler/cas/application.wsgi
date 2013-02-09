#!/usr/bin/env python


from cgi import parse_qs, escape
import sys
sys.path.append('/srv/www/scheduler/application/')
import pycas
from pycas import CAS_OK, CAS_COOKIE_EXPIRED, CAS_COOKIE_INVALID
from pycas import CAS_TICKET_INVALID, CAS_GATEWAY, CAS_NOTLOGGED, CAS_MSG

def application(environ, start_response):
	CAS_SERVER  = "http://login.case.edu"
    SERVICE_URL = "http://concertina.case.edu/"
	
	status, id, cookie = pycas.login(CAS_SERVER, SERVICE_URL, environ, secure=0, opt="gateway")
	if (status == CAS_OK):
		good_html = """
		<html>
		<head>
		<title>
		castest.py
		</title>
		<style type=text/css>
		td {background-color: #dddddd; padding: 4px}
		</style>
		</head>
		<body>
		<h2>pycas.py</h2>
		<hr>
		<p>
		<b>Parameters returned from pycas.login()</b>
		<table>
		<tr><td>status</td><td> <b>%s</b> - <i>%s</i></td></tr>
		<tr><td>id</td><td> <b>%s</b></td></tr>
		<tr><td>cookie</td><td> <b>%s</b></td></tr>
		</table>
		</p>
		</body></html>""" % (status,CAS_MSG[status],id,cookie)
		response_body = good_html
		stat = '200 OK'
		cookie_parts = cookie.split(":")
		response_headers = [(cookie_parts[0], ':'.join(cookie_parts[1:])), ('Content-Type', 'text/html'),
			('Content-Length', str(len(response_body)))]
	elif (status == CAS_NOTLOGGED):
		opt = ""
		secure = 0
		response_body = pycas.do_redirect(CAS_SERVER, SERVICE_URL, opt, secure)	
		cas_url  = CAS_SERVER + "/cas/login?service=" + SERVICE_URL
		stat = '307 TEMPORARY REDIRECT'
		response_headers = [('Location', cas_url),('Content-Type', 'text/html'),
			('Content-Length', str(len(response_body)))]
	else:
		response_body = """something went wrong %s""" % (status)
	#stat = '200 OK'
	#response_headers = [('Content-Type', 'text/html'),
	#	('Content-Length', str(len(response_body)))]
	start_response(stat, response_headers)

	return [response_body]
