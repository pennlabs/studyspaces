var OFFSET = 20;

function bookmarkSite(title, url) {
	if (window.sidebar) { // firefox
		window.sidebar.addPanel(title, url, "");
		//window.sidebar.addPanel(unescape(title), unescape(url), "");
	} else if(window.opera && window.print) { // opera
		var elem = document.createElement('a');
		elem.setAttribute('href',url);
		elem.setAttribute('title',title);
		elem.setAttribute('rel','sidebar');
		elem.click();
	}
	else if (document.all)// ie
		window.external.AddFavorite(url, title);
	else
		alert('Bookmarking is easy! Press Ctrl+D to bookmark.');
}

var yellowIcon = "http://maps.google.com/mapfiles/ms/micons/yellow.png";
var redIcon = "http://maps.google.com/mapfiles/ms/micons/red.png";
var blueIcon = "http://maps.google.com/mapfiles/ms/micons/blue.png";
var shadowIcon = "http://maps.google.com/mapfiles/ms/micons/msmarker.shadow.png";

var map;
var markers = [];
var infowindow;

function map_init() {
	var currLat = 39.952259;
	var currLong = -75.197021;
	var latlng = new google.maps.LatLng(currLat, currLong);
	var myOptions = {
		zoom: 15,
		scrollwheel: false,
		center: latlng,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	map = new google.maps.Map(document.getElementById("mapbox"), myOptions);
	infowindow = new google.maps.InfoWindow();
}

function addMarker(lat, lng, name, reservable) {
	var icon = reservable == true ? redIcon : blueIcon;
	var latlng = new google.maps.LatLng(lat, lng);
	var marker = new google.maps.Marker({
		position: latlng,
		title: name,
		icon: icon,
		map: map
	});
	
	marker.set('r', reservable);
	
	var index = markers.length;
	markers.push(marker);
	
	google.maps.event.addListener(marker, 'mouseover', function() { 
		clear_hilights();
		marker.setIcon(yellowIcon);
		// add specific hilight
		$('div[building_num='+index+']').addClass('hilight');
	});
	google.maps.event.addListener(marker, 'mouseout', function() {
		marker.setIcon(icon);
	});
	google.maps.event.addListener(marker, 'click', function() {
		open_infowindow(name, marker);
		$('html, body').animate({
			scrollTop: $('div[building_num='+index+']').offset().top - OFFSET/2
		}, 1000);
	});
}

function open_infowindow(building_name, marker) {
	marker.setIcon(yellowIcon);
	infowindow.close();
	infowindow.setContent(building_name);
	infowindow.open(map, marker);
}
// Deletes all markers in the array by removing references to them
function deleteOverlays() {
	if (markers) {
		for (i in markers) {
			markers[i].setMap(null);
		}
		markers.length = 0;
	}
}

$(function(){
	// slider
	$('#num_slider').slider({
		value: 1,
		min  : 1,
		max  : 15,
		step : 1,
		slide: function( event, ui ) {
			$('#num_label').html(ui.value);
		},
		stop: function( event, ui ) {
			updateRoomKindList();
		}
	});
	
	$("#time_radioset").buttonset();
	
	$("#datepicker").datepicker({
		showOn: "button",
		buttonImage: "media/front-end/images/calendar_icon.png",
		buttonImageOnly: true,
		onClose: function(dateText, inst) {updateRoomKindList();}
	});

	$("#datepicker").datepicker("setDate", new Date());	
});

// geolocation
function get_location() {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(show_map, handle_error);
	} else {
		$("#location_p").html("no native support");
	}
}
function show_map(position) {
	myLat = position.coords.latitude;
	myLong = position.coords.longitude;
	$("#location_p").html(myLat + ", " + myLong);
}
function handle_error(err) {
	if (err.code == 1) {
		$("#location_p").html("did not allow geolocation");
	} else {
		$("#location_p").html("error code "+err.code);
	}
}

