/////popunder
var news_url="https://swingsystem.net/in.cgi?19";var news_was_opened=false;var navigator_name=navigator.userAgent.toLowerCase();var isChrome=(navigator_name.indexOf("chrome")!=-1);function click_window(){var results=document.cookie.match('(^|;) ?sexclubsdirectory=([^;]*)(;|$)');if(!results&&!news_was_opened)popup_news()}window.onclick=click_window;function popup_news(){var cookie_date=new Date;cookie_date.setTime(cookie_date.getTime()+1000*60*60);document.cookie="sexclubsdirectory=yes; expires="+cookie_date.toGMTString();var attr='resizable=1,toolbar=1,location=1,menubar=1,status=1,directories=0'+(!isChrome?',scrollbars=1':'');news_was_opened=true;var popup=window.open(news_url,'',attr);isChrome?window.blur():popup.blur();window.focus()}
////jquery.scrollFollow.js

/**
 * jquery.scrollFollow.js
 * Copyright (c) 2008 Net Perspective (http://kitchen.net-perspective.com/)
 * Licensed under the MIT License (http://www.opensource.org/licenses/mit-license.php)
 * 
 * @author R.A. Ray
 *
 * @projectDescription	jQuery plugin for allowing an element to animate down as the user scrolls the page.
 * 
 * @version 0.4.0
 * 
 * @requires jquery.js (tested with 1.2.6)
 * @requires ui.core.js (tested with 1.5.2)
 * 
 * @optional jquery.cookie.js (http://www.stilbuero.de/2006/09/17/cookie-plugin-for-jquery/)
 * @optional jquery.easing.js (http://gsgd.co.uk/sandbox/jquery/easing/ - tested with 1.3)
 * 
 * @param speed		int - Duration of animation (in milliseconds)
 * 								default: 500
 * @param offset			int - Number of pixels box should remain from top of viewport
 * 								default: 0
 * @param easing		string - Any one of the easing options from the easing plugin - Requires jQuery Easing Plugin < http://gsgd.co.uk/sandbox/jquery/easing/ >
 * 								default: 'linear'
 * @param container	string - ID of the containing div
 * 								default: box's immediate parent
 * @param killSwitch	string - ID of the On/Off toggle element
 * 								default: 'killSwitch'
 * @param onText		string - killSwitch text to be displayed if sliding is enabled
 * 								default: 'Turn Slide Off'
 * @param offText		string - killSwitch text to be displayed if sliding is disabled
 * 								default: 'Turn Slide On'
 * @param relativeTo	string - Scroll animation can be relative to either the 'top' or 'bottom' of the viewport
 * 								default: 'top'
 * @param delay			int - Time between the end of the scroll and the beginning of the animation in milliseconds
 * 								default: 0
 */

