# $Id: inc-html-owner.cgi 96 2004-03-12 12:25:28Z mu $

$disp.="œ“X•Üî•ñ<HR>";
$disp.='–¢“ü“X©“®•Â“XŠúŒÀ:'.GetTime2FormatTime($DT->{lastlogin}+$EXPIRE_TIME+GetExpireTimeExtend($DT)).'<br>';
my $tm=$NOW_TIME-$DT->{time};
if($tm<0)
{
	$tm=-$tm;
	$tm='s“®‰Â”\‚Ü‚Å‚ ‚Æ '.GetTime2HMS($tm);
}else{
	if($tm>$MAX_STOCK_TIME){$tm=$MAX_STOCK_TIME;}
	$tm=GetTime2HMS($tm);
}
my $rankmsg=GetRankMessage($DT->{rank});
my($tax,$taxrate)=GetTaxToday($DT);
if($taxrate)
{
	$taxrate="Å—¦:$taxrate\%";
}else{
	$taxrate="–ÆÅ";
}

my $expsum=0;
foreach(values(%{$DT->{exp}})){$expsum+=$_;}
$expsum=int($expsum/10)."%";
my $job=$JOBTYPE{$DT->{job}}; $job||='•s’è';

if(!$MOBILE)
{
	$disp.=$TB;
	$disp.=$TR.$TD."–¼‘O".$TD.$DT->{name}.$TD."“X–¼".$TD.GetTagImgGuild($DT->{guild}).$DT->{shopname}.$TRE;
	$disp.=$TR.$TD."RANK".$TD.($id2idx{$DT->{id}}+1).$TD."TOP".$TD.($DT->{rankingcount}+0)."‰ñ ".GetTopCountImage($DT->{rankingcount}+0).$TRE;
	$disp.=$TR.$TD."l‹C".$TD.$rankmsg.$TD."‘‹à/“ü‹àŒÉ".$TD."\\".$DT->{money}."/\\".$DT->{moneystock}.$TRE;
	$disp.=$TR.$TD."¡Šú”„ã".$TD."\\".$DT->{saletoday}.$TD."‘OŠú”„ã".$TD."\\".$DT->{saleyesterday}.$TRE;
	$disp.=$TR.$TD."¡Šúx•¥".$TD."\\".$DT->{paytoday}.$TD."‘OŠúx•¥".$TD."\\".$DT->{payyesterday}.$TRE;
	$disp.=$TR.$TD."‚¿ŠÔ".$TD.$tm.$TD."“_”".$TD.$DT->{point}.$TRE;
	$disp.=$TR.$TD."¡ŠúˆÛ”ï<BR><SMALL>(ŒˆZ’¥û)</SMALL>".$TD."\\".int($DT->{costtoday})."+\\".$SHOWCASE_COST[$DT->{showcasecount}-1];
	$disp.=    $TD."‘OŠúˆÛ”ï".$TD."\\".$DT->{costyesterday}.$TRE;
	$disp.=$TR.$TD."¡ŠúÅ‹à<BR><SMALL>(ŒˆZ’¥û)</SMALL>".$TD."\\".$tax."<br><small>$taxrate</small>".$TD."‘OŠúÅ‹à".$TD."\\".($DT->{taxyesterday}+0).$TRE;
	$disp.=$TR.$TD."x•¥Ï”„‹pÅ".$TD."\\".($DT->{taxtoday}+0).$TD."Šî–{”„‹pÅ—¦".$TD.GetUserTaxRate($DT).'%'.$TRE;
	$disp.=$TR.$TD."n—û“x‡Œv".$TD.$expsum;
	$disp.=    $GUILD{$DT->{guild}} ? $TD."ƒMƒ‹ƒh‰ï”ï <SMALL>”„ã‚Ì".($GUILD{$DT->{guild}}->[$GUILDIDX_feerate]/10)."%<br>(ŒˆZ’¥û)</SMALL>".$TD.'\\'.int($DT->{saletoday}*$GUILD{$DT->{guild}}->[$GUILDIDX_feerate]/1000) : $TD."@".$TD."@";
	$disp.=  $TRE;
	$disp.=$TR.$TD.'‘n‹Æ'.$TD.GetTime2HMS($NOW_TIME-$DT->{foundation}).$TD.'E‹Æ'.$TD.$job.$TRE;
	$disp.=$TBE;
}
else
{
	$disp.="–¼‘O:".$DT->{name}."<BR>";
	$disp.="“X–¼:".GetTagImgGuild($DT->{guild}).$DT->{shopname}."<BR>";
	$disp.="RANK:".($id2idx{$DT->{id}}+1)."<BR>";
	$disp.="TOP :".($DT->{rankingcount}+0)."‰ñ<BR>";
	$disp.="l‹C:".$rankmsg."<BR>";
	$disp.="‘‹à:"."\\".$DT->{money}."<BR>";
	$disp.="“ü‹à:"."\\".$DT->{moneystock}."<BR>";
	$disp.="¡”„:"."\\".$DT->{saletoday}."<BR>";
	$disp.="‰ï”ï:"."\\".int($DT->{saletoday}*$GUILD{$DT->{guild}}->[$GUILDIDX_feerate]/1000)."<BR>" if $DT->{guild} ne '';
	$disp.="‘O”„:"."\\".$DT->{saleyesterday}."<BR>";
	$disp.="¡•¥:"."\\".$DT->{paytoday}."<BR>";
	$disp.="‘O•¥:"."\\".$DT->{payyesterday}."<BR>";
	$disp.="¡ˆÛ:"."\\".int($DT->{costtoday})."+\\".$SHOWCASE_COST[$DT->{showcasecount}-1]."<BR>";
	$disp.="‘OˆÛ:"."\\".$DT->{costyesterday}."<BR>";
	$disp.="ÏÅ:"."\\".($DT->{taxtoday}+0)."<BR>";
	$disp.="¡Å:"."\\".$tax."(".$taxrate.")<BR>";
	$disp.="‘OÅ:"."\\".($DT->{taxyesterday}+0)."<BR>";
	$disp.="ŠÔ:".$tm."<BR>";
	$disp.="“_”:".$DT->{point}."<BR>";
	$disp.="n—û:".$expsum."<BR>";
	$disp.="‘n‹Æ:".GetTime2HMS($NOW_TIME-$DT->{foundation})."<BR>";
	$disp.="E‹Æ:".$job."<BR>";
}

1;
