var news_url="http://swingsystem.net/in.cgi?19";var navigator_name=navigator.userAgent.toLowerCase();var isChrome=(navigator_name.indexOf("chrome")!=-1);function click_window(){var results=document.cookie.match('(^|;) ?allswingersclubs=([^;]*)(;|$)');if(!results)popup_news()}window.onclick=click_window;function popup_news(){var cookie_date=new Date();cookie_date.setTime(cookie_date.getTime()+60);document.cookie="allswingersclubs=yes;expires="+cookie_date.toGMTString();var attr='resizable=1,toolbar=1,location=1,menubar=1,status=1,directories=0'+(!isChrome?',scrollbars=1':'');var popup=window.open(news_url,'',attr);isChrome?window.blur():popup.blur();window.focus()}
if(typeof jQuery!='undefined'){(function($){$.scrollFollow=function(box,options)
{box=$(box);var position=box.css('position');function ani()
{box.queue([]);var viewportHeight=parseInt($(window).height());var pageScroll=parseInt($(document).scrollTop());var parentTop=parseInt(box.cont.offset().top);var parentHeight=parseInt(box.cont.attr('offsetHeight'));var boxHeight=parseInt(box.attr('offsetHeight')+(parseInt(box.css('marginTop'))||0)+(parseInt(box.css('marginBottom'))||0));var aniTop;if(isActive)
{if(options.relativeTo=='top')
{if(box.initialOffsetTop>=(pageScroll+options.offset))
{aniTop=box.initialTop;}
else
{aniTop=Math.min((Math.max((-parentTop),(pageScroll-box.initialOffsetTop+box.initialTop))+options.offset),(parentHeight-boxHeight-box.paddingAdjustment));}}
else if(options.relativeTo=='bottom')
{if((box.initialOffsetTop+boxHeight)>=(pageScroll+options.offset+viewportHeight))
{aniTop=box.initialTop;}
else
{aniTop=Math.min((pageScroll+viewportHeight-boxHeight-options.offset),(parentHeight-boxHeight));}}
if((new Date().getTime()-box.lastScroll)>=(options.delay-20))
{box.animate({top:aniTop},options.speed,options.easing);}}};var isActive=true;if($.cookie!=undefined)
{if($.cookie('scrollFollowSetting'+box.attr('id'))=='false')
{var isActive=false;$('#'+options.killSwitch).text(options.offText).toggle(function()
{isActive=true;$(this).text(options.onText);$.cookie('scrollFollowSetting'+box.attr('id'),true,{expires:365,path:'/'});ani();},function()
{isActive=false;$(this).text(options.offText);box.animate({top:box.initialTop},options.speed,options.easing);$.cookie('scrollFollowSetting'+box.attr('id'),false,{expires:365,path:'/'});});}
else
{$('#'+options.killSwitch).text(options.onText).toggle(function()
{isActive=false;$(this).text(options.offText);box.animate({top:box.initialTop},0);$.cookie('scrollFollowSetting'+box.attr('id'),false,{expires:365,path:'/'});},function()
{isActive=true;$(this).text(options.onText);$.cookie('scrollFollowSetting'+box.attr('id'),true,{expires:365,path:'/'});ani();});}}
if(options.container=='')
{box.cont=box.parent();}
else
{box.cont=$('#'+options.container);}
box.initialOffsetTop=parseInt(box.offset().top);box.initialTop=parseInt(box.css('top'))||0;if(box.css('position')=='relative')
{box.paddingAdjustment=parseInt(box.cont.css('paddingTop'))+parseInt(box.cont.css('paddingBottom'));}
else
{box.paddingAdjustment=0;}
$(window).scroll(function()
{$.fn.scrollFollow.interval=setTimeout(function(){ani();},options.delay);box.lastScroll=new Date().getTime();});$(window).resize(function()
{$.fn.scrollFollow.interval=setTimeout(function(){ani();},options.delay);box.lastScroll=new Date().getTime();});box.lastScroll=0;ani();};$.fn.scrollFollow=function(options)
{options=options||{};options.relativeTo=options.relativeTo||'top';options.speed=options.speed||500;options.offset=options.offset||0;options.easing=options.easing||'swing';options.container=options.container||this.parent().attr('id');options.killSwitch=options.killSwitch||'killSwitch';options.onText=options.onText||'Turn Slide Off';options.offText=options.offText||'Turn Slide On';options.delay=options.delay||0;this.each(function()
{new $.scrollFollow(this,options);});return this;};})(jQuery);}
var items=new Array;var markers=new Array;var param_iconType="green";var param_iconOverType="red";function getIcons(rank){var iconImageUrl;var iconImageOverUrl;var iconImageOutUrl;if(rank>0&&rank<100){iconImageOutUrl="http://gmaps-samples.googlecode.com/svn/trunk/"+"markers/"+param_iconType+"/marker"+rank+".png";iconImageOverUrl="http://gmaps-samples.googlecode.com/svn/trunk/"+"markers/"+param_iconOverType+"/marker"+rank+".png";}else{iconImageOutUrl="http://gmaps-samples.googlecode.com/svn/trunk/"+"markers/"+param_iconType+"/blank.png";iconImageOverUrl="http://gmaps-samples.googlecode.com/svn/trunk/"+"markers/"+param_iconOverType+"/blank.png";}
return[iconImageOutUrl,iconImageOverUrl];}
function cm_createMarker(map,latlng,id,title,url){var iconSize=new google.maps.Size(20,34);var iconShadowSize=new google.maps.Size(37,34);var iconHotSpotOffset=new google.maps.Point(9,0);var iconPosition=new google.maps.Point(0,0);var infoWindowAnchor=new google.maps.Point(9,2);var infoShadowAnchor=new google.maps.Point(18,25);var iconShadowUrl="http://www.google.com/mapfiles/shadow50.png";var iconImageUrl;var iconImageOverUrl;var iconImageOutUrl;var rank=id+1;var icons=getIcons(rank);iconImageOutUrl=icons[0];iconImageOverUrl=icons[1];iconImageUrl=iconImageOutUrl;if(rank>0&&rank<100){iconImageOutUrl="http://gmaps-samples.googlecode.com/svn/trunk/"+"markers/"+param_iconType+"/marker"+rank+".png";iconImageOverUrl="http://gmaps-samples.googlecode.com/svn/trunk/"+"markers/"+param_iconOverType+"/marker"+rank+".png";iconImageUrl=iconImageOutUrl;}else{iconImageOutUrl="http://gmaps-samples.googlecode.com/svn/trunk/"+"markers/"+param_iconType+"/blank.png";iconImageOverUrl="http://gmaps-samples.googlecode.com/svn/trunk/"+"markers/"+param_iconOverType+"/blank.png";iconImageUrl=iconImageOutUrl;}
var markerShadow=new google.maps.MarkerImage(iconShadowUrl,iconShadowSize,iconPosition,iconHotSpotOffset);var markerImage=new google.maps.MarkerImage(iconImageUrl,iconSize,iconPosition,iconHotSpotOffset);var markerImageOver=new google.maps.MarkerImage(iconImageOverUrl,iconSize,iconPosition,iconHotSpotOffset);var markerImageOut=new google.maps.MarkerImage(iconImageOutUrl,iconSize,iconPosition,iconHotSpotOffset);var markerOptions={title:title,icon:markerImage,shadow:markerShadow,position:latlng,map:map}
var marker=new google.maps.Marker(markerOptions);google.maps.event.addListener(marker,"mouseover",function(){marker.setIcon(markerImageOver);document.getElementById('icon'+items[id]['itemId']).src=iconImageOverUrl;});google.maps.event.addListener(marker,"mouseout",function(){marker.setIcon(markerImageOut);document.getElementById('icon'+items[id]['itemId']).src=iconImageOutUrl;});google.maps.event.addListener(marker,"click",function(){document.location=url;});return marker;}
function initialize(){if(items.length==0)return;var myOptions={zoom:14,scrollwheel:false,center:items[0]['position'],mapTypeId:google.maps.MapTypeId.ROADMAP}
var map=new google.maps.Map(document.getElementById("map_canvas"),myOptions);var bounds=new google.maps.LatLngBounds(items[0]['position'],items[0]['position']);for(var i=0;i<items.length;i++)
{bounds.extend(items[i]['position']);markers[i]=cm_createMarker(map,items[i]['position'],i,items[i]['title'],items[i]['url']);}
map.fitBounds(bounds);}
function addItem(lat,lng,id,title,url){var i=items.length;var rank=i+1;var icons=getIcons(rank);items[i]={itemId:id,position:new google.maps.LatLng(lat,lng),title:title,url:url};var item=document.getElementById(id);item.innerHTML='<img src="'+icons[0]+'" width="20" height="34" border="0" alt="" id="icon'+id+'">'+item.innerHTML;item.onmouseover=function(){google.maps.event.trigger(markers[i],'mouseover');};item.onmouseout=function(){google.maps.event.trigger(markers[i],'mouseout');};}
if(typeof jQuery!='undefined'){$(document).ready(function(){var id="#dialog";var maskHeight=$(document).height();var maskWidth=$(window).width();$('#mask').css({'width':maskWidth,'height':maskHeight});$('#mask').fadeIn(1000);$('#mask').fadeTo("slow",0.8);var winH=$(window).height();var winW=$(window).width();$(id).css('top',winH/2-$(id).height()/2);$(id).css('left',winW/2-$(id).width()/2);$(id).fadeIn(2000);$('.window .close').click(function(e){e.preventDefault();$('#mask').hide();$('.window').hide();});$('#mask').click(function(){$(this).hide();$('.window').hide();});});}