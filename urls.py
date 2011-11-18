from django.conf.urls.defaults import * 
from django.http import HttpResponse
from app import urls
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

def default(request):
  return HttpResponse(u"StudySpaces@Penn. We're working on it. <br/><br/>Questions? Contact us at pennappslabs@gmail.com")

urlpatterns = patterns('',
    # Example:

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
   # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
    # (r'^$', default),
    # for everything else, there's Studyspaces
     (r'^', include(urls)),
  )
