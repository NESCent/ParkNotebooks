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

# check data in park notebook sheets
# the headers are Date,Age,Obsr.,small,med.,large,sum,PUPAE,IMAGO,Sum Total
# sum = small + med + large
# Sum Total = sum + pupae + imago


import sys
import os
import csv

HEADERS = ['Date', 'Age', 'Obsr.', 'small', 'med.', 'large', 'sum', 'PUPAE', 'IMAGO', 'Sum Total']

def checkDirectory(directoryName):
	filenames = os.listdir(directoryName)
	directoryErrors = []
	for filename in filenames:
		errors = checkFile(os.path.join(directoryName, filename))
		directoryErrors.append({'filename': filename, 'errors': errors})
	return directoryErrors

def checkFile(filename):
	errors = []
	with open(filename, 'rb') as csvfile:
		# can specify fieldnames here, but would rather confirm them directly
		csvdata = csv.DictReader(csvfile)
		for dictRow in csvdata:
			result = checkRow(dictRow)
			if result is not None:
				errors.append({'line': csvdata.line_num, 'row': dictRow, 'error': result})
	if len(errors) == 0:
		print "%s: OK" % os.path.basename(filename)
   	else:
		print "%s: FAILED" % os.path.basename(filename)
		for failure in errors:
			print "  Line %d of %s failed check with error: %s" % (failure['line'], os.path.basename(filename), failure['error'])
	return errors

def checkRow(dictRow):
	# first simply check the number of rows
	if len(dictRow) != len(HEADERS):
		return "wrong number of headers in CSV row"
	# second, check to make sure the headers are the same
	if sorted(HEADERS) != sorted(dictRow.keys()):
		return "Headers in CSV row don't match the template"
	# third, check the data
	# CSV library returns strings.  Convert to ints where we expect numbers
	smlDict = {k: dictRow[k] for k in ['small','med.','large','sum']}
	missingValuesDict = {}
	for k in smlDict:
		try:
			val = int(smlDict[k])
		except ValueError:
			val = 0.0
			missingValuesDict[k] = True
		smlDict[k] = val

	spiDict = {k: dictRow[k] for k in ['sum','PUPAE','IMAGO','Sum Total']}
	for k in spiDict:
		try:
			val = int(spiDict[k])
		except ValueError:
			val = 0.0
			missingValuesDict[k] = True
		spiDict[k] = val

	# small and medium may be combined into one column in some rows, but both can't be missing
	if 'small' in missingValuesDict and 'med.' in missingValuesDict:
		return "small and med. both missing"
	# small + medium + large must equal sum
	calculatedSum = smlDict['small'] + smlDict['med.'] + smlDict['large']
	if  calculatedSum != smlDict['sum']:
		return "small + med. + large = %d but expected %d" % (calculatedSum, smlDict['sum'])
	# sum + pupae + imago must equal totalsum
	calculatedTotalSum = spiDict['sum'] + spiDict['PUPAE'] + spiDict['IMAGO']
	if  calculatedTotalSum != spiDict['Sum Total']:
		return "sum + PUPAE + IMAGO = %d but expected %d" % (calculatedTotalSum, spiDict['Sum Total'])
	# If no errors, return None
	return None

if __name__ == '__main__':
	errors = checkDirectory(sys.argv[1])
	