#!/usr/bin/python
#
#    Copyright 2011 National Evolutionary Synthesis Center (NESCent). 
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

# makes copies based on the template (first doc in the feed)
def MakeCopies(client,feed,counter,increment,stop):
	nameStub = 'newtest'
	template = feed.entry[0]
	while counter<stop:
		newName = nameStub+str(counter)+'_1'
		newfeed=client.GetResources(uri='/feeds/default/private/full/-/spreadsheet?title='+newName)
		# check to make sure we don't have this one already
		if not newfeed.entry:
			print 'new doc:',newName
			newdoc = client.CopyResource(template,newName)
		else:
			print 'already have:',newName 
		counter+=increment;
	
def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], '', ['user=', 'pw='])
	except getopt.error, msg:
		print 'python copyGoogleDocs.py --user [username] --pw [password] '
		sys.exit(2)

	user = ''
	pw = ''
	key = ''
	# Process options
	for option, arg in opts:
		if option == '--user':
	  		user = arg
		elif option == '--pw':
	  		pw = arg
	
	client = gdata.docs.client.DocsClient(source='nescent-parkNotebooks-v1')
	client.ssl = True
	client.http_client.debug = False
	try:
		client.ClientLogin(user,pw,client.source)
	except gdata.service.BadAuthentication:
		print "Error logging in with these credentials"
		return
	
	templateTitle='park_template'
	feed = client.GetResources(uri='/feeds/default/private/full/-/spreadsheet?title='+templateTitle)
  
	if not feed.entry:
		print 'No spreadsheet titled '+templateTitle+'\n'
	else:
		print 'copying '+templateTitle
		MakeCopies(client,feed,10020690,10,10020700)

if __name__ == '__main__':
	main()