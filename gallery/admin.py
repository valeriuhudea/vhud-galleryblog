from django.contrib import admin
from .models import *
from django import forms

class AlbumAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'thumbnail', 'tags', 'visibility', 'slug')
    list_display = ('title', 'description', 'thumbnail', 'created', 'tags', 'visibility', 'slug')
    list_filter = ('title', 'description', 'thumbnail', 'visibility', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('visibility', 'created')

class AlbumImageAdmin(admin.ModelAdmin):
	
    fields = ('album', 'name', 'image', 'thumbnail', 'alt', 'width', 'height', 'slug', 'price', 'availability', 'description')
    list_display = ( 'name', 'image', 'thumbnail', 'get_album_title', 'created', 'slug', 'price', 'availability')
    list_filter = ( 'name', 'thumbnail', 'album', 'alt', 'price', 'availability')
    readonly_fields = ('slug',)

    class CustomModelChoiceField(forms.ModelChoiceField):
         def label_from_instance(self, obj):
             return "%s" % (obj.title)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'album':
            return self.CustomModelChoiceField(queryset=Album.objects)

        return super(AlbumImageAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
		
    def get_album_title(self, obj):
        return obj.album.title
    get_album_title.admin_order_field  = 'album'  #Allows column order sorting
    get_album_title.short_description = 'Album Name'  #Renames column head
			 	 
class ClientMessagesAdmin(admin.ModelAdmin):
     fields = ('name', 'email', 'subject', 'message')
     list_display = ('name', 'email', 'message',  'subject', 'date')
     list_filter = ('name', 'email', 'subject', 'message', 'date')	 
     readonly_fields = ['date']

admin.site.register(Album, AlbumAdmin)
admin.site.register(AlbumImage, AlbumImageAdmin)
admin.site.register(ClientMessage, ClientMessagesAdmin)

