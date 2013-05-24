#!/usr/bin/python
#
#    Copyright 2013 National Evolutionary Synthesis Center (NESCent).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import getopt
import tempfile
import gdata.docs.service
import gdata.docs.client

import checkData
import exportGoogleDocs

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], '', ['user=', 'pw='])
	except getopt.error, msg:
		print 'python checkGoogleDocs.py --user [username] --pw [password]'
		sys.exit(2)

	user = None
	pw = None
	key = ''
	# Process options
	for option, arg in opts:
		if option == '--user':
	  		user = arg
		elif option == '--pw':
	  		pw = arg

	if user is None or pw is None:
		print 'python checkGoogleDocs.py --user [username] --pw [password] '
		sys.exit(2)

	# Source is just a name identifying this application
	client = gdata.docs.client.DocsClient(source='nescent-parkNotebooks-v1')
	client.ssl = True
	client.http_client.debug = False
	try:
		client.ClientLogin(user,pw,client.source)
	except gdata.service.BadAuthentication:
		print "Error logging in with these credentials"
		return

	# Make a temp directory
	tempdir = tempfile.mkdtemp()
	# export the docs there

	titleSearchStr='ftbms010010020_1'
	feed = client.GetResources(uri='/feeds/default/private/full/-/spreadsheet?title='+titleSearchStr)

	if not feed.entry:
		print 'No spreadsheet titled '+titleSearchStr+'\n'
		return
	exportGoogleDocs.DownloadFeed(client, feed, tempdir)
	# run checkdata on it
	checkData.checkDirectory(tempdir)

if __name__ == '__main__':
	main()