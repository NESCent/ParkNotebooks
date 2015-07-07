These are the scripts used in the Park Notebooks digitization project.

* add_metadata.py : given the list of filenames and experimental codes, add metadata as per Table 1 in Park 1948
* copyGoogleDocs.py: create new Google Spreadsheets from a template via the Python API for Google Docs.
* checkData.py: validate the csv files based on columns that we know to be sums of other columns
* checkGoogleDocs.py: uses exportGoogleDocs and checkData to validate the Google Spreadsheets
* checkData.pl: original perl script used to validate the csv files, superseded by checkData.py
* concat_replicates.py : given csv file with filenames and metadata (the output from add_metadata.py) concatenates csv files from same experiment
* exportGoogleDocs.py: download the final spreadsheets to local csv files. Currently has hard-coded paths for download. Should take these as command-line args of from config file.

