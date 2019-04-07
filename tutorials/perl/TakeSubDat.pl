#!/usr/bin/perl

    my $filename1 = $ARGV[0]; # SNP names : AGRN.txt
    my $filename2 = $ARGV[1]; # whole data : GiantdatAl.txt

my %snphash = ();

open(my $fh, '<:encoding(UTF-8)', $filename1)
    or die "Could not open file '$filename' $!";

while (my $row = <$fh>) {
    chomp $row;
#    print $row;
    $snphash{$row} = 1;
}

close($fh);

open(my $f2, '<:encoding(UTF-8)', $filename2)
    or die "Could not open file '$filename' $!";

while (my $row = <$f2>) {
    my @list = split / /, $row;

    if( defined($snphash{$list[0]})) {
	print $row;
    }     
}
close($f2)

