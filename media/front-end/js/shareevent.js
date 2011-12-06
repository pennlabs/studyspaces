(function() {
  var array_to_url, get_nth_suffix, map_init, num_to_str, root, _gaq;
  root = typeof exports !== "undefined" && exports !== null ? exports : this;
  root.page_init = function(epoch, shr, smin, ehr, emin, latitude, longitude, reserve_type, building_name, room_name, shorturl) {
    var d, d_names, date, date_string, day, eampm, edate_string_google, m_names, month, sampm, sdate_string_google, suffix, time_string, year;
    d_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    m_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    d = new Date(epoch);
    day = d.getDay();
    date = d.getDate();
    suffix = get_nth_suffix(date);
    month = d.getMonth();
    year = d.getFullYear();
    sdate_string_google = "" + year + (num_to_str(month + 1)) + (num_to_str(date)) + "T" + (num_to_str(shr)) + (num_to_str(smin)) + "00";
    edate_string_google = "" + year + (num_to_str(month + 1)) + (num_to_str(date)) + "T" + (num_to_str(ehr)) + (num_to_str(emin)) + "00";
    date_string = "" + d_names[day] + " " + m_names[month] + " " + date + suffix + ", " + year;
    $("p#date").html(date_string);
    sampm = (shr >= 12 ? "PM" : "AM");
    shr = (shr > 12 ? shr - 12 : shr);
    eampm = (ehr >= 12 ? "PM" : "AM");
    ehr = (ehr > 12 ? ehr - 12 : ehr);
    time_string = "" + shr + ":" + (num_to_str(smin)) + " " + sampm + " - " + ehr + ":" + (num_to_str(emin)) + " " + sampm;
    $("p#time").html(time_string);
    if ($.cookie("studyspaces_visited")) {
      $("#notifybar").hide();
    }
    $("#add_to_cal").hover((function() {
      return $("#cal_button").attr("src", "media/front-end/images/cal_button_hover.png");
    }), function() {
      return $("#cal_button").attr("src", "media/front-end/images/cal_button.png");
    });
    map_init(latitude, longitude, reserve_type, building_name);
    return root.calendar = function() {
      var url;
      url = [];
      url['action'] = "TEMPLATE";
      url['text'] = "Study Session";
      url['dates'] = "" + sdate_string_google + "Z/" + edate_string_google + "Z";
      url['location'] = "" + building_name + " - " + room_name;
      url['details'] = "Details at: " + shorturl + "\n\nEvent created via pennstudyspaces.com";
      return window.open("http://www.google.com/calendar/event?" + (array_to_url(url)), 'Google Calendar', 'height=700,width=900,scrollbars=yes,resizable=yes');
    };
  };
  root.bookmark_site = function(title, url) {
    var elem;
    if (window.sidebar) {
      return window.sidebar.addPanel(title, url, "");
    } else if (window.opera && window.print) {
      elem = document.createElement("a");
      elem.setAttribute("href", url);
      elem.setAttribute("title", title);
      elem.setAttribute("rel", "sidebar");
      return elem.click();
    } else if (document.all) {
      return window.external.AddFavorite(url, title);
    } else {
      return alert("Bookmarking is easy! Press Ctrl+D to bookmark.");
    }
  };
  root.select_text = function(element) {
    var range, selection, text;
    text = element;
    if ($.browser.msie) {
      range = document.body.createTextRange();
      range.moveToElementText(text);
      return range.select();
    } else if ($.browser.mozilla || $.browser.opera) {
      selection = window.getSelection();
      range = document.createRange();
      range.selectNodeContents(text);
      selection.removeAllRanges();
      return selection.addRange(range);
    } else if ($.browser.safari) {
      selection = window.getSelection();
      return selection.setBaseAndExtent(text, 0, text, 1);
    }
  };
  _gaq = _gaq || [];
  _gaq.push(["_setAccount", "UA-21029575-2"]);
  _gaq.push(["_trackPageview"]);
  (function() {
    var ga, s;
    ga = document.createElement("script");
    ga.type = "text/javascript";
    ga.async = true;
    ga.src = ("https:" === document.location.protocol ? "https://ssl" : "http://www") + ".google-analytics.com/ga.js";
    s = document.getElementsByTagName("script")[0];
    return s.parentNode.insertBefore(ga, s);
  })();
  num_to_str = function(num) {
    return (num < 10 ? "0" : "") + num;
  };
  array_to_url = function(array) {
    var key, pairs;
    pairs = [];
    for (key in array) {
      pairs.push(array.hasOwnProperty(key) ? "" + (encodeURIComponent(key)) + "=" + (encodeURIComponent(array[key])) : void 0);
    }
    return pairs.join("&");
  };
  map_init = function(latitude, longitude, reserve_type, building_name) {
    var blue_icon, icon, infowindow, latlng, map, marker, my_options, red_icon;
    blue_icon = "http://maps.google.com/mapfiles/ms/micons/blue.png";
    red_icon = "http://maps.google.com/mapfiles/ms/micons/red.png";
    latlng = new google.maps.LatLng(latitude, longitude);
    my_options = {
      zoom: 15,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("mapbox"), my_options);
    icon = (reserve_type !== "N" ? red_icon : blue_icon);
    marker = new google.maps.Marker({
      position: latlng,
      title: building_name,
      icon: icon,
      map: map
    });
    infowindow = new google.maps.InfoWindow({
      content: building_name,
      size: new google.maps.Size(50, 50)
    });
    return google.maps.event.addListener(marker, "click", function() {
      return infowindow.open(map, marker);
    });
  };
  get_nth_suffix = function(date) {
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
  };
}).call(this);
