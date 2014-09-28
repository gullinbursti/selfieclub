from django.conf.urls import patterns, url
from media import views
from rest_framework.urlpatterns import format_suffix_patterns


# 'urlpatterns' is required in order to work.  Dsiabling invalid-name.
urlpatterns = patterns(  # pylint: disable=invalid-name
    '',
    url(r'^', views.UploadInstructions.as_view())
    )

urlpatterns = format_suffix_patterns(urlpatterns)  # noqa # pylint: disable=invalid-name
