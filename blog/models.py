from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from sorl.thumbnail import ImageField

from django.db.models import Q

# Create your models here.

class ArticleManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) | 
                         Q(body__icontains=query)|
                         Q(slug__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct()
        return qs.filter(status='published')

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset() \
            .filter(status='published')

class Post(models.Model):
    tags = TaggableManager()
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    post_image = models.ImageField(upload_to='media', blank=True)	
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='created')

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    #objects = models.Manager()
    objects = ArticleManager()        
    published = PublishedManager()  # Our custom manager.

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.created.year,
                             self.created.month,
                             self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=40)
    email = models.EmailField()
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'