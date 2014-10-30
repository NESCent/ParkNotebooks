# Digitizing data from Tribolium competition experiements of Thomas Park

* Michael Wade
* Dan Leehr
* Karen A. Cranston

Department of Biology, Indiana University,  Bloomington, IN 47405

National Evolutionary Synthesis Center, Durham, NC, 27705

abstract
(140 words max)

Mike - add some text introducing Park

The raw data from both the published and unpublished experiments has never been published, and exists only as handwritten data sheets in binders. We describe the digitization of data from two published Park manuscripts. We scanned binder pages, used Amazon Mechanical Turk and Google Spreadsheets to transcribe the scanned tables and developed methods for computational validation of the data entry process.

# Background & Summary

Mike - short introduction to Park and to the experiments

Mike - description of reuse potential

(700 words maximum) An overview of the study design, the assay(s)
performed, and the created data, including any background information
needed to put this study in the context of previous work and the literature.
The section should also briefly outline the broader goals that motivated
the creation of this dataset and the potential reuse value. We also
encourage authors to include a figure that provides a schematic overview
of the study and assay(s) design. This section and the other main
body sections of the manuscript should include citations to the literature
as needed citecite1, cite2. 

#Methods

This section should include detailed text describing the methods used
in the study and assay(s), and the processing steps leading to the
production of the data files, including any computational analyses
(e.g. normalization, image feature extraction). These methods should
be described in enough detail to allow other researchers to interpret
and repeat, if required, the study and assay(s). Authors are encouraged
to cite previous descriptions of the methods under use, but ideally
the methods descriptions should be complete enough for others to understand
and reproduce the methods and processing steps without referring to
associated publications. In principle, fundamentally new methods should
not be presented for the first time in Data Descriptors, and we may
choose to decline publication of a Data Descriptor until any novel
methods or techniques are published in an appropriate research or
methods-focused journal article. 

## Scanned images and data entry spreadsheets
Mike A - details of scanning process

We first scanned the pages using a {need information about scanner from Duke} and saved the as high-resolution JPG images. An initial pilot project scanned 66 pages, followed by a full list of 1093 pages. Using the set of 1093 images, which we sorted visually into images that contained consistent tabular data and those that did not. There were 1046 images containing tabular data in two distinct tabular formats. Of the 1046 tabular images, we sorted into full and partial pages depending on whether the majority of  lines on the binder sheet contained data. Figure 1 contains a sample full page of tabular data that represents the majority of the images. 

The remaining 47 pages either contained a non-standard tabular format, or did not contain tabular data (for example, documentation). These pages were not considered for bulk transcription.

At this point, the usable images were sorted into 6 directories or batches. Each batch contained images of pages from the same experiment, in the same format and with roughly the same amount of data. For each image, we provided a publicly-accessible URL. We then created a template online Google spreadsheet that contained only a single row with the same columns as the tabular data on the scanned pages and set the permissions to "Anyone with the link can edit". For each image that included a table, we used the Google Docs API to copy the template and create a spreadsheet for data entry, saving its URL. We recorded the mapping of image URLs to spreadsheet URLs in a CSV file.

## Digitization with Mechanical Turk
Mechanical Turk is an online marketplace that pairs workers with online tasks (Human Intelligent Tasks, or HITs). We created a HIT template that included the image, a link to the associated online spreadsheet and instructions for doing the data entry. See Figure 2 for the HIT template. By including the image location and spreadsheet location as variables on the HIT template, we could use the AMT bulk creation process to create a separate HIT for each combination of image and associated spreadsheet, based on the mapping CSV file. We then published the HITs, asking workers to enter the numbers from the image into the cells of the spreadsheet. For full pages, we allowed 60 minutes of time and paid $1.00 USD. For half pages, we allowed 45 minutes and paid $0.60 USD. For each submitted batch, all HITs were taken and completed within 1 hour of submission. The average time to complete a full page was 23 minutes and for a half page was 12 minutes.  

We did an initial pilot project to test the workflow, then a full set of two experiments with slight modifications to the initial protocol. 

#Data Records

