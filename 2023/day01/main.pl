#!/usr/bin/perl
use v5.36;

my $ans   = 0;
my $ans2  = 0;
my %numsd = qw(one 1 two 2 three 3 four 4 five 5 six 6 seven 7 eight 8 nine 9);
open( my $f, "<", $ARGV[0] );
while (<$f>) {
    my @nums = $_ =~ /(\d{1})/g;
    $ans += $nums[0] . $nums[-1];
    my @nums2 = $_ =~ /(?=(\d{1}|one|two|three|four|five|six|seven|eight|nine))/g;
    my $first = exists $numsd{ $nums2[0] }  ? $numsd{ $nums2[0] }  : $nums2[0];
    my $last  = exists $numsd{ $nums2[-1] } ? $numsd{ $nums2[-1] } : $nums2[-1];
    $ans2 += $first . $last;
}
say "Part 1: $ans";
say "Part 2: $ans2";
