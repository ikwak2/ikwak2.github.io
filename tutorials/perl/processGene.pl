#!/usr/bin/perl

# ./processGene.pl <MAGMA output> <Folder name>
# will create <Folder name> folder and save results of MAGMA output

my $filename = $ARGV[0];
my $dir = $ARGV[1];
mkdir $dir;
open(my $fh, '<:encoding(UTF-8)', $filename)
    or die "Could not open file '$filename' $!";

my $i = 1;

my $maxlengthgene;
my $maxgname;
$maxlengthgene = 0; 
$maxgname ="temp";

while (my $row = <$fh>) {
    chomp $row;
#    print $i;


    if($i > 2) {
	
	my @list = split /\t/, $row;
	
	my $tofile = $dir."/".$list[0].".txt";
	open (MYFILE, '>', $tofile);
	
	my @list = split /\t/, $row;
	
	for(my $j = 2 ; $j < scalar(@list) ; $j++) {
	    print MYFILE $list[$j];
	    print MYFILE "\n";
	}
	
	if( scalar(@list) > $maxlengthgene ) {
	    $maxlengthgene = scalar(@list);
	    $maxgname = $list[0];
	}
    }
    $i = $i + 1
}

print $maxgname;
print "  ";
print $maxlengthgene;
print "\n";
