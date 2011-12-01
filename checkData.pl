#!/usr/bin/perl
use strict;
use warnings;
use diagnostics;
use Scalar::Util qw(looks_like_number);

# check data in park notebook sheets
# the headers are Date,Age,Obsr.,small,med.,large,sum,PUPAE,IMAGO,Sum Total
# sum = small + med + large
# Sum Total = sum + pupae + imago

my $input=$ARGV[0];
opendir DIR, $input || die "Cannot open directory $input\n";

my @files = grep { /\.csv$/ } readdir(DIR);
my $nfiles=@files;
print "Found $nfiles input files\n";
if ($nfiles==0) { die "Did not find any input files\n"; }

foreach(@files) {
	my $filename=$_;
	open (FILE,'<',$input.'/'.$filename) || die "cannot open file $filename\n";

	# read whole file
	my @data=<FILE>;
	close FILE;
	my $firstline=shift(@data);

	# check that header row has right number fields
	my @fields=split(/,/,$firstline);
	my $nfields = @fields;
	if ($nfields!=10) { print "$filename: has $nfields fields\n"; next; }
	
	# check each row in file
	my $pass=0;
	my $linenum=2;
	foreach(@data) {
		chomp;
		my $line=$_;
		if ($line) {
			unless(checkData($_)) { 
				print "$filename: fail line $linenum: $_\n";
			}
		}
		++$linenum;
	}
}  # end of foreach(files)

# checks the sums in each row and that values are numeric
sub checkData {
	my $line=shift(@_);
	my $pass=1;
	my @fields=split(/,/,$line);
	my $nfields = @fields;
	if ($nfields < 10) { print "$nfields fields, <10: $line\n"; return 0; }
	my $small = $fields[3];
	my $medium = $fields[4];
	my $large = $fields[5];
	my $sum=$fields[6];
	my $pupae = $fields[7];
	my $imago = $fields[8];
	my $totalsum = $fields[9];
	# small and medium may be combined into one column in some rows
	if ($line=~/,,/) {
		if (!$small) { $small=0; }
		elsif (!$medium) { $medium=0; }
		else { print "unpexpected missing value\n"; return 0; }
	}
	# start the non-numeric check at field 5 because either 3 (small)
	# or 4 (medium) might be blank
	for(my $i = 5; $i < $nfields; $i++) {
		unless (looks_like_number($fields[$i])) { 
			print "field $i, $fields[$i] is not numeric\n";
			return 0;
		}
	}
	unless ($small+$medium+$large==$sum) { $pass=0; }
	unless ($sum+$pupae+$imago==$totalsum) { $pass=0; }
	return $pass;
}