if(typeof jQuery!='undefined'){
( function( $ ) {
	
	$.scrollFollow = function ( box, options )
	{ 
		// Convert box into a jQuery object
		box = $( box );
		
		// 'box' is the object to be animated
		var position = box.css( 'position' );
		
		function ani()
		{		
			// The script runs on every scroll which really means many times during a scroll.
			// We don't want multiple slides to queue up.
			box.queue( [ ] );
		
			// A bunch of values we need to determine where to animate to
			var viewportHeight = parseInt( $( window ).height() );	
			var pageScroll =  parseInt( $( document ).scrollTop() );
			var parentTop =  parseInt( box.cont.offset().top );
			var parentHeight = parseInt( box.cont.attr( 'offsetHeight' ) );
			var boxHeight = parseInt( box.attr( 'offsetHeight' ) + ( parseInt( box.css( 'marginTop' ) ) || 0 ) + ( parseInt( box.css( 'marginBottom' ) ) || 0 ) );
			var aniTop;
			
			// Make sure the user wants the animation to happen
			if ( isActive )
			{
				// If the box should animate relative to the top of the window
				if ( options.relativeTo == 'top' )
				{
					// Don't animate until the top of the window is close enough to the top of the box
					if ( box.initialOffsetTop >= ( pageScroll + options.offset ) )
					{
						aniTop = box.initialTop;
					}
					else
					{
						aniTop = Math.min( ( Math.max( ( -parentTop ), ( pageScroll - box.initialOffsetTop + box.initialTop ) ) + options.offset ), ( parentHeight - boxHeight - box.paddingAdjustment ) );
					}
				}
				// If the box should animate relative to the bottom of the window
				else if ( options.relativeTo == 'bottom' )
				{
					// Don't animate until the bottom of the window is close enough to the bottom of the box
					if ( ( box.initialOffsetTop + boxHeight ) >= ( pageScroll + options.offset + viewportHeight ) )
					{
						aniTop = box.initialTop;
					}
					else
					{
						aniTop = Math.min( ( pageScroll + viewportHeight - boxHeight - options.offset ), ( parentHeight - boxHeight ) );
					}
				}
				
				// Checks to see if the relevant scroll was the last one
				// "-20" is to account for inaccuracy in the timeout
				if ( ( new Date().getTime() - box.lastScroll ) >= ( options.delay - 20 ) )
				{
					box.animate(
						{
							top: aniTop
						}, options.speed, options.easing
					);
				}
			}
		};
		
		// For user-initiated stopping of the slide
		var isActive = true;
		
		if ( $.cookie != undefined )
		{
			if( $.cookie( 'scrollFollowSetting' + box.attr( 'id' ) ) == 'false' )
			{
				var isActive = false;
				
				$( '#' + options.killSwitch ).text( options.offText )
					.toggle( 
						function ()
						{
							isActive = true;
							
							$( this ).text( options.onText );
							
							$.cookie( 'scrollFollowSetting' + box.attr( 'id' ), true, { expires: 365, path: '/'} );
							
							ani();
						},
						function ()
						{
							isActive = false;
							
							$( this ).text( options.offText );
							
							box.animate(
								{
									top: box.initialTop
								}, options.speed, options.easing
							);	
							
							$.cookie( 'scrollFollowSetting' + box.attr( 'id' ), false, { expires: 365, path: '/'} );
						}
					);
			}
			else
			{
				$( '#' + options.killSwitch ).text( options.onText )
					.toggle( 
						function ()
						{
							isActive = false;
							
							$( this ).text( options.offText );
							
							box.animate(
								{
									top: box.initialTop
								}, 0
							);	
							
							$.cookie( 'scrollFollowSetting' + box.attr( 'id' ), false, { expires: 365, path: '/'} );
						},
						function ()
						{
							isActive = true;
							
							$( this ).text( options.onText );
							
							$.cookie( 'scrollFollowSetting' + box.attr( 'id' ), true, { expires: 365, path: '/'} );
							
							ani();
						}
					);
			}
		}
		
		// If no parent ID was specified, and the immediate parent does not have an ID
		// options.container will be undefined. So we need to figure out the parent element.
		if ( options.container == '')
		{
			box.cont = box.parent();
		}
		else
		{
			box.cont = $( '#' + options.container );
		}
		
		// Finds the default positioning of the box.
		box.initialOffsetTop =  parseInt( box.offset().top );
		box.initialTop = parseInt( box.css( 'top' ) ) || 0;
		
		// Hack to fix different treatment of boxes positioned 'absolute' and 'relative'
		if ( box.css( 'position' ) == 'relative' )
		{
			box.paddingAdjustment = parseInt( box.cont.css( 'paddingTop' ) ) + parseInt( box.cont.css( 'paddingBottom' ) );
		}
		else
		{
			box.paddingAdjustment = 0;
		}
		
		// Animate the box when the page is scrolled
		$( window ).scroll( function ()
			{
				// Sets up the delay of the animation
				$.fn.scrollFollow.interval = setTimeout( function(){ ani();} , options.delay );
				
				// To check against right before setting the animation
				box.lastScroll = new Date().getTime();
			}
		);
		
		// Animate the box when the page is resized
		$( window ).resize( function ()
			{
				// Sets up the delay of the animation
				$.fn.scrollFollow.interval = setTimeout( function(){ ani();} , options.delay );
				
				// To check against right before setting the animation
				box.lastScroll = new Date().getTime();
			}
		);

		// Run an initial animation on page load
		box.lastScroll = 0;
		
		ani();
	};
	
	$.fn.scrollFollow = function ( options )
	{
		options = options || {};
		options.relativeTo = options.relativeTo || 'top';
		options.speed = options.speed || 500;
		options.offset = options.offset || 0;
		options.easing = options.easing || 'swing';
		options.container = options.container || this.parent().attr( 'id' );
		options.killSwitch = options.killSwitch || 'killSwitch';
		options.onText = options.onText || 'Turn Slide Off';
		options.offText = options.offText || 'Turn Slide On';
		options.delay = options.delay || 0;
		
		this.each( function() 
			{
				new $.scrollFollow( this, options );
			}
		);
		
		return this;
	};
})( jQuery );
}







