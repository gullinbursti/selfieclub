from django.conf.urls import patterns, url
from activity import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns(
    '',
    url(r'^user/$', views.User.as_view()),
    url(r'^user/(?P<id>\d{1,9})/$', views.User.as_view())
    )

urlpatterns = format_suffix_patterns(urlpatterns)
