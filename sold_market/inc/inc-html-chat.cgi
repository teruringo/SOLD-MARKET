# $Id: inc-html-chat.cgi 96 2004-03-12 12:25:28Z mu $

my $linemax=$MOBILE?10:$MAX_CHAT_MESSAGE;

my %printed=();

$disp.="Åú$CHAT_TITLE(CHATïó)<HR>";

if(!$GUEST_USER)
{
	$disp.=<<"STR";
	$CHAT_INFO
	<FORM ACTION="$MYNAME" $METHOD>
	$USERPASSFORM
	$errormsg
	<INPUT TYPE=TEXT NAME=msg SIZE=50 VALUE="$Q{msg}">
	<INPUT TYPE=SUBMIT VALUE="èëçû">
	</FORM><HR>
STR
}
else
{
	$disp.="èoìXé“à»äOÇÕâ{óóÇÃÇ›<HR>";
}

$disp.=$TB if !$MOBILE;
foreach(@MESSAGE)
{
	chop;
	my($tm,$mode,$id,$to,$msg,$no)=split(/,/);
	my($message,$sname,$name)=split(/\t/,$msg);
	
	$tm=GetTime2FormatTime($tm);
	if(!$to)
	{
		$sname="<B>ä«óùêl</B>";
		$name ="";
	}
	else
	{
		if(defined($id2idx{$to}))
		{
			my $DT=$DT[$id2idx{$to}];
			$sname=GetTagImgGuild($DT->{guild}).$DT->{shopname};
			$name =$DT->{name};
			$sname="<a href=\"shop.cgi?ds=$to&$USERPASSURL\">".$sname."</a>" if !$printed{$to}++ && !$GUEST_USER;
		}
		else
		{
			$sname="<SMALL>closed</SMALL> ".$sname;
		}
	}
	
	if($MOBILE)
	{
		$disp.=$tm."<BR>".$no.":".$sname.":".$name."<BR>".$message;
		$disp.="<HR SIZE=1>";
	}
	else
	{
		$disp.=$TR.$TD.$tm.$TD.$sname.$TD.$name.$TD.$no.$TD.$message.$TRE;
	}
}
$disp.=$TBE if !$MOBILE;

1;
