(function() {
  var root;
  root = typeof exports !== "undefined" && exports !== null ? exports : this;
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
  root.map_init = function(latitude, longitude) {
    var latlng, my_options;
    latlng = new google.maps.LatLng(latitude, longitude);
    my_options = {
      zoom: 15,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    return new google.maps.Map(document.getElementById("mapbox"), my_options);
  };
  root.add_marker = function(map, latitude, longitude, reserve_type, building_name) {
    var blue_icon, icon, infowindow, latlng, marker, red_icon;
    red_icon = "http://maps.google.com/mapfiles/ms/micons/red.png";
    blue_icon = "http://maps.google.com/mapfiles/ms/micons/blue.png";
    latlng = new google.maps.LatLng(latitude, longitude);
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
}).call(this);
