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

# check data in park notebook sheets
# the headers are Date,Age,Obsr.,small,med.,large,sum,PUPAE,IMAGO,Sum Total
# sum = small + med + large
# Sum Total = sum + pupae + imago


import sys
import os
import csv

PILOT_HEADERS = ['Date', 'Age', 'Obsr.', 'small', 'med.', 'large', 'sum', 'PUPAE', 'IMAGO', 'Sum Total']
STD_HEADERS = ['Date', 'Age', 'Obsr.', 'small', 'med.', 'large', 'sum', 'PUPAE', 'IMAGO', 'Sum Total', 'Dead Imagoes', 'Wt. in grams']
MEAN_HEADERS = ['PER VIAL Age','PER VIAL larvae and pupae Mean','PER VIAL larvae and pupae %','PER VIAL imagoes Mean','PER VIAL imagoes %','PER VIAL total Mean','PER GRAM L & P Mean','PER GRAM Imag. Mean','PER GRAM Total Mean','n']

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
		line_count = csvdata.line_num - 1
	if len(errors) == 0:
		warning = "WARNING: %d lines" % line_count if line_count < 2 else "%d lines" % line_count
		print "%s: OK (%s)" % (os.path.basename(filename), warning)
   	else:
		print "%s: FAILED (%d lines)" % (os.path.basename(filename), line_count)
		for failure in errors:
			print "  Line %d of %s failed check with error: %s" % (failure['line'], os.path.basename(filename), failure['error'])
	return errors

# rows with the 'standard' headers incl. small, med., large
def checkStdRow(dictRow):
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

# Rows with mean values - Per Vial and per gm
def checkMeanRow(dictRow):
	# per vial means
	pvmDict = {k: dictRow[k] for k in ['PER VIAL larvae and pupae Mean','PER VIAL imagoes Mean','PER VIAL total Mean']}
	missingValuesDict = {}
	for k in pvmDict:
		try:
			val = float(pvmDict[k])
		except ValueError:
			val = 0.0
			missingValuesDict[k] = True
		pvmDict[k] = val

	# per vial percentages
	pvpDict = {k: dictRow[k] for k in ['PER VIAL larvae and pupae %','PER VIAL imagoes %']}
	for k in pvpDict:
		try:
			val = float(pvpDict[k])
		except ValueError:
			val = 0.0
			missingValuesDict[k] = True
		pvpDict[k] = val

	# per gram means
	pgDict = {k: dictRow[k] for k in ['PER GRAM L & P Mean','PER GRAM Imag. Mean','PER GRAM Total Mean']}
	for k in pgDict:
		try:
			val = float(pgDict[k])
		except ValueError:
			val = 0.0
			missingValuesDict[k] = True
		pgDict[k] = val

	# in per vial, 'mean larvae and pupae' + 'mean imagoes' should equal 'total mean',
	calculatedPVTotalMean = pvmDict['PER VIAL larvae and pupae Mean'] + pvmDict['PER VIAL imagoes Mean']
	if abs(calculatedPVTotalMean - pvmDict['PER VIAL total Mean']) > 0.05:
		return "PV L&P mean + imagoes Mean = %f but expected %f" % (calculatedPVTotalMean, pvmDict['PER VIAL total Mean'])
	# sum of percentages  should be 100.0
	calculatedPVTotalPercent = pvpDict['PER VIAL larvae and pupae %'] + pvpDict['PER VIAL imagoes %']
	if abs(calculatedPVTotalPercent - 100.0) > 0.05:
		return "PV L&P% + imagoes% = %f but expected %f" % (calculatedPVTotalPercent, 100.0)
	# in per gram, 'L&P Mean' + 'Imag Mean' should equal 'Total Mean'
	calculatedPGTotalMean = pgDict['PER GRAM L & P Mean'] + pgDict['PER GRAM Imag. Mean']
	if abs(calculatedPGTotalMean - pgDict['PER GRAM Total Mean']) > 0.05:
		return "PG L&P Mean + imag. Mean = %f but expected %f" % (calculatedPGTotalMean, pgDict['PER GRAM Total Mean'])
	# If no errors, return None
	return None


def checkRow(dictRow):
	# first simply check the number of rows
	if len(dictRow) != len(PILOT_HEADERS) and len(dictRow) != len(STD_HEADERS) and len(dictRow) != len(MEAN_HEADERS):
		return "wrong number of headers in CSV row"
	# second, see if we have a standard or mean datasheet
	if sorted(PILOT_HEADERS) == sorted(dictRow.keys()):
		return checkStdRow(dictRow)
	elif sorted(STD_HEADERS) == sorted(dictRow.keys()):
		return checkStdRow(dictRow)
   	elif sorted(MEAN_HEADERS) == sorted(dictRow.keys()):
		return checkMeanRow(dictRow)
	else:
		return "Headers in CSV row don't match any template"


if __name__ == '__main__':
	errors = checkDirectory(sys.argv[1])
	