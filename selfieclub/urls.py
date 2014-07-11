from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^media/', include('media.urls')),
    url(r'^activity/', include('activity.urls')),
    url(r'^newsfeed/user/', include('newsfeed_user.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    )
