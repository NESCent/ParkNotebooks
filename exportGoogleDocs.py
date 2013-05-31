#!/usr/bin/python

#    Copyright 2011-2013 National Evolutionary Synthesis Center (NESCent).
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
import gdata.docs.service
import gdata.docs.client
import os.path
import copyGoogleDocs

DOWNLOAD_DIR = '/Users/dan/parkNotebooks/exports/batch1/'

def DownloadFeed(client,feed,dir):
	if not feed.entry:
		print 'No entries in feed\n'
	for entry in feed.entry:
		title=entry.title.text.encode('UTF-8')
		destinationFile=os.path.join(dir, title+'.csv')
		if not os.path.exists(destinationFile):
			print 'Downloading spreadsheet to %s' % destinationFile
			client.DownloadResource(entry, destinationFile, extra_params={'gid': 0, 'exportFormat': 'csv'})  # export the first sheet as csv	
		else: 
			print '%s already exists' % destinationFile
	

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], '', ['user=', 'pw=', 'sheets='])
	except getopt.error, msg:
		print 'python exportGoogleDocs.py --user [username] --pw [password] --sheets [spreadsheet names]'
		sys.exit(2)

	user = None
	pw = None
	sheets = None
	# Process options
	for option, arg in opts:
		if option == '--user':
	  		user = arg
		elif option == '--pw':
	  		pw = arg
		elif option == '--sheets':
	  		sheets = arg

	if user is None or pw is None or sheets is None:
		print 'python exportGoogleDocs.py --user [username] --pw [password] --sheets [spreadsheet names]'
		sys.exit(2)
	# Source is the application name
	client = gdata.docs.client.DocsClient(source='nescent-parkNotebooks-v1')
	client.ssl = True
	client.http_client.debug = False
	try:
		client.ClientLogin(user,pw,client.source)
	except gdata.service.BadAuthentication:
		print "Error logging in with these credentials"
		return

	sheetNames = copyGoogleDocs.getDestinationNames(sheets)
	for sheetName in sheetNames:
		feed = client.GetResources(uri='/feeds/default/private/full/-/spreadsheet?title='+sheetName)

		if not feed.entry:
			print 'No spreadsheet titled '+titleSearchStr+'\n'
		else:
			DownloadFeed(client,feed,DOWNLOAD_DIR)

if __name__ == '__main__':
	main()