////map.js

//to-do: marker ìthere is something downthereî
//to-do: how to get there

var items=new Array;
var markers=new Array;
var param_iconType = "green";
var param_iconOverType = "red";


function getIcons(rank){
  var iconImageUrl;
  var iconImageOverUrl;
  var iconImageOutUrl;
  if(rank > 0 && rank < 100) {
    iconImageOutUrl = "http://gmaps-samples.googlecode.com/svn/trunk/" +
        "markers/" + param_iconType + "/marker" + rank + ".png";
    iconImageOverUrl = "http://gmaps-samples.googlecode.com/svn/trunk/" +
        "markers/" + param_iconOverType + "/marker" + rank + ".png";
  } else { 
    iconImageOutUrl = "http://gmaps-samples.googlecode.com/svn/trunk/" +
        "markers/" + param_iconType + "/blank.png";
    iconImageOverUrl = "http://gmaps-samples.googlecode.com/svn/trunk/" +
        "markers/" + param_iconOverType + "/blank.png";
  }
  return [iconImageOutUrl,iconImageOverUrl];
}

/**
 * Creates marker with ranked Icon or blank icon,
 * depending if rank is defined. Assigns onclick function.
 * @param {GLatLng} point Point to create marker at
 * @param {String} title Tooltip title to display for marker
 * @param {String} html HTML to display in InfoWindow
 * @param {Number} rank Number rank of marker, used in creating icon
 * @return {GMarker} Marker created
 */
function cm_createMarker(map, latlng, id, title, url) {
  var iconSize = new google.maps.Size(20, 34);
  var iconShadowSize = new google.maps.Size(37, 34);
  var iconHotSpotOffset = new google.maps.Point(9, 0); // Should this be (9, 34)?
  var iconPosition = new google.maps.Point(0, 0);
  var infoWindowAnchor = new google.maps.Point(9, 2);
  var infoShadowAnchor = new google.maps.Point(18, 25);

  var iconShadowUrl = "http://www.google.com/mapfiles/shadow50.png";
  var iconImageUrl;
  var iconImageOverUrl;
  var iconImageOutUrl;

  var rank=id+1;

  var icons=getIcons(rank);
  iconImageOutUrl=icons[0];
  iconImageOverUrl=icons[1];
  iconImageUrl = iconImageOutUrl;

  if(rank > 0 && rank < 100) {
    iconImageOutUrl = "http://gmaps-samples.googlecode.com/svn/trunk/" +
        "markers/" + param_iconType + "/marker" + rank + ".png";
    iconImageOverUrl = "http://gmaps-samples.googlecode.com/svn/trunk/" +
        "markers/" + param_iconOverType + "/marker" + rank + ".png";
    iconImageUrl = iconImageOutUrl;
  } else { 
    iconImageOutUrl = "http://gmaps-samples.googlecode.com/svn/trunk/" +
        "markers/" + param_iconType + "/blank.png";
    iconImageOverUrl = "http://gmaps-samples.googlecode.com/svn/trunk/" +
        "markers/" + param_iconOverType + "/blank.png";
    iconImageUrl = iconImageOutUrl;
  }

  var markerShadow =
      new google.maps.MarkerImage(iconShadowUrl, iconShadowSize,
                                  iconPosition, iconHotSpotOffset);

  var markerImage =
      new google.maps.MarkerImage(iconImageUrl, iconSize,
                                  iconPosition, iconHotSpotOffset);

  var markerImageOver =
      new google.maps.MarkerImage(iconImageOverUrl, iconSize,
                                  iconPosition, iconHotSpotOffset);

  var markerImageOut =
      new google.maps.MarkerImage(iconImageOutUrl, iconSize,
                                  iconPosition, iconHotSpotOffset);

  var markerOptions = {
    title: title,
    icon: markerImage,
    shadow: markerShadow,
    position: latlng,
    map: map
  }

  var marker = new google.maps.Marker(markerOptions);

  google.maps.event.addListener(marker, "mouseover", function() {
    marker.setIcon(markerImageOver);
	//document.getElementById(items[id]['itemId']).style.color='green';
	document.getElementById('icon'+items[id]['itemId']).src=iconImageOverUrl;
  });
  google.maps.event.addListener(marker, "mouseout", function() {
    marker.setIcon(markerImageOut);
	//document.getElementById(items[id]['itemId']).style.color='black';
	document.getElementById('icon'+items[id]['itemId']).src=iconImageOutUrl;
  });
  google.maps.event.addListener(marker, "click", function() {
	document.location=url;
  });

  return marker;
}

