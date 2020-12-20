from __future__ import unicode_literals
from itertools import chain

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import admin, messages
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpRequest
from django.views.generic import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, BadHeaderError
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import ListView
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib import messages

from taggit.models import Tag
from django.db.models import Count, Q

from rest_framework import status, viewsets, generics, permissions, renderers
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

#from .models import *
from .serializers import *
from .forms import *

from gallery.models import Album, AlbumImage
from blog.models import Post

def gallery_page(request, tag_slug=None):
    object_list = Album.visible.all()
    tags = object_list.order_by('tags__name').values_list('tags__name', flat=True).distinct()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])		
    paginator = Paginator(object_list, 4)
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1) # If page is not an integer, deliver first page.
    except EmptyPage:
        albums = paginator.page(paginator.num_pages) # If page is out of range (e.g.  9999), deliver last page of results.
    return render(request, 'gallery/gallery.html', {'albums': albums, 'tag': tag, 'tags': tags})

def gallery_detail(request, album):
    album = get_object_or_404(Album, slug=album,
                             visibility='visible')

    images = AlbumImage.objects.filter(album=album.id)
	
    # List of similar albums
    post_tags_ids = album.tags.values_list('id', flat=True)
    similar_albums = Album.visible.filter(tags__in=post_tags_ids) \
        .exclude(id=album.id)
    similar_albums = similar_albums.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-created')[:4]
    return render(request, 'gallery/album_detail.html', {'album': album, 'images': images, 'similar_albums': similar_albums})

def artwork_details(request, image_slug):

    album_image = get_object_or_404(AlbumImage, slug=image_slug)

    return render(request, 'gallery/artwork-details.html', {'album_image': album_image})

class AfaSearchView(ListView):
    template_name = 'gallery/search_page.html'
    paginate_by = 10
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        albums = Album.visible.all()
        blogs = Post.published.all()
        queryset_chain = chain(albums, blogs)		
        quertyset_list = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)
		
        if query is not None:
            #painting_results = AlbumImage.objects.search(query)
            album_results = Album.objects.search(query)
            blog_results = Post.objects.search(query)
            queryset_chain = chain(album_results, blog_results)
            quertyset_list = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)            
            self.count = len(quertyset_list)
            return quertyset_list	
        return Album.objects.none() and Post.objects.none()

class PageView():

    def home_page(request):
        object_list = Album.visible.all()
        return render(request, 'gallery/home.html')

    def donation_page(request):
        object_list = Album.visible.all()
        return render(request, 'gallery/donation_page.html')
		
    def handler404(request, exception):
        assert isinstance(request, HttpRequest)
        return render(request, 'handler404.html', None, None, 404)
			
    def about_page(request):

        return render(request, 'gallery/about.html')		

    def contact_page(request):

        return render(request, 'gallery/contact.html')		

    def contactView(request):
        if request.method == 'GET':
            form = ContactForm()
        else:
            form = ContactForm(request.POST)
            to_email_list = ['valzld@protonmail.com', 'valeriu.hudea@gmail.com']
            if form.is_valid():
                form.save()			    
                name = form.cleaned_data['name']
                subject = form.cleaned_data['subject']
                from_email = form.cleaned_data['email']
                contact_message = form.cleaned_data['message']
                message = "Name: " +name + " |" + " Sender's Email: " +from_email + " |" + " Message: " +contact_message
                try:
                    send_mail(subject, message, from_email, to_email_list)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect('successView')
        return render(request, "gallery/contact.html", {'form': form})

    def successView(request):
        return render(request, 'gallery/success.html')
	
    def delete_all_user_orders(username):
        Storage.objects.filter(owner=username).filter(already_ordered=False).delete()
        return True

    def calculate_total_price(username):
        total_prices = ''
        for obj in Storage.objects.filter(added_by=username).filter(already_ordered=False):
            price_all += obj.price
        return total_price

    def register_page(request):
        if not request.user.is_authenticated:
            if request.method == "POST":
                form = RegistrationForm(request.POST)
                if form.is_valid():
                    form.save()
                    username = form.cleaned_data["username"]
                    password = form.cleaned_data["password1"]
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    return redirect("home")
                else:
                    return render(request, 'registration/register.html', {'form': form})
            else:
                form = RegistrationForm()
            context = {"form": form}
            return render(request, 'registration/register.html', context)
        else:
            return redirect("home")

    def login_page(request):
        if not request.user.is_authenticated:
            if request.method == "POST":
                form = UserLoginForm(data=request.POST)
                if form.is_valid():
                    username = form.cleaned_data["username"]
                    password = form.cleaned_data["password"]
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        if next is not None:
                            return redirect("home")
                        else:
                            return redirect("home")
            else:
                form = UserLoginForm()
            context = {"form": form}
            return render(request, 'registration/login.html', context)
        else:
            return redirect("home")

    def logout_page(request):
        if request.user.is_authenticated:
            logout(request)
        return redirect("home")

    #@login_required

    #@staff_member_required

### Api Views ###

class UsersView(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `GET` and `POST` actions for Users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupsView(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `GET` and `POST` actions for Groups.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

######################################

class AlbumImageView(viewsets.ModelViewSet):
    serializer_class = AlbumImageSerializer

    def get_queryset(self):
        return AlbumImage.objects.filter(album=self.kwargs['pk'])

class AlbumListView(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def perform_create(self, serializer):
        serializer.save

class AlbumView(viewsets.ModelViewSet):
    #lookup_field = 'id'
    #permission_classes = [IsOwner]
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()

class AlbumImageListView(viewsets.ModelViewSet):
    queryset = AlbumImage.objects.all()
    serializer_class = AlbumImageSerializer

class AlbumImageView(viewsets.ModelViewSet):
    queryset = AlbumImage.objects.all()
    serializer_class = AlbumImageSerializer


