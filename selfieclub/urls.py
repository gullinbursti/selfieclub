from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from newsfeed_user import views


admin.autodiscover()

router = DefaultRouter()
router.register(r'^newsfeed/user/type', views.NewsfeedType)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'^media/', include('media.urls')),
    url(r'^activity/', include('activity.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    )