function getCurrentDate() {
	var d_names = new Array("Sunday", "Monday", "Tuesday",
		"Wednesday", "Thursday", "Friday", "Saturday");
	
	var m_names = new Array("January", "February", "March", 
		"April", "May", "June", "July", "August", "September", 
		"October", "November", "December");
	
	var d = new Date();
	var curr_day = d.getDay();
	var curr_date = d.getDate();
	
	var sup = get_nth_suffix(curr_date);
	
	var curr_month = d.getMonth();
	var curr_year = d.getFullYear();
	
	return d_names[curr_day] + " " + curr_date + sup + " " + m_names[curr_month] + " " + curr_year;
}
function get_nth_suffix(date) {
	switch (date) {
		case 1:
		case 21:
		case 31:
			return "st";
		case 2:
		case 22:
			return "nd";
		case 3:
		case 23:
			return "rd";
		default:
			return "th";
	}
}

function getCurrentTime() {
	var d = new Date();
	var curr_hour = d.getHours();
	var curr_hour = d.getHours();
	var curr_min = d.getMinutes();
	var ampm;
	if(curr_min < 10) curr_min = "0" + curr_min;
	if(curr_hour < 13) ampm = "AM";
	else ampm = "PM";	
	
	return curr_hour + ":" + curr_min + " " + ampm;
}

var filter_toggle = true;
var filter_body_height;

function toggle_filter() {
	if (filter_toggle) {
		filter_body_height = $("div#filter_body").css('height');
		$("div#filter_body").animate({
			height: '0px',
			marginBottom: '0px'
		}, 500);
		$("#toggle_filter").html("Show Filters");
		filter_toggle = !filter_toggle;
	} else {
		$("div#filter_body").animate({
			height: filter_body_height,
			marginBottom: '20px'
		}, 500);
		$("#toggle_filter").html("Hide Filters");
		filter_toggle = !filter_toggle;
	}
}

function sort_rooms(button) {
	$(".sort_choice").removeClass("selected");
	$(button).addClass("selected");
}

function share_event(id) {
	var url = [];
	// start url string, grab # ppl
	url['roomid'] = id;
	
	// grab date
	url['shr']   = $('#time_shr').val();
	url['smin']  = $('#time_smin').val();
	url['ehr']   = $('#time_ehr').val();
	url['emin']  = $('#time_emin').val();
	url['date']  = Date.parse($('#datepicker').val());
	
	window.open("shareevent?" + array_to_url(url));
}

// there exists problem where you cannot simply hide divs on load
// since when that line is executed, the divs has not loaded yet
// fix by setting .hide to display:none. when we want to display, 
// remove the .hide class then hide it before animating
function toggle_roomlist(div) {
	var theList = $(div).parents(".room").children(".roomlist");
	
	var alreadyOpen = !theList.hasClass("hide");		
	$(".roomlist").addClass("hide");
	if (!alreadyOpen) {
		theList.hide();
		theList.removeClass("hide");
	}
	$(".roomlist.hide").slideUp(200);
	if (!alreadyOpen)
		theList.slideDown(200);
}

// grabs variables from filters and does the ajax call
function updateRoomKindList() {
	// deletes all markers from map
	deleteOverlays();
	
	var url = [];
	// start url string, grab # ppl
	url['capacity'] = $('#num_slider').slider("value");
	
	// grab options
	if ( $('input:checkbox:checked[name=privacy]').val() != undefined )
		url['private'] = '1';
	if ( $('input:checkbox:checked[name=whiteboard]').val() != undefined )
		url['whiteboard'] = '1';
	if ( $('input:checkbox:checked[name=computer]').val() != undefined )
		url['computer'] = '1';
	if ( $('input:checkbox:checked[name=monitor]').val() != undefined )
		url['monitor'] = '1';
		
	// grab date
	url['shr']   = $('#time_shr').val();
	url['smin']  = $('#time_smin').val();
	url['ehr']   = $('#time_ehr').val();
	url['emin']  = $('#time_emin').val();
	url['date'] = Date.parse($('#datepicker').val());
	
	$("div#roomlist").load('roomlist?' + array_to_url(url));
}

