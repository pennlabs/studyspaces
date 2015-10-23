from django.conf.urls.defaults import *
from views import *
from django.conf.urls.static import static
from django.conf import settings

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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
(r'^roomlist/(?P<capacity>\d+)/(?P<private>[01])/(?P<whiteboard>[01])/(?P<computer>[01])/(?P<monitor>[01])/$', roomlist)
(r'^roomlist/(?P<capacity>\d+)/(?P<private>[01])/(?P<whiteboard>[01])/(?P<computer>[01])/(?P<monitor>[01])/$', roomlist)
(r'^roomlist/(?P<capacity>\d+)/(?P<private>[01])/$', roomlist)
"""
