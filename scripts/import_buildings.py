print """THIS IS NOT A RUNNABLE SCRIPT. INSTEAD, RUN python manage.py shell
from studyspaces/ and copy in the contents of this script"""
#assumes: an empty database
from app.models import Building 

b_in = open('scripts/buildings_from_registrar_api', 'r')

for line in b_in:
  Building(name=line).save()
  print ".",

print "Buildings imported successfully"