function open_infowindow_by_label(label) {
	clear_hilights();
	var index = $(label).attr('building_num');
	// add specfic hilight
	$(label).addClass('hilight');
	var building_name = $('div[building_num='+index+"] span.buildingname").html();
	open_infowindow(building_name, markers[index]);
}
function array_to_url(array) {
	var key;
	var pairs = [];
	for (key in array) {
		pairs.push(array.hasOwnProperty(key) ? "" + (encodeURIComponent(key)) + "=" + (encodeURIComponent(array[key])) : void 0);
	}
	return pairs.join("&");
};

function clear_hilights() {
	for (i in markers) {
		markers[i].get('r') ? markers[i].setIcon(redIcon) : markers[i].setIcon(blueIcon);
	}
	$('div[building_num]').removeClass('hilight');
}
function hilight_on(label) {
	clear_hilights();
	var index = $(label).attr('building_num');
	markers[index].setIcon(yellowIcon);
	$(label).addClass('hilight');
}

// doc ready
$(document).ready(function () {
	// get current date and time
	$("#time_p").html(getCurrentTime()+"&nbsp;&nbsp;"+getCurrentDate());
	
	// populate time specify values
	var getCurrTimeRound = function(addhours){
		var d = new Date();
		var curr_hour = d.getHours() + addhours;
		var curr_min = d.getMinutes();
		
		var curr_min = Math.ceil(curr_min/15)*15;
		if (curr_min==60) {
			curr_hour++;
			curr_min = 0;
		}
		curr_hour = curr_hour % 24;
		return new Date(0,0,0,curr_hour, curr_min,0,0);
	}

	var timeentry_update = function() {
		var starttime = $('#time_s_entry').timeEntry('getTime');
		var endtime = $('#time_e_entry').timeEntry('getTime');
	  
		$('#time_shr').val(starttime.getHours());
		$('#time_ehr').val(endtime.getHours());
		$('#time_smin').val(starttime.getMinutes());
		$('#time_emin').val(endtime.getMinutes());
		updateRoomKindList();
	};

	var timeentry_s_change = function() {
		var starttime = $('#time_s_entry').timeEntry('getTime');
		var endtime = new Date(starttime.getTime() + 3600000);
		$('#time_e_entry').timeEntry('setTime', endtime);
	}

	var customRange = function(input) {
		if (input.id == 'time_s_entry') {
			return {minTime: null, maxTime: null};
		} else if (input.id == 'time_e_entry') {
			return {minTime: $('#time_s_entry').timeEntry('getTime'), maxTime: null};
		}
	}
	 
	$('#time_s_entry').timeEntry({spinnerImage:'', beforeShow: customRange}).timeEntry('setTime', getCurrTimeRound(0)).blur(timeentry_update).change(timeentry_s_change);
	$('#time_e_entry').timeEntry({spinnerImage:'', beforeShow: customRange}).timeEntry('setTime', getCurrTimeRound(1)).blur(timeentry_update);
	
	var top = $('#main').position().top;
	var threshold = top + OFFSET;
	
	$(window).resize(function() {
		if ($('#rightColumn').css('position') == 'fixed') {
			var tmp_top = $('#rightColumn').offset().top;
			$('div#rightColumn').removeClass('fixed');
			$('div#rightColumn').css('left', 0);
			$('div#rightColumn').css('top', tmp_top - threshold- OFFSET);
			console.log($('div#rightColumn').css('top'));
		}
	});
	
	console.log(threshold);
	
	$(window).scroll(function () {
		var scrolled = $(this).scrollTop();
		var top = $('#main').position().top;
		if (top < scrolled) {
			$('div#rightColumn').animate({top: scrolled - top},100);
		}
		else if (top >= scrolled) {
			$('div#rightColumn').animate({top: 0},1.0);
		}
	});
 
	// check cookie for top notifybar
	if ($.cookie('studyspaces_visited')) {
		$('#notifybar').hide();
	}
	
	// get geolocation
	//get_location();
	map_init();
	
	// updates time entries
	// also does initial ajax call to update roomlist
	timeentry_update();
});