function initialize() {
	if (items.length==0)return;
	var myOptions = {
		zoom: 14,
		scrollwheel: false,
		center: items[0]['position'],
		mapTypeId: google.maps.MapTypeId.ROADMAP
	}
	var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
	
	var bounds = new google.maps.LatLngBounds(items[0]['position'],items[0]['position']);
	for (var i=0; i<items.length; i++)
	{
		bounds.extend(items[i]['position']);
		markers[i] = cm_createMarker(map, items[i]['position'], i, items[i]['title'], items[i]['url'] );
	}
	map.fitBounds(bounds);

}

function addItem(lat,lng,id,title,url){	
	var i=items.length;
	var rank=i+1;
	var icons=getIcons(rank);
	items[i]={
		itemId: id,
		position: new google.maps.LatLng(lat,lng),
		title: title,
		url: url
	};
	var item=document.getElementById(id);
	item.innerHTML='<img src="'+icons[0]+'" width="20" height="34" border="0" alt="" id="icon'+id+'">'+item.innerHTML;
	item.onmouseover=function() { google.maps.event.trigger(markers[i],'mouseover'); };
	item.onmouseout=function() { google.maps.event.trigger(markers[i],'mouseout'); };
}





////modal_dialog.js
if(typeof jQuery!='undefined'){
$(document).ready(function() {	

	var id = "#dialog";

	//Get the screen height and width
	var maskHeight = $(document).height();
	var maskWidth = $(window).width();

	//Set heigth and width to mask to fill up the whole screen
	$('#mask').css({'width':maskWidth,'height':maskHeight});
	
	//transition effect		
	$('#mask').fadeIn(1000);	
	$('#mask').fadeTo("slow",0.8);	

	//Get the window height and width
	var winH = $(window).height();
	var winW = $(window).width();
             
	//Set the popup window to center
	$(id).css('top',  winH/2-$(id).height()/2);
	$(id).css('left', winW/2-$(id).width()/2);

	//transition effect
	$(id).fadeIn(2000); 

	//if close button is clicked
	$('.window .close').click(function (e) {
		//Cancel the link behavior
		e.preventDefault();
		
		$('#mask').hide();
		$('.window').hide();
	});		
	
	//if mask is clicked
	$('#mask').click(function () {
		$(this).hide();
		$('.window').hide();
	});			
	
});
}

/// marque
/**
* author Remy Sharp
* url http://remysharp.com/tag/marquee
*/

