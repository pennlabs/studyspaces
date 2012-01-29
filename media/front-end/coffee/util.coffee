root = exports ? this

# Bookmark Button
root.bookmark_site = (title, url) ->
  if window.sidebar
    window.sidebar.addPanel title, url, ""
  else if window.opera and window.print
    elem = document.createElement("a")
    elem.setAttribute "href", url
    elem.setAttribute "title", title
    elem.setAttribute "rel", "sidebar"
    elem.click()
  else if document.all
    window.external.AddFavorite url, title
  else
    alert "Bookmarking is easy! Press Ctrl+D to bookmark."

# Google Maps
root.map_init = (latitude, longitude) ->
  latlng = new google.maps.LatLng(latitude, longitude)
  my_options = (
    zoom: 15
    center: latlng
    mapTypeId: google.maps.MapTypeId.ROADMAP
  )
  return new google.maps.Map(document.getElementById("mapbox"), my_options)

root.add_marker = (map, latitude, longitude, reserve_type, building_name) ->
  red_icon = "http://maps.google.com/mapfiles/ms/micons/red.png"
  blue_icon = "http://maps.google.com/mapfiles/ms/micons/blue.png"
  latlng = new google.maps.LatLng(latitude, longitude)
  icon = (if (reserve_type isnt "N") then red_icon else blue_icon)
  marker = new google.maps.Marker(
    position: latlng
    title: building_name
    icon: icon
    map: map
  )
  infowindow = new google.maps.InfoWindow(
    content: building_name,
    size: new google.maps.Size(50,50)
  )
  google.maps.event.addListener(marker, "click", ->
    infowindow.open(map, marker))
