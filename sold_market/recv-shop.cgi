#! /usr/local/bin/perl
# $Id: recv-shop.cgi 96 2004-03-12 12:25:28Z mu $

require './_base.cgi';

Error('DISNABLED MOVE-TOWN') if !$MOVETOWN_ENABLE;
Error('NOT SET $TOWN_CODE') if !$TOWN_CODE;

Error("NOT POST") if $ENV{REQUEST_METHOD} ne "POST";
read(STDIN,$query,$ENV{CONTENT_LENGTH});

$townmaster=ReadTown($TOWN_CODE,1);
Error("NO OWN TOWN") if !$townmaster;

#debug open(OUT,">$DATA_DIR/recvshop.cgi");
#print OUT $query."\n";
#close(OUT);

my @buffer=split(/\n/,$query);

#ˆÚ“]Œ³‚ÌŠXî•ñ‚ðŽæ“¾•³“–«ƒ`ƒFƒbƒN
$towncode=shift(@buffer);
$TOWN=ReadTown($towncode);
Error("NOT ALLOW TOWN $towncode") if !$TOWN;
Error("NOT ALLOW ADDR $towncode $ENV{REMOTE_ADDR}") if $TOWN->{myaddr} ne '' && $ENV{REMOTE_ADDR}!~/$TOWN->{myaddr}/;

#ƒpƒXƒ[ƒhƒ`ƒFƒbƒN
$login=shift(@buffer);
Error("PASSWORD ERROR $towncode $login") if !CheckHash($login,$TOWN->{password});

#“X•Üƒf[ƒ^Žæ“¾
$data=shift(@buffer);
eval("\$DTM=".$data.";");
Error("DATA ERROR $towncode") if $DTM->{name} eq '';

#“X•Üƒf[ƒ^Žæ“¾
$data=shift(@buffer);
eval("\$DTM_STOCK=".$data.";");

#ˆÚ“]Œ³ŠXƒf[ƒ^Žæ“¾
%towndata=split(/\t/,shift(@buffer));
Error("DATA STOCK ERROR $towncode") if $towndata{code} eq '';

#IPŽæ“¾
$trueip=shift(@buffer);

print "Content-type: text/plain\n\n";

Lock();
DataRead();

$DTM->{nocheckip}=0 if $towndata{group} eq '' || $towndata{group} ne $townmaster->{group};

