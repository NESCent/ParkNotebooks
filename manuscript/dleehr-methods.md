# Methods/Process

## Overview

This project involved the categorization of roughly 1000 scanned pages into groups based on their tabular data format and amount of content per page.  After categorization, the pages were submitted for transcription to Google Drive Spreadsheets via Amazon Mechanical Turk.  The spreadsheets were downloaded, collected, and reports were generated on their accuracy and errors.

The scripts used to automate aspects of this project are available at https://github.com/NESCent/ParkNotebooks.  Wiki documentation on the pilot project is available at https://github.com/NESCent/ParkNotebooks/wiki/Project-Overview.

## 1: Reviewing/evaluating images

The images scanned by Duke Libraries were provided in JPEG format and have been uploaded to the NESCent web server.  I downloaded a copy of the image sets locally to review the data sets.  There were 1093 image files spanning two directories: experiment1 and experiment2.

I sorted through these images visually to determine if they would be suitable for data entry as Amazon MTurk tasks.  As I reviewed each image, I checked to see if it was tabular data and in a repeated format.  1025 of the pages had the same tabular format.  These pages were then reviewed for the amount of data on each page.  Pages with less than 50% of the lines used were categorized as half pages and placed in a folder of half pages.  Sorting the files by file size quickly identified many pages with little content as full content.

21 of the pages had a tabular format that was unlike the other 1025 format.  These data were marked as 'per vial / per gram', or 'mean'.  29 pages did not contain tabular data and were not considered further for transcription.  18 pages found were labled as various computation sheets.  These did not have a uniform format and were not considered further for bulk transcription.

At this point, the usable images were sorted into 6 directories or batches.  Each batch contained images of pages in the same format and with roughly the same amount of data.

    ./experiment1/full
    ./experiment1/half
    ./experiment2/full
    ./experiment2/half
    ./experiment2/mean-full
    ./experiment2/mean-half

Local sorting provided a mechanism to quickly generate a list of the files in each batch.  These lists were stored in text files, with one filename per line.

## 2: Generating template spreadsheets

To request data entry into spreadsheets we would need to generate an empty spreadsheet corresponding to each image.  The images were already public on the NESCent web server, so the links were well known.  

Creating spreadsheets to correspond to the images first required writing a template for each page format: `mean_park_template` and `std_park_template`.  These files were created in Google Drive under the `parknotebooksproject@gmail.com` account.

With the templates created, the generation of the empty spreadsheets was performed with the `copyGoogleDocs.py` script:

`python copyGoogleDocs.py --user [username] --pw [password] --template [empty spreadsheet name] --jpeglist [list of jpeg filenames] --output [csvfile]`

The script expects credentials for a Google account, the file name of the template, a list of JPEG filenames, and the name of an output file.  Upon execution, the script loops over the list of filenames, copies the template to a spreadsheet on Google Drive with the same name as the JPEG file, and records the public URL of the spreadsheet to the output file.  

The output file contains the mapping of JPEG images to spreadsheets in Google Drive, which is suitable for requesting a batch of tasks in Amazon MTurk,

## 3: Requesting MTurk tasks

There were six batches to request.  Three batches contained full pages and three contained half pages.  We set the payment to $1.00 for a full page and $.60 for a half page.  The first batch submitted was the half-pages from experiment 1.  This contained 204 pages.

Batches are submitted with instructions for the task.  There were existing instructions from the pilot project that specified the location of the spreadsheet and gave the worker guidelines for transcribing the data.  I modified these slightly to accommodate the additional/different columns in our pages.

When the task is presented to the worker, it is displayed as an HTML document with variables substituted from our batch files.  So the instructions render as mostly static text, but with a unique spreadsheet link and image link for each task.

The first batch of 204 tasks was completed in roughly 4 hours.  Status of the tasks was monitored through the requester interface.

## 4: Downloading CSV data

Upon completion, I downloaded the spreadsheets to local CSV files.  This was accomplished with the `exportGoogleDocs.py` script.

`python exportGoogleDocs.py --user [username] --pw [password] --sheets [spreadsheet names] --download-dir [download dir]`

Like `copyGoogleDocs.py`, this script requires credentials for a Google account.  It also expects a list of spreadsheet names (similar to the JPEG file names) and a directory where the data should be downloaded.  Upon execution, it saves the content from each named spreadsheet to a CSV file.

## 5: Checking CSV data

Since the tabular data included columns that were sums of other columns, a simple check of the data could be performed automatically.  This check examines the values in each row and reports whether or not the sums are correct.  It is not able to detect errors in the original source or detect missing rows.

The check was performed by the `checkData.py` script.  In the pilot project, a Perl version of this script was used.  I adapted it to Python and continued development to support the per vial / per gram data, and to produce additional reports in CSV format.

`python checkData.py [-v | --verbose] -d /path/to/directory`

Upon reviewing the first batch of half-pages, I discovered some issues to address.  In 14 cases, the worker changed the column names in his/her spreadsheet.  The `checkData.py` script expects these column names to be identical to the template, so these 14 spreadsheets failed the check immediately.  I updated the instructions to clarify that the workers should not change or edit the columns.

After fixing the column names, 95 of the 204 spreadsheets had no detectable errors.  31 spreadsheets had every row fail the check, 2 were empty, and 76 had at least one failure.  The most common source of error was a case where two values (small, med.) were combined into one column, but the worker did not notice this.  Instead, the user entered the value from small/med. into the column for small, then the value for large into the column for med., and the value for sum into the column for med.  The next column (PUPAE) was then entered as the sum.  This error was often detected because the check of `small + med. + large == sum` would fail.  As a result, I updated the instructions in an attempt to make workers aware of this.

We re-submitted the 2 empty spreadsheets for another worker and they were completed.

The remainder of the batches had similar results.  Detailed results are provided in the reports.  The incidence of changing column names was slightly reduced after the changes to the instructions.  However, it was still necessary to fix the column names for some of the spreadsheets, so this was done unilaterally before running `checkData.py`.  

## 6: Approving tasks

We decided to approve tasks for payment if a reasonable effort had been made to enter the data.  With the check scripts and the JPEG scans, it would be possible to fix/reconcile errors.

I decided that spreadsheets with no data entered were not a reasonable effort, and these were rejected.  Rejecting a task sends it back to the pool for another worker to complete, and the original worker does not receive payment.  There were 11 empty spreadsheets that were re-requested

I also decided to reject spreadsheets that were clearly incomplete.  The `checkData.py` script reports the number of rows in each spreadsheet.  A full page of data would contain up to 37 rows, and the smaller "full" pages in the batch would contain 18-20.  I examined any spreadsheets in a full page batch that contained less than 20 rows and compared them to their scanned image counterpart.  There were 5 spreadsheets detected as incomplete that were re-requested.

After completing the download/check/approval of a batch, I repeated steps 3-6 with the remainder of the batches.

