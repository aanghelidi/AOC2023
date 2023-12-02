#!/usr/bin/perl
use v5.36;
use List::Util qw( max );

my $ans  = 0; my $ans2 = 0;
open( my $f, "<", $ARGV[0] );
while (<$f>) {
    s/^Game\s\d+: //;
    my @sets     = split( /;\s/, $_ );
    my $possible = 1; my @c_blues; my @c_greens; my @c_reds;
    for my $set (@sets) {
        my @cubes = split( /,\s/, $set );
        my $red = 0; my $blue = 0; my $green = 0;
        for my $cube (@cubes) {
            my @cparts = split( /\s/, $cube );
            $red   += $cparts[0] if grep { $_ eq "red" } @cparts;
            $blue  += $cparts[0] if grep { $_ eq "blue" } @cparts;
            $green += $cparts[0] if grep { $_ eq "green" } @cparts;
        }
        push @c_reds, $red; push @c_blues, $blue; push @c_greens, $green;
        $possible = 0 if $red > 12 || $green > 13 || $blue > 14;
    }
    $ans  += $. if $possible;
    $ans2 += ( max @c_blues ) * ( max @c_reds ) * ( max @c_greens );
}
say "Part 1: $ans";
say "Part 2: $ans2";
