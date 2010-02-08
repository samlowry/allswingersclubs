//to-do: marker “there is something downthere”
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