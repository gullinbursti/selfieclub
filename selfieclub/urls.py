from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from newsfeed_member import views as newsfeed_member_views
from member import views as member_views
from club import views as club_views
from selfie import views as selfie_views


admin.autodiscover()

router = DefaultRouter()
router.register(r'^selfie', selfie_views.Selfie)
router.register(r'^club', club_views.Club)
router.register(r'^club/type', club_views.ClubType)
router.register(r'^newsfeed/member/type', newsfeed_member_views.NewsfeedType)
router.register(r'^newsfeed/member', newsfeed_member_views.Newsfeed)
router.register(r'^member', member_views.Member)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'^media/', include('media.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    )
