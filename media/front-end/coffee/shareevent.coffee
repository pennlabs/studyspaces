# creates global functions to be used in other scripts by appending to the window
# for a more indepth analysis of global vars in coffeescript, read http://stackoverflow.com/questions/4214731/coffeescript-global-variables
root = exports ? this
# document ready, initialize page
root.page_init = (epoch, shr, smin, ehr, emin, latitude, longitude, reserve_type, building_name, room_name, shorturl) ->
  d_names = new Array("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
  m_names = new Array("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
  d = new Date(epoch)
  day = d.getDay()
  date = d.getDate()
  suffix = get_nth_suffix(date)
  month = d.getMonth()
  year = d.getFullYear()
  # format date string to pass into Google Calendar
  # this date is in the format YYYYMMDDTHHMMSS (ex. 20111201T110000 for December 1, 2011 at 11:00:00 AM)
  # month is incremented by 1 because month is zero-indexed
  sdate_string_google = year + num_to_str(month + 1) + num_to_str(date) + "T" + num_to_str(shr) + num_to_str(smin) + "00"
  edate_string_google = year + num_to_str(month + 1) + num_to_str(date) + "T" + num_to_str(ehr) + num_to_str(emin) + "00"
  # format date string
  date_string = d_names[day] + " " + " " + m_names[month] + " " + date + suffix + ", " + year
  $("p#date").html date_string
  # format start time
  sampm = (if shr >= 12 then "PM" else "AM")
  shr = (if shr > 12 then shr - 12 else shr)
  # format end time
  eampm = (if ehr >= 12 then "PM" else "AM")
  ehr = (if ehr > 12 then ehr - 12 else ehr)
  time_string = shr + ":" + num_to_str(smin) + " " + sampm + " - " + ehr + ":" + num_to_str(emin) + " " + sampm
  $("p#time").html time_string
  # check cookie for top notifybar
  $("#notifybar").hide()  if $.cookie("studyspaces_visited")
  map_init latitude, longitude, reserve_type, building_name
  # adds events to Google Calendar with new window
  root.calendar = ->
    dates = sdate_string_google + "Z/" + edate_string_google + "Z"
    loc = building_name + " - " + room_name
    details = "Details at: " + shorturl + "%0A%0AEvent created via pennstudyspaces.com"
    window.open "http://www.google.com/calendar/event?action=TEMPLATE&text=Study Session" + "&dates=" + dates + "&details=" + details + "&location=" + loc, 'Google Calendar', 'height=700,width=900,scrollbars=yes,resizable=yes'

num_to_str = (num) ->
  return "0" + num  if num < 10
  "" + num
# Google Maps
map_init = (latitude, longitude, reserve_type, building_name) ->
  blue_icon = "http://maps.google.com/mapfiles/ms/micons/blue.png"
  red_icon = "http://maps.google.com/mapfiles/ms/micons/red.png"
  latlng = new google.maps.LatLng(latitude, longitude)
  my_options =
    zoom: 15
    center: latlng
    mapTypeId: google.maps.MapTypeId.ROADMAP

  map = new google.maps.Map(document.getElementById("mapbox"), my_options)
  icon = (if (reserve_type isnt "N") then red_icon else blue_icon)
  marker = new google.maps.Marker(
    position: latlng
    title: building_name
    icon: icon
    map: map
  )
# gets the suffix of a date
get_nth_suffix = (date) ->
  switch date
    when 1, 21, 31 then "st"
    when 2, 22 then "nd"
    when 3, 23 then "rd"
    else "th"

# bookmark site
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
# utility function to select text
root.select_text = (element) ->
  text = element
  if $.browser.msie
    range = document.body.createTextRange()
    range.moveToElementText text
    range.select()
  else if $.browser.mozilla or $.browser.opera
    selection = window.getSelection()
    range = document.createRange()
    range.selectNodeContents text
    selection.removeAllRanges()
    selection.addRange range
  else if $.browser.safari
    selection = window.getSelection()
    selection.setBaseAndExtent text, 0, text, 1
# Google Analytics
_gaq = _gaq or []
_gaq.push [ "_setAccount", "UA-21029575-2" ]
_gaq.push [ "_trackPageview" ]
(->
  ga = document.createElement("script")
  ga.type = "text/javascript"
  ga.async = true
  ga.src = (if "https:" is document.location.protocol then "https://ssl" else "http://www") + ".google-analytics.com/ga.js"
  s = document.getElementsByTagName("script")[0]
  s.parentNode.insertBefore ga, s
)()
