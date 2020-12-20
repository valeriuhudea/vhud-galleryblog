from django import template
from ..models import *
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.simple_tag
def total_albums():
    return Album.visible.count()

@register.inclusion_tag('gallery/latest_albums.html')
def show_latest_albums(count=5):
    latest_albums = Album.visible.order_by('-modified')[:count]
    return {'latest_albums': latest_albums}
	
#@register.simple_tag
#def get_most_commented_posts(count=5):
#    return Post.published.annotate(
#        total_comments=Count('comments')
#    ).order_by('-total_comments')[:count]


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()

# custom filter to enable md syntax for gallery albums.
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.filter(name='class_name')
def class_name(value):
    return value.__class__.__name__