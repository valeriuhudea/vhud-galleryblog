import uuid
from django.db import models
from django.utils.text import slugify
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from taggit.managers import TaggableManager
from sorl.thumbnail import ImageField

from django.contrib.postgres.search import SearchVectorField
from django.conf import settings
from django.db.models import Q

#from .custom_storages import MediaStorage

User._meta.get_field('email')._unique = True

class VisibleManager(models.Manager):
    def get_queryset(self):
        return super(VisibleManager,
                     self).get_queryset() \
            .filter(visibility='visible')
			
class AvailableManager(models.Manager):
    def get_queryset(self):
        return super(AvailableManager,
                     self).get_queryset() \
            .filter(availability='available')


class AlbumManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) | 
                         Q(description__icontains=query)|
                         Q(slug__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct()
        return qs.filter(visibility='visible')


class AlbumImageManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(name__icontains=query) | 
                         Q(price__icontains=query)|
                         Q(description__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs		

class ClientMessage(models.Model):
    name = models.CharField(max_length=100, help_text="Sender Name")
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
	
    class Meta:
        verbose_name_plural = "ClientMessage"
		
    def __str__(self):
        return self.name + "-" +  self.email	

class Album(models.Model):
    tags = TaggableManager(blank=True)
    VISIBLE_CHOICES = (
        ('hidden', 'Hidden'),
        ('visible', 'Visible'),
    )
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)	
    description = models.TextField(max_length=1024, blank=True, null=True)
    thumbnail = ProcessedImageField(upload_to='media', processors=[ResizeToFit(300)], format='JPEG', options={'quality': 90}, blank=True)	
    visibility = models.CharField(max_length=10, choices=VISIBLE_CHOICES, default='hidden')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified', )

    def __str__(self):
        return self.title

    #objects = models.Manager()
    objects = AlbumManager()	
    visible = VisibleManager()

    def get_absolute_url(self):
        return reverse('gallery:gallery_detail', args=[self.slug])
	
#    def get_absolute_url(self):
#        return reverse('album', kwargs={'slug':self.slug})	

class AlbumImage(models.Model):
    AVAILABLE_CHOICES = (
        ('unavailable', 'Unavailable'),
        ('available', 'Available'),
		('sold', 'Sold'),
    )
    name = models.CharField(max_length=60)
    image = ProcessedImageField(upload_to='media', processors=[ResizeToFit(1280)], format='JPEG', options={'quality': 90})
    thumbnail = ProcessedImageField(upload_to='media', processors=[ResizeToFit(300)], format='JPEG', options={'quality': 80}, null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.PROTECT, blank=True, null=True)
    alt = models.CharField(max_length=255, default=uuid.uuid4)
    description = models.TextField(max_length=1024, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    slug = models.SlugField(max_length=70, default=uuid.uuid4, editable=False)
    availability = models.CharField(max_length=12, choices=AVAILABLE_CHOICES, default='Unavailable')	
    price = models.IntegerField(default=0, blank=True, null=True)
	
    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.name

    #objects = models.Manager()		
    objects = AlbumImageManager()	
    available = AvailableManager()
    
    @property
    def get_absolute_image_url(self):
        return "{0}{1}".format(settings.STATIC_URL, self.image)

#    def get_absolute_url(self):
#        return reverse('gallery:gallery_detail', args=[self.slug])