my($result,$detailresult)=CheckShopData($DTM);
if($result eq '')
{
	$DTM->{name}=$DTM->{newname};
	$DTM->{pass}=($PASSWORD_CRYPT ? crypt($DTM->{newpass},GetSalt()) : $DTM->{newpass});
	$DTM->{rankingyesterday}=0;
	$DTM->{boxcount}=0;
	$DTM->{lastlogin}=$NOW_TIME;
	$DTM->{item}=[];
	$DTM->{exp}={};
	$DTM->{itemyesterday}={};
	$DTM->{itemtoday}={};
	my %itemcode2no=();
	my $val;
	foreach my $no (1..$MAX_ITEM)
	{
		my $code=$ITEM[$no]->{code};
		$itemcode2no{$code}=$no;
		next if $code eq '';
		
		$val=GetValue($DTM,$DTM_STOCK,'itemcode',$code,$ITEM[$no]->{limit});
		$DTM->{item}->[$no-1]=$val;
		
		$val=GetValue($DTM,$DTM_STOCK,'expcode',$code,1000);
		$DTM->{exp}->{$no}=$val if $val;
		
		$val=GetValue($DTM,$DTM_STOCK,'itemyesterdaycode',$code);
		$DTM->{itemyesterday}->{$no}=$val if $val;
		
		$val=GetValue($DTM,$DTM_STOCK,'itemtodaycode',$code);
		$DTM->{itemtoday}->{$no}=$val if $val;

		sub GetValue
		{
			my($DTM,$DTM_STOCK,$key,$code,$limit)=@_;
			
			my $val=$DTM->{$key}->{$code}+0;
			foreach(@$DTM_STOCK)
			{
				$val+=$_->{$key}->{$code};
				delete $_->{$key}->{$code};
				delete $_->{$key} if !scalar(%{$_->{$key}});
			}
			if($limit && $val>$limit)
			{
				$DTM->{$key}->{$code}=$val-$limit;
				$val=$limit;
			}
			else
			{
				delete $DTM->{$key}->{$code};
			}
			return $val;
		}
	}
	if($DTM_STOCK->[9]->{town})
	{
		my $stock=$DTM_STOCK->[9];
		# debug $stock->{itemcode}->{yyyy}=123;
		foreach(keys(%{$stock->{itemcode}}))
		{
			$detailresult.=$_."\t".$stock->{itemcode}->{$_}."\t";
		}
		$detailresult="trash=$DTM_STOCK->[9]->{town}\t$detailresult" if $detailresult=~s/\t$//;
	}
	$DTM->{usercode}={};
	if($townmaster->{allowuserdata})
	{
		$DTM->{usercode}=$DTM->{user};
		$DTM->{user}={};
		foreach my $key ((split /,/,$townmaster->{allowuserdata}),(grep /^_so_/,keys %{$DTM->{usercode}}))
		{
			next if $key!~/^_so_/ && $townmaster->{allowuserdata} eq 'none';
			my $found=0;
			foreach my $stock ($DTM,@$DTM_STOCK)
			{
				if(exists $stock->{usercode}{$key})
				{
					$DTM->{user}{$key}=$stock->{usercode}{$key} if !$found++;
					delete $stock->{usercode}{$key};
				}
			}
		}
	}
	unshift(@{$DTM_STOCK},
		{
			'town'				=>"$towncode!$towndata{name}",
			'id'				=>$DTM->{id},
			'itemcode'			=>$DTM->{itemcode},
			'expcode'			=>$DTM->{expcode},
			'itemyesterdaycode'	=>$DTM->{itemyesterdaycode},
			'itemtodaycode'		=>$DTM->{itemtodaycode},
			'usercode'			=>$DTM->{usercode},
		}
	);
	$DTM->{id}='';
	foreach(@$DTM_STOCK)
	{
		$DTM->{id}=$_->{id},last if (split(/!/,$_->{town}))[0] eq $TOWN_CODE;
	}
	$DTM->{id}=$DTnextid if $DTM->{id} eq '' || scalar(grep($_==$DTM->{id},map{$_->{id}}@DT));
	OpenAndCheck(GetPath($SUBDATA_DIR,"$DTM->{name}-s"));
	print OUT "stock=".GetDataTree([@{$DTM_STOCK}[0..9]])."\n";
	close(OUT);
	
	foreach my $idx (0..$DTM->{showcasecount}-1)
	{
		my $itemno=$itemcode2no{$DTM->{showcasecode}->[$idx]}+0;
		$itemno=0 if CheckItemFlag($itemno,'noshowcase');
		$DTM->{price}->[$idx]=0 if !$itemno;
		$DTM->{showcase}->[$idx]=$itemno;
	}
	$DTblockip=$DTM->{remoteaddr};
	#ˆÚ“®‹——£‚É‰ž‚¶‚½ŽžŠÔÁ”ï
	#$DTM->{time}=$NOW_TIME-$MAX_STOCK_TIME if $NOW_TIME-$DTM->{time}>$MAX_STOCK_TIME;
	$DTM->{_MoveTownTime}=GetMoveTownTime($DTM,$townmaster,$TOWN); # ˆÚ“]ŽžŠÔ:•Û‘¶‚³‚ê‚È‚¢ˆêŽž“I‚Èƒpƒ‰ƒ[ƒ^
	EditTime($DTM,-$DTM->{_MoveTownTime});
	
	push(@DT,$DTM);
	$DT=$DTM;
	require "$ITEM_DIR/funcshopin.cgi" if $DEFINE_FUNCSHOPIN;
	my $usetime="";
	$usetime.='/ˆÚ“]ŽžŠÔ'.GetTime2HMS($DTM->{_MoveTownTime})    if $DTM->{_MoveTownTime};
	$usetime.='/—\’èŽžŠÔ'.GetTime2HMS($DTM->{_MoveTownTimeSrc}) if $DTM->{_MoveTownTimeSrc};
	WriteLog(1,0,0,$DTM->{shopname}."‚ª".$TOWN->{name}."‚©‚çˆÚ“]‚µ‚Ä‚«‚Ü‚µ‚½".$usetime,1);
	DataWrite();
	DataCommitOrAbort();
	WriteErrorLog("SUCCESS $towncode ".$DTM->{shopname},$LOG_MOVESHOP_FILE);
	print "OK\n$detailresult\n";
}
else
{
	print "$result\n$detailresult\n";
}
UnLock();

exit;

sub Error
{
	WriteErrorLog($_[0],$LOG_MOVESHOP_FILE);
	exit;
}

