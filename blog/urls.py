from . import views
from .feeds import LatestPostsFeed

from django.urls import path
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),

    # showing post by tags
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),

    # path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<slug:post>/', views.post_detail, name='post_detail'),

    path('<int:post_id>/share/', views.post_share, name='post_share'),
]