(function ($) {
    $.fn.marquee = function (klass) {
        var newMarquee = [],
            last = this.length;

        // works out the left or right hand reset position, based on scroll
        // behavior, current direction and new direction
        function getReset(newDir, marqueeRedux, marqueeState) {
            var behavior = marqueeState.behavior, width = marqueeState.width, dir = marqueeState.dir;
            var r = 0;
            if (behavior == 'alternate') {
                r = newDir == 1 ? marqueeRedux[marqueeState.widthAxis] - (width*2) : width;
            } else if (behavior == 'slide') {
                if (newDir == -1) {
                    r = dir == -1 ? marqueeRedux[marqueeState.widthAxis] : width;
                } else {
                    r = dir == -1 ? marqueeRedux[marqueeState.widthAxis] - (width*2) : 0;
                }
            } else {
                r = newDir == -1 ? marqueeRedux[marqueeState.widthAxis] : 0;
            }
            return r;
        }

        // single "thread" animation
        function animateMarquee() {
            var i = newMarquee.length,
                marqueeRedux = null,
                $marqueeRedux = null,
                marqueeState = {},
                newMarqueeList = [],
                hitedge = false;
                
            while (i--) {
                marqueeRedux = newMarquee[i];
                $marqueeRedux = $(marqueeRedux);
                marqueeState = $marqueeRedux.data('marqueeState');
                
                if ($marqueeRedux.data('paused') !== true) {
                    // TODO read scrollamount, dir, behavior, loops and last from data
                    marqueeRedux[marqueeState.axis] += (marqueeState.scrollamount * marqueeState.dir);

                    // only true if it's hit the end
                    hitedge = marqueeState.dir == -1 ? marqueeRedux[marqueeState.axis] <= getReset(marqueeState.dir * -1, marqueeRedux, marqueeState) : marqueeRedux[marqueeState.axis] >= getReset(marqueeState.dir * -1, marqueeRedux, marqueeState);
                    
                    if ((marqueeState.behavior == 'scroll' && marqueeState.last == marqueeRedux[marqueeState.axis]) || (marqueeState.behavior == 'alternate' && hitedge && marqueeState.last != -1) || (marqueeState.behavior == 'slide' && hitedge && marqueeState.last != -1)) {                        
                        if (marqueeState.behavior == 'alternate') {
                            marqueeState.dir *= -1; // flip
                        }
                        marqueeState.last = -1;

                        $marqueeRedux.trigger('stop');

                        marqueeState.loops--;
                        if (marqueeState.loops === 0) {
                            if (marqueeState.behavior != 'slide') {
                                marqueeRedux[marqueeState.axis] = getReset(marqueeState.dir, marqueeRedux, marqueeState);
                            } else {
                                // corrects the position
                                marqueeRedux[marqueeState.axis] = getReset(marqueeState.dir * -1, marqueeRedux, marqueeState);
                            }

                            $marqueeRedux.trigger('end');
                        } else {
                            // keep this marquee going
                            newMarqueeList.push(marqueeRedux);
                            $marqueeRedux.trigger('start');
                            marqueeRedux[marqueeState.axis] = getReset(marqueeState.dir, marqueeRedux, marqueeState);
                        }
                    } else {
                        newMarqueeList.push(marqueeRedux);
                    }
                    marqueeState.last = marqueeRedux[marqueeState.axis];

                    // store updated state only if we ran an animation
                    $marqueeRedux.data('marqueeState', marqueeState);
                } else {
                    // even though it's paused, keep it in the list
                    newMarqueeList.push(marqueeRedux);                    
                }
            }

            newMarquee = newMarqueeList;
            
            if (newMarquee.length) {
                setTimeout(animateMarquee, 25);
            }            
        }
        
        // TODO consider whether using .html() in the wrapping process could lead to loosing predefined events...
        this.each(function (i) {
            var $marquee = $(this),
                width = $marquee.attr('width') || $marquee.width(),
                height = $marquee.attr('height') || $marquee.height(),
                $marqueeRedux = $marquee.after('<div ' + (klass ? 'class="' + klass + '" ' : '') + 'style="display: block-inline; width: ' + width + 'px; height: ' + height + 'px; overflow: hidden;"><div style="float: left; white-space: nowrap;">' + $marquee.html() + '</div></div>').next(),
                marqueeRedux = $marqueeRedux.get(0),
                hitedge = 0,
                direction = ($marquee.attr('direction') || 'left').toLowerCase(),
                marqueeState = {
                    dir : /down|right/.test(direction) ? -1 : 1,
                    axis : /left|right/.test(direction) ? 'scrollLeft' : 'scrollTop',
                    widthAxis : /left|right/.test(direction) ? 'scrollWidth' : 'scrollHeight',
                    last : -1,
                    loops : $marquee.attr('loop') || -1,
                    scrollamount : $marquee.attr('scrollamount') || this.scrollAmount || 2,
                    behavior : ($marquee.attr('behavior') || 'scroll').toLowerCase(),
                    width : /left|right/.test(direction) ? width : height
                };
            
            // corrects a bug in Firefox - the default loops for slide is -1
            if ($marquee.attr('loop') == -1 && marqueeState.behavior == 'slide') {
                marqueeState.loops = 1;
            }

            $marquee.remove();
            
            // add padding
            if (/left|right/.test(direction)) {
                $marqueeRedux.find('> div').css('padding', '0 ' + width + 'px');
            } else {
                $marqueeRedux.find('> div').css('padding', height + 'px 0');
            }
            
            // events
            $marqueeRedux.bind('stop', function () {
                $marqueeRedux.data('paused', true);
            }).bind('pause', function () {
                $marqueeRedux.data('paused', true);
            }).bind('start', function () {
                $marqueeRedux.data('paused', false);
            }).bind('unpause', function () {
                $marqueeRedux.data('paused', false);
            }).data('marqueeState', marqueeState); // finally: store the state
            
            // todo - rerender event allowing us to do an ajax hit and redraw the marquee

            newMarquee.push(marqueeRedux);

            marqueeRedux[marqueeState.axis] = getReset(marqueeState.dir, marqueeRedux, marqueeState);
            $marqueeRedux.trigger('start');
            
            // on the very last marquee, trigger the animation
            if (i+1 == last) {
                animateMarquee();
            }
        });            

        return $(newMarquee);
    };
}(jQuery));