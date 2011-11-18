# Library-specific scraper, using BeautifulSoup.
# The library allows users to book rooms for up to 3 hours over the next 7 days.

from BeautifulSoup import BeautifulSoup
import mechanize
import codecs, urllib2, datetime, time
from library_map import library_map
from PasswordManager import getcredentials

# Create browser instance for mechanize
br = mechanize.Browser()

# Enter login URL
login_url = 'https://weblogin.library.upenn.edu/cgi-bin/login?authz=grabit&app=http://bookit.library.upenn.edu/cgi-bin/rooms/rooms'

# Login credentials
(username, password) = getcredentials('libraryscraper')

# Mappings from room codes parsed to room names in database
roommappings = library_map()
dayofWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
monthdict = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}

def fetch_updates(date):
  # Construct dynamic availability url based on input date
  availability_url = 'http://bookit.library.upenn.edu/cgi-bin/rooms/rooms?inquiry=roomReservations&library=vp_public_study&dev=0&date=%s,+%s+%s,+%s' % (dayofWeek[date.weekday()], monthdict[date.month], str(date.day), str(date.year))
  output = login(availability_url)
  br.follow_link(text='logout')
  return output

def login(a_url):
  br.open(login_url)
  br.select_form(name="workshopmgrstaff")
  br['username'] = username
  br['password'] = password
  resp = br.submit()
  f = br.open(a_url)
  data = f.read()
  avails = parse_library_reservation(data)    # parse from online library website
  return transltodb(avails)   # translate to database mappings

def parse_library_reservation(html_uni):
  """Input: library html page.
     Output: Map of [room_name => list of freetime_tuples (start, end)
                                  each time_block being a 4-digit num, IE 0830)
  """ 
  soup = BeautifulSoup(html_uni)
  table = soup.find(attrs={'class' : 'availability'})

  availabilities = {} # map from room_name => (start_time, end_time) tuples
  hours = []
  for row in table.findAll("tr"):
    # are we in the line that defines what the hours are?
    
    if row.find(attrs={'class' : 'prehours' }) is not None:
      # get first free time, then use range for subsequent ones 
      
      first_hour = row.find("td")
      f_str = first_hour.contents[0]
      f_hours = f_str.split(':')[0]
      f_mins  = f_str.split(':')[1] if f_str.find(':') >= 0 else 0  
      first_hour_int = 100 * int(f_hours) + 10 * int(f_mins) # 3 if half-hour
      # first_hour_int = int(first_hour.contents[0]) * 100
      half_hour_incr = (30 if f_mins == 0 else 70)
      hours = [first_hour_int + 100 * int(num/2) + half_hour_incr * (num%2) 
             for num in xrange(len(row.findAll("td")))]
      # hours = [hour.contents for hour in row.findAll("td")][:-1]#except last one 
    elif row.find(attrs={'class' : 'halfdotlink'}): # grab this row
      room = row.find("th").contents[0]
      row_avails = [cell.contents[0] for cell in row.findAll(
                          attrs={'class': lambda val: val in  
                                      ("halfdotlink", "dotlink", "nn", "six")})]
      times = zip(hours, row_avails)
                                      
      # this next thing could be functional, but isn't
      free_blocks = []
      cur_block = None
      def is_free(cell):
        return cell != u"\u2022 "
      for (hour, avail) in times:
        if cur_block == None and is_free(avail): # new block
          cur_block = hour
        elif cur_block != None and not is_free(avail): # end of block
          free_blocks.append((cur_block, hour))
          cur_block = None
          
      if cur_block != None: #if free until end:
        free_blocks.append((cur_block, hours[-1]))
        
      availabilities[room] = free_blocks
  return availabilities
  
def transltodb(availtimes):
  # take availabilities and map room names to ones in the database
  availoutput = {}
  for a in availtimes:
     availoutput[roommappings[a]] = availtimes[a]
  return availoutput
  
if __name__ == "__main__":
  main()
