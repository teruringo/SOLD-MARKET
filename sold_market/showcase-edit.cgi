#! /usr/local/bin/perl
# $Id: showcase-edit.cgi 96 2004-03-12 12:25:28Z mu $

$NOMENU=1;
require './_base.cgi';
GetQuery();

OutError('ïsê≥Ç»åƒÇ—èoÇµÇ≈Ç∑') if $Q{no}eq'';

Lock();
DataRead();
CheckUserPass();

$no=int($Q{no});
$itemno=int($Q{item});
$per=CheckCount(int($Q{per}),0,1,200);
$yen=CheckCount(int($Q{yen}),0,0,$MAX_MONEY);
$price=0;

UseTime($TIME_EDIT_SHOWCASE);

if($no<0 || $no>=$DT->{showcasecount}
|| $itemno<0 || $itemno>$MAX_ITEM
|| ($per<=0 && $yen<=0)
|| $per>200
|| CheckItemFlag($itemno,'noshowcase')
)
{
	OutError('ïsê≥Ç»óvãÅÇ≈Ç∑');
}

$price=0;
if($itemno>0)
{
	OutError('ÇªÇÃÉAÉCÉeÉÄÇÕç›å…ñ≥ÇµÇ≈Ç∑') if !$DT->{item}[$itemno-1];
	$price=$yen!=0 ? $yen : int($ITEM[$itemno]->{price} / 100 * $per);
}
$price=$MAX_MONEY if $price>$MAX_MONEY;

if($itemno && $price)
{
	$ret="íI".($no+1)."Ç…$ITEM[$itemno]->{name}Ç$priceâ~Ç≈í¬óÒ";
	WriteLog(0,$DT->{id},0,$ret,1);
	WriteLog(0,0,0,$DT->{shopname}."Ç≈$ITEM[$itemno]->{name}Ç™$priceâ~Ç…Çƒí¬óÒÇ≥ÇÍÇ‹ÇµÇΩ",1);
}
else
{
	$itemno=0;
	$price=0;
	$ret="íI".($no+1)."Ç÷ÇÃí¬óÒÇÇ‚ÇﬂÇ‹ÇµÇΩ";
	WriteLog(0,$DT->{id},0,$ret,1);
	#if($DT->{showcase}[$no])
	#{
	#	WriteLog(0,0,0,$DT->{shopname}."ÇÃ$ITEM[$DT->{showcase}[$no]]->{name}Ç™ìXì™Ç©ÇÁè¡Ç¶Ç‹ÇµÇΩ",1);
	#}
}

$DT->{showcase}[$no]=$itemno;
$DT->{price}[$no]=$price;

DataWrite();
DataCommitOrAbort();
UnLock();

$disp.=$ret;
OutHTML('í¬óÒíI',$disp);

exit;
