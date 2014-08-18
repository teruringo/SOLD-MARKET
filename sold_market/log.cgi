#! /usr/local/bin/perl
# $Id: log.cgi 96 2004-03-12 12:25:28Z mu $

$NOITEM=1;
require './_base.cgi';
GetQuery();

DataRead();
CheckUserPass(1);

ReadLog($DT->{id},$Q{lmd}+0,$Q{key},$Q{tgt});
RequireFile('inc-html-log.cgi');

OutHTML('Å‹ß‚Ìo—ˆ–',$disp);
