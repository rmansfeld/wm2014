from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = staticfiles_urlpatterns()

urlpatterns += patterns('',
                        url(r'^admin/', include(admin.site.urls)),
                        url(r'', include('tipgame.urls'))
)

urlpatterns += patterns('django.contrib.auth.views',
                        (r'^accounts/login/$', 'login', {'template_name': 'tipgame/login.html'}),
                        (r'^accounts/logout/$', 'logout_then_login', {'login_url': '/accounts/loggedout/?next=/'}),
                        (r'^accounts/loggedout/$', 'login', {'template_name': 'tipgame/loggedout.html'}))
