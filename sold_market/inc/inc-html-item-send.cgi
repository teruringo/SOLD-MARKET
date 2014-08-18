# $Id: inc-html-item-send.cgi 96 2004-03-12 12:25:28Z mu $

RequireFile('inc-html-ownerinfo.cgi');

$disp.="<HR>œ”jŠüˆ•ª<BR>";

if(CheckItemFlag($itemno,'notrash'))
{
	$disp.='‚±‚Ì¤•i‚Í”jŠü‚Å‚«‚Ü‚¹‚ñ<br>';
}
else
{
	$disp.=<<STR;
<FORM ACTION="item-send.cgi" $METHOD>
$USERPASSFORM
<INPUT TYPE=HIDDEN NAME=bk VALUE="$Q{bk}">
<INPUT TYPE=HIDDEN NAME=item VALUE="$itemno">
‚±‚Ì¤•i‚ğ
<SELECT NAME=cnt1>
<OPTION VALUE="0" SELECTED>
<OPTION>1
<OPTION>10
<OPTION>100
<OPTION>1000
<OPTION>10000
</SELECT>
$ITEM[$itemno]->{scale}A‚à‚µ‚­‚Í
<INPUT TYPE=TEXT SIZE=5 NAME=cnt2>
$ITEM[$itemno]->{scale}
<INPUT TYPE=SUBMIT VALUE="”jŠü‚·‚é">(ŠÔÁ”ï–³)
</FORM>
STR
	#(ŠÔ${\GetTime2HMS($TIME_SEND_ITEM)}Á”ï)
}

1;
