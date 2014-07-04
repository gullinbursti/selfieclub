from django.conf.urls import patterns, url
from media import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns(
    '',
    url(r'^', views.UploadInstructions.as_view())
    )

urlpatterns = format_suffix_patterns(urlpatterns)
