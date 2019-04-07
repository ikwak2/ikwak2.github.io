#!/usr/bin/perl

my $filename = $ARGV[0];
my $dir = $ARGV[1];
open(my $fh, '<:encoding(UTF-8)', $filename)
    or die "Could not open file '$filename' $!";

my $i = 1;

while (my $row = <$fh>) {
    chomp $row;
    my $tofile = $dir."/kegg".$i.".txt";
    open (MYFILE, '>', $tofile);

    #    print MYFILE "Bob\n";

    my @list = split /\t/, $row;

    print MYFILE $list[0];
    #    print "\n";

    for(my $j = 1 ; $j < scalar(@list) ; $j++) {
        if( $j != 1 ) {
            print MYFILE "\n";
            print MYFILE $list[$j];
            #       print "\n";
        }
    }
    $i = $i + 1
}