All data associated with this manuscript is deposited in the Dryad data respository {link to dryad data package}. All scripts used for data processing, as well as additional documentation, is on GitHub at http://github.com/nescent/parknotebooks. All code is licensed under the GPL v. 3 license. All data is released with the CC0 waiver. 

The data includes both the scanned images from the notebooks as well as the comma-separated (csv) files that contain digitized data from the images that follow standard data format. The two files *digguide.csv details the naming scheme of the image files. The majority (1025) of the pages follow a very consistent structure with the following columns:

* Date: the date of the observation, in format MM-DD-YY, where month and day can be either one digit or two.
* Age: the age of the population in days
* Obsr.: the name of the person making the observation
* Larvae (multiple columns): the number of individuals in larval stages, separated by size. Sometimes three columns (small, medium, large) and sometimes two (small  med, large)
* Sum: the sum of the counts in the Larvae columns
* Pupae: the number of individuals in pupal stage
* Imago: the number of individuals in imago state
* Total: the sum of the Sum, Pupae and Imago columns
* Dead Imago: number of dead individuals in imago state
* wt. in grams: total weight of ?? the population?

A smaller set of pages (21) follow a different structure, recording the mean values per vial and per gram:

__Need detail on what these columns are__

* PER VIAL Age
* PER VIAL larvae and pupae Mean
* PER VIAL larvae and pupae %
* PER VIAL imagoes Mean
* PER VIAL imagoes %	
* PER VIAL total Mean
* PER GRAM L & P Mean
* PER GRAM Imag. Mean
* PER GRAM Total Mean
* n

#Technical Validation

To validate accuracy of the data entry, we did not do double-entry but instead relied on features of the data that allowed for internal verification. In both tabular formats, there were columns that were sums of other columns, providing an intrinsic check. In the dated observation data, the 'Sum' and 'Total' columns in each row were sums of other columns. In the mean value data, the 'PER VIAL total Mean' and 'PER GRAM Total Mean' columns in each row were sums of other columns. We wrote a python script that checked that the entered sum was equal to the actual sum of the columns. This script also checked that the files contains the expected number of columns and reported the number of rows, both passing the sum test and failing. In most cases where the sum test failed, the error was in the original data entry on the binder page, not in the transcribed data. The script generated summary reports regarding each page in CSV format as well as detailed per-row errors.

Q: Have the errors been corrected in the final spreadsheets?

#Usage Notes

Mike W - anything for here?

Brief instructions that may help other researchers reuse these dataset.
This is an optional section, but strongly encouraged when helpful
to readers. This may include discussion of software packages that
are suitable for analyzing the assay data files, suggested downstream
processing steps (e.g. normalization, etc.), or tips for integrating
or comparing this with other datasets. If needed, authors are encouraged
to upload code, programs, or data processing workflows as Supplementary
Information, when they may help others analyse the data.

#Acknowledgements
This work was supported by the National Evolutionary Synthesis Center (NESCent), NSF #EF-0905606 

Author contributions: MW provided the notebooks and expert knowledge of the data and experimental lab conditions. KC designed and implemented the pilot experiment. MA scanned the images and provided metadata matching images to notebook pages. DL implemented the full experiment, making improvements to validation protocols. 


#Competing financial interests

The author(s) declare no competing financial interests.

#Figure Legends

Figure 1: Sample scanned notebook page. This page is representative of the standard tabular format submitted to Mechanical Turk for digitization. 

Figure 2: Human Intelligent Task (HIT) template. The template used to generate individual HITs for submission to Amazon Mechanical Turk. 

#Tables

Tables supporting the Data Descriptor. These can provide summary information
(sample numbers, demographics, etc.), but they should generally not
be used to present primary data (i.e. measurements). Tables containing
primary data should be submitted to an appropriate data repository. 

Tables may be provided within the LaTeX document or as separate
files (tab-delimited text or Excel files). Legends, where needed,
should be included here. Generally, a Data Descriptor should have
fewer than ten Tables, but more may be allowed when needed. Tables
may be of any size, but only Tables which fit onto a single printed
page will be included in the PDF version of the article (up to a maximum
of three). 

