from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Album

# feeds functionality
class LatestGalleryFeed(Feed):
    title = 'Anita Francu Art Gallery'
    link = reverse_lazy('gallery:gallery_page')
    description = 'New art in my gallery.'

    def items(self):
        return Album.visible.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.description, 30)
