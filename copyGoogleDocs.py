#!/usr/bin/python
#
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
import gdata.acl.data
import csv

from os.path import *

DOC_SUFFIX = '_1'
IMAGE_BASE_URL = "http://www.nescent.org/Park_notebooks/full_scans/"

# reads in a list of relative paths to jpeg files
# ./experiment1/tbcms01001001.jpg
# ...
# ./experiment2/tbcms02006040.jpg
def getDestinationNames(filename):
	filenames = []
	with open(filename, 'rb') as files:
		for line in files:
			filenames.append(line.rstrip())
	return filenames

# makes a single copy to the filename provided
def MakeCopy(client, feed, dest):
	sheetBasename = splitext(basename(dest))[0]
	template = feed.entry[0]
	newName = sheetBasename + DOC_SUFFIX
	newfeed = client.GetResources(uri='/feeds/default/private/full/-/spreadsheet?title='+newName)
	# check to make sure we don't have this one already
	if not newfeed.entry:
		print 'new doc:',newName
		newdoc = client.CopyResource(template,newName)
		# Make it editable to anyone with the link
		scope = gdata.acl.data.AclScope(type='default')
		role = gdata.acl.data.AclRole(value='writer')
		acl_entry = gdata.docs.data.AclEntry(scope=scope, role=role)
		# Need the feed entry
		newfeed = client.GetResources(uri='/feeds/default/private/full/-/spreadsheet?title='+newName)
		new_acl = client.Post(acl_entry, newfeed.entry[0].GetAclFeedLink().href)

	else:
		print 'already have:',newName
	# Now we need a URL for this
	# URL should look like https://docs.google.com/spreadsheet/ccc?key=0Ag-1ley90MKndE5IX2RjQk5ybmVobzVrMGt0RlJiWnc
	newfeed = client.GetResources(uri='/feeds/default/private/full/-/spreadsheet?title='+newName)
	spreadsheetURL = newfeed.entry[0].GetAlternateLink().href.replace('&usp=docslist_api','')
	imageURL = IMAGE_BASE_URL + dest[2:]

	return {'data_entry_spreadsheet': spreadsheetURL , 'image_url': imageURL}

# makes copies based on the template (first doc in the feed)
def MakeCopies(client,feed,counter,increment,stop):
	nameStub = 'newtest'
	template = feed.entry[0]
	while counter<stop:
		newName = nameStub+str(counter)+DOC_SUFFIX
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
		opts, args = getopt.getopt(sys.argv[1:], '', ['user=', 'pw=', 'jpeglist=', 'output='])
	except getopt.error, msg:
		print 'python copyGoogleDocs.py --user [username] --pw [password] --jpeglist [list of jpeg filenames] --output [csvfile]'
		sys.exit(2)

	user = None
	pw = None
	jpeglist = None
	outputfile = None
	key = ''
	# Process options
	for option, arg in opts:
		if option == '--user':
	  		user = arg
		elif option == '--pw':
	  		pw = arg
		elif option == '--jpeglist':
			jpeglist = arg
		elif option == '--output':
			outputfile = arg

	if user is None or pw is None or jpeglist is None or outputfile is None:
		print 'python copyGoogleDocs.py --user [username] --pw [password] --jpeglist [list of jpeg filenames] --output [csvfile]'
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
	
	templateTitle='park_template'
	feed = client.GetResources(uri='/feeds/default/private/full/-/spreadsheet?title='+templateTitle)
  
	if not feed.entry:
		print 'No spreadsheet titled '+templateTitle+'\n'
	else:
		print 'copying '+templateTitle
		try:
			names = getDestinationNames(jpeglist)
		except:
			print "Unable to read file names from %s" % jpeglist
			return
		links = []
		for name in names:
			link = MakeCopy(client, feed, name)
			links.append(link)
			print str(link)
		# now make a CSV out of the links
		#image_url,data_entry_spreadsheet
		with open(outputfile, 'wb') as csvfile:
			csvwriter = csv.DictWriter(csvfile, fieldnames=["image_url", "data_entry_spreadsheet"])
			csvwriter.writeheader()
			csvwriter.writerows(links)

if __name__ == '__main__':
	main()