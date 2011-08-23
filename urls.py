from django.conf.urls.defaults import *
from django.conf import settings


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^call/', include('call.foo.urls')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.STATIC_PATH}),
	
    (r'^$', 'cloze.index'),
    (r'^distractor/', 'distractor.index'),
    (r'^answer/', 'answer.index'),
        
    # (r'^$', 'call.hello.index')
    # (r'^add/', 'call.add.index'),
    # (r'^list/', 'call.list.index'),


    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
