from django.conf.urls import include, url, handler404, handler500, handler403, handler400, re_path
from blog import views
from gallery.views import *
from blog.feeds import LatestPostsFeed

from django.urls import path
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework_nested import routers
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings

import djoser
from djoser.urls import authtoken

### Admin ###

admin.site.site_header = 'Anita Francu Art Admin Panel'
admin.site.site_title = 'Anita Francu Art'

### Router Implemenation ###

router = routers.SimpleRouter()
router.register(r'gallery', AlbumListView)
router.register(r'images', AlbumImageListView, basename='images')
router.register(r'users', UsersView, basename='users')
router.register(r'groups', GroupsView, basename='groups')

albums_router = routers.NestedSimpleRouter(router, r'gallery', lookup='gallery')
albums_router.register(r'images', AlbumImageView, basename='gallery-image')

### Error Handling ###
handler404 = PageView.handler404

sitemaps = {
    'post': PostSitemap,
}

urlpatterns = [
    path('', PageView.home_page, name='home'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
	
    path('register', PageView.register_page, name='register_page'),
    path('login', PageView.login_page, name='login_page'),
    path('logout', PageView.logout_page, name='logout_page'),	
	path('about', PageView.about_page, name='about_page'),
	path('contact', PageView.contactView, name='contactView'),
	path('success', PageView.successView, name="successView"),
    path('contribution/', PageView.donation_page, name="donation_page"),
	
	url(r'^search/', AfaSearchView.as_view(), name="search_page"),

    url(r'^gallery/', include('gallery.urls', namespace='gallery')),
    url(r'^blog/', include('blog.urls', namespace='blog')),

    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(albums_router.urls)),
    url(r'^api/v1/auth/', include(djoser.urls.authtoken)),
    url(r'^admin/', admin.site.urls, name='admin_page'),
	#url(r'^static/(?P<path>.*)$', serve), re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    #url(r'^media/(?P<path>.*)$', serve), re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),	
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
	#url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
