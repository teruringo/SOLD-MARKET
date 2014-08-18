#! /usr/local/bin/perl
# $Id: buy.cgi 96 2004-03-12 12:25:28Z mu $

$NOMENU=1;
require './_base.cgi';

GetQuery();

DataRead();
CheckUserPass();

($id,$showcase,$mstno)=split('!',$Q{buy},3);
$id=int($id+0);
$showcase=int($showcase+0);

if($id==0)
{
	# sê
	$DTS=GetWholeStore();
}
else
{
	# ˆê”Ê“X
	$DTS=$DT[(CheckUserID($id))[1]];
}

$showcase=CheckShowCaseNumber($DTS,$showcase);
($itemno,$price,$stock)=CheckShowCaseItem($DTS,$showcase);

OutError("’Â—ñ’I‚É‚Í‰½‚à‚ ‚è‚Ü‚¹‚ñ") if !$itemno || !$stock;
OutError("’Â—ñ‚ª•Ï‰»‚µ‚½‚æ‚¤‚Å‚·") if $itemno!=$mstno;
OutError('‚±‚Ì¤•i‚Íw“ü•s‰Â‚Å‚·') if $id && CheckItemFlag($itemno,'nobuy');

RequireFile('inc-html-ownerinfo.cgi');
RequireFile('inc-html-buy.cgi');

OutHTML(($id==0?'sê':$DTS->{shopname}).'‚æ‚èd“ü',$disp);

exit;
