from django.conf.urls import patterns, url
from activity import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns(
    '',
    url(r'^user/(?P<user_id>\d{1,9}/)$', views.User.as_view())
    )

urlpatterns = format_suffix_patterns(urlpatterns)
