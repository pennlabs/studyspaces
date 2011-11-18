import csv
import sys, os
sys.path.append("..")
sys.path.append("../..")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from app.models import Building

"""
Building location upload script.

This takes a CSV file containing lat/long data, and imports it into the
database, i.e. it goes thru every building in the database, looks up 
a building in the CSV with the same name, and takes locations from the
CSV.

The CSV can be edited in a text editor or in Excel. If edited in Excel,
the line endings get messed up, but it can still be used with this 
script and the script will generate a copy with correct line endings. 
"""

def _getCSVRowData(csvrow):
  """ Helper function for CSVRow, returns the storage dictionary. """
  return object.__getattribute__(csvrow, 'data')

class CSVRow(object):
  """ Stores a row of a CSV table. Its fields may be accessed
      using the . operator.""" 
  def __init__(self, initial_data):
    object.__setattr__(self, 'data', initial_data)
  def __repr__(self):
    return str(_getCSVRowData(self))
  def __setattr__(self, name, value):
    _getCSVRowData(self)[name] = value
  def __getattribute__(self, name):
    return _getCSVRowData(self)[name]

def csv_read(filename):
  """ Read a CSV file. Assume the first row in the file is a list of
      column headers. Return (list of columns, list of CSVRows) """
  # rU = read, allow universal line breaks
  csvreader = csv.reader(open(filename, 'rU'), dialect='excel')
  columns = csvreader.next()
  def getrows():
    for line in csvreader:
      yield CSVRow(dict(zip(columns, line)))
  return (columns, list(getrows()))

def csv_write(filename, columns, data):
  csvwriter = csv.writer(open(filename, 'w'))
  csvwriter.writerow(columns)
  for row in data:
    csvwriter.writerow([_getCSVRowData(row).get(col,'') for col in columns])

# read data
(columns, data) = csv_read('buildings.csv')

# write copy of data, with unix line breaks (since the original data is
# probably edited in excel occasionally
csv_write('buildings_out.csv', columns, data)

# read data, generate lookup table based on name.
# data from source TEMP is a placeholder for something we want to put in the db
new_data = {}
fake_database = []
for building in data:
  if building.source != "TEMP":
    new_data[building.name] = building
  else:
    fake_database.append(building)

# modify the lat/long values of all data in the database, based on name.
"""
# test code for when not connected to database.
for db_building in fake_database:
  try:
    new_building = new_data[db_building.name]
    db_building.latitude = new_building.latitude
    db_building.longitude = new_building.longitude
    print db_building
  except KeyError:
    print "FAIL %s" % db_building
"""

for db_building in Building.objects.all():
  try:
    new_building = new_data[db_building.name]
    db_building.latitude = new_building.latitude
    db_building.longitude = new_building.longitude
    print (db_building.name, db_building.latitude, db_building.longitude)
    db_building.save()
  except KeyError:
    print "FAIL %s" % str((db_building.name, db_building.latitude, db_building.longitude))
