from django.conf.urls.defaults import *
from views import *
urlpatterns = patterns('',
  (r'^test$', show_all_available),
  (r'^logtest$', log_test),
  (r'^$', index),
  (r'^beta$', index),
  (r'^roomlist$', roomlist),
  (r'^api$', roomlist),
  (r'^availability$', availability_display),
  (r'^deeplink$', deeplink),
  (r'^shareevent', shareevent)
)

"""
(r'^roomlist/(?P<capacity>\d+)/(?P<private>[01])/(?P<whiteboard>[01])/(?P<computer>[01])/(?P<monitor>[01])/$', roomlist)
(r'^roomlist/(?P<capacity>\d+)/(?P<private>[01])/(?P<whiteboard>[01])/(?P<computer>[01])/(?P<monitor>[01])/$', roomlist)
(r'^roomlist/(?P<capacity>\d+)/(?P<private>[01])/$', roomlist)
"""
