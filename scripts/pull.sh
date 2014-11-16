#!/bin/bash
# get latest version and make sure things are good
git pull
# reasonably, and with luck, some sort of tests go here
python manage.py syncdb
sudo service apache2 restart
