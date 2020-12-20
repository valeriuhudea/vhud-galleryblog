from django.urls import path
from .feeds import LatestGalleryFeed
from django.conf.urls import include, url, re_path

from .views import *

app_name = 'gallery'

### URL Output regex ###

urlpatterns = [
	#path('404', PageView.handler404, {'exception': Exception()}),

	path('', gallery_page, name='gallery_page'),
	path('tag/<slug:tag_slug>/', gallery_page, name='gallery_page_by_tag'),
    path('<slug:album>/', gallery_detail, name='gallery_detail'),
    path('<slug:album>/tag/<slug:tag_slug>/', gallery_detail, name='gallery_detail_by_tag'),
    path('<slug:album>/', gallery_detail, name='gallery_detail'),
    path('<slug:image_slug>/artworkdetails', artwork_details, name='artwork_details'),
] 
