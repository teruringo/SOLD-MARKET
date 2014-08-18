# $Id: inc-html-moneystock.cgi 96 2004-03-12 12:25:28Z mu $

RequireFile('inc-html-ownerinfo.cgi');

$disp.="œ“ü‹àˆ—<HR>";

if($Q{conf}ne'' && $errormsg eq '' && $money>0 && $money<=$DT->{moneystock})
{
	$disp.="“ü‹àŠzF\\".$money."<br>Á”ïŠÔ ".GetTime2HMS(GetTimeDeal($money))."<br>";
	$disp.=<<"HTML";
	<FORM ACTION="moneystock.cgi" $METHOD>
	$USERPASSFORM
	<INPUT TYPE=HIDDEN NAME=money VALUE="$money">
	<INPUT TYPE=SUBMIT NAME=ok VALUE="“ü‹àó—">
	<INPUT TYPE=SUBMIT VALUE="æ‚èÁ‚µ">
	</FORM>
HTML
}
else
{
	my $maxmoney=$DT->{moneystock};
	my $usetime=GetTimeDeal($maxmoney)-$TIME_SEND_MONEY;
	my $stocktime=GetStockTime($DT->{time})-$TIME_SEND_MONEY;
	$maxmoney=0 if $stocktime<0;
	$maxmoney=int($maxmoney/$usetime*$stocktime) if $usetime>0 && $stocktime>0 && $stocktime<$usetime;

	$disp.=<<"HTML";
	<FORM ACTION="moneystock.cgi" $METHOD>
	$USERPASSFORM$errormsg
	“ü‹àŒÉ‚©‚çˆø‚«o‚·‹àŠz
	<INPUT TYPE=TEXT NAME=money SIZE=10 VALUE="$money">
	<INPUT TYPE=HIDDEN NAME=conf VALUE="conf">
	<INPUT TYPE=SUBMIT VALUE="‹àŠzŒˆ’è">
	</FORM>
	<FORM ACTION="moneystock.cgi" $METHOD>
	$USERPASSFORM
	<INPUT TYPE=HIDDEN NAME=money VALUE="$maxmoney">
	<INPUT TYPE=HIDDEN NAME=conf VALUE="conf">
	<INPUT TYPE=SUBMIT VALUE="Å‘åŠzw’è">
	</FORM>
HTML
	$disp.="(Á”ïŠÔ:".GetTime2HMS($TIME_SEND_MONEY)."{\\$TIME_SEND_MONEY_PLUS‚É‚Â‚«".GetTime2HMS($TIME_SEND_MONEY).")";
}
1;
