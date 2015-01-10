from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from newsfeed_member import views as newsfeed_member_views
from member import views as member_views
from club import views as club_views
from status import views as status_views


admin.autodiscover()

# Keep in mind that order is relavant, more exact names should be at the top
ROUTER = DefaultRouter()
ROUTER.register(r'^statusupdate', status_views.StatusUpdateViewSet)
ROUTER.register(r'^statusupdate/(?P<status_update_id>\d+)/children',
                status_views.StatusUpdateChildren)
ROUTER.register(r'^statusupdate/(?P<status_update_id>\d+)/$',
                status_views.StatusUpdateViewSet)
ROUTER.register(r'^statusupdate/(?P<status_update_id>\d+)/voters',
                status_views.StatusUpdateVoters)
ROUTER.register(r'^statusupdate/(?P<status_update_id>\d+)/viewers',
                status_views.StatusUpdateViewers)
ROUTER.register(r'^club/(?P<club_id>\d+)/statusupdates',
                club_views.ClubStatusUpdates)
ROUTER.register(r'^club/labeled/(?P<label>[^/]+)',
                club_views.ClubsWithLabelByLabelName)
ROUTER.register(r'^club/label/name', club_views.ClubLabelByName)
ROUTER.register(r'^club/label', club_views.ClubLabel)
ROUTER.register(r'^club/type', club_views.ClubType)
ROUTER.register(r'^club', club_views.Club)
ROUTER.register(r'^newsfeed/member/type', newsfeed_member_views.NewsfeedType)
ROUTER.register(r'^newsfeed/member', newsfeed_member_views.Newsfeed)
ROUTER.register(r'^member/(?P<member_id>\d+)/clubs',
                member_views.MemberClubs)
ROUTER.register(r'^member', member_views.Member)
ROUTER.register(r'^member/(?P<member_id>\d+)/statusupdates',
                member_views.MemberStatusUpdates)


# 'urlpatterns' is required by Django lib.
urlpatterns = patterns(  # pylint: disable=invalid-name
    '',
    url(r'^', include(ROUTER.urls)),
    url(r'^media/', include('media.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^messaging/', include('messaging.urls'))
    )
