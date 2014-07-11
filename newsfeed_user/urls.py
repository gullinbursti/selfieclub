from django.conf.urls import patterns, url
from newsfeed_user import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns(
    '',
    url(r'^type/$', views.NewsfeedType.as_view()),
    url(r'^type/(?P<id>\d{1,9})/$', views.NewsfeedType.as_view())
    )

urlpatterns = format_suffix_patterns(urlpatterns)