sub CheckShopData
{
	my($DT)=@_;
	return('DENY','msg=ˆÚ“]æ‚É‹ó‚«‚ª‚ ‚è‚Ü‚¹‚ñ‚Å‚µ‚½') if scalar(@DT)>=$MAX_MOVE_USER;
	return('DENY','msg=ˆÚ“]æ‚É“¯‚¶–¼‘O(ID)‚Ì“X•Ü‚ª‘¶Ý‚µ‚Ü‚µ‚½') if scalar(grep($_ eq $DT->{newname},map{$_->{name}}@DT));
	return('DENY','msg=ˆÚ“]æ‚É“¯‚¶“X–¼‚Ì“X•Ü‚ª‘¶Ý‚µ‚Ü‚µ‚½') if scalar(grep($_ eq $DT->{shopname},map{$_->{shopname}}@DT));
	return('DENY','msg=ˆÚ“]æ‚É‘¶Ý‚µ‚È‚¢ƒMƒ‹ƒh‚ÉŠ‘®‚µ‚Ä‚¢‚Ü‚·') if $DT->{guild} ne '' && !scalar(grep($_ eq $DT->{guild},keys(%GUILD)));
	return('DENY','msg=d•¡“o˜^‹^˜f‚É‚æ‚éˆÚ“]§ŒÀ‚Å‚·') if $townmaster->{blocksameip} ne '' && !$DT->{nocheckip} && scalar(GetIPList($trueip));
	return('DENY','msg=Ž‘‹à‚ª‘«‚è‚Ü‚¹‚ñ') if $townmaster->{allowmoney} ne '' && $townmaster->{allowmoney}>$DT->{money}+$DT->{moneystock};
	return('DENY','msg=Ž‘‹à‚ª‘½‚·‚¬‚Ü‚·') if $townmaster->{denymoney}  ne '' && $townmaster->{denymoney}<$DT->{money}+$DT->{moneystock};
	return('DENY','msg=ƒMƒ‹ƒh§ŒÀ‚Å‚·')   if $townmaster->{allowguild} ne '' && !scalar(grep($_ eq $DT->{guild},split(/[^\w]+/,$townmaster->{allowguild}))) && $DT->{guild} ne '';
	return('DENY','msg=ƒMƒ‹ƒh§ŒÀ‚Å‚·')   if $townmaster->{denyguild}  ne '' && scalar(grep($_ eq $DT->{guild},split(/[^\w]+/,$townmaster->{denyguild}))) && $DT->{guild} ne '';
	return('DENY','msg=ƒgƒbƒv‰ñ”‚ª‘«‚è‚Ü‚¹‚ñ') if $townmaster->{allowtopcount} ne '' && $townmaster->{allowtopcount}>$DT->{rankingcount};
	return('DENY','msg=ƒgƒbƒv‰ñ”‚ª‘½‚·‚¬‚Ü‚·') if $townmaster->{denytopcount}  ne '' && $townmaster->{denytopcount}<$DT->{rankingcount};
	return('DENY','msg=ŠJ‹ÆŠúŠÔ‚ª’Z‚¢‚Å‚·') if $townmaster->{allowfoundation} ne '' && $townmaster->{allowfoundation}>$NOW_TIME-$DT->{foundation};
	return('DENY','msg=ŠJ‹ÆŠúŠÔ‚ª’·‚¢‚Å‚·') if $townmaster->{denyfoundation}  ne '' && $townmaster->{denyfoundation}<$NOW_TIME-$DT->{foundation};
	return('DENY','msg=‚Ç‚ÌƒMƒ‹ƒh‚É‚àŠ‘®‚µ‚Ä‚¢‚Ü‚¹‚ñ') if $townmaster->{onlyguild}  ne '' && $DT->{guild} eq '';
	return('DENY','msg=ƒMƒ‹ƒh‚ÉŠ‘®‚µ‚Ä‚¢‚Ü‚·') if $townmaster->{noguild}  ne '' && $DT->{guild} ne '';
	return('DENY','msg=ˆÚ“]æ‚É‘¶Ý‚µ‚È‚¢E‹Æ‚ÉŠ‘®‚µ‚Ä‚¢‚Ü‚·') if $DT->{job} ne '' && !scalar(grep($_ eq $DT->{job},keys(%JOBTYPE)));
	return('DENY','msg=E‹Æ§ŒÀ‚Å‚·')   if $townmaster->{allowjob} ne '' && !scalar(grep($_ eq $DT->{job},split(/\W+/,$townmaster->{allowjob}))) && $DT->{job} ne '';
	return('DENY','msg=E‹Æ§ŒÀ‚Å‚·')   if $townmaster->{denyjob}  ne '' &&  scalar(grep($_ eq $DT->{job},split(/\W+/,$townmaster->{denyjob}))) && $DT->{job} ne '';
	return('DENY','msg=‚Ç‚ÌE‹Æ‚É‚àA‚¢‚Ä‚¢‚Ü‚¹‚ñ') if $townmaster->{onlyjob}  ne '' && $DT->{job} eq '';
	return('DENY','msg=E‹Æ‚ÉA‚¢‚Ä‚¢‚Ü‚·') if $townmaster->{nojob}  ne '' && $DT->{job} ne '';
	#allowitem=need:tegata:1:’ÊsŽèŒ`
	#denyitem=yakusou:1,po-syon:1
	#allowuserdata=count,count2,string
	
	foreach my $idx (@DTindexnamelist_num)
	{
		return('DENY','msg=“X•Üƒf[ƒ^“à‚É•s³‚Èƒf[ƒ^‚ª‘¶Ý‚µ‚Ü‚·') if $DT->{$idx}=~/[^\d\.\-\+]/;
	}
	
	return "";
}

