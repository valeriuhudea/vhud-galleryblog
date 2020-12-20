from django.contrib import admin
from .models import Post, Comment

#@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'post_image', 'tags', 'slug', 'author', 'body', 'publish', 'status')
    list_display = ('title', 'tags', 'slug', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


#@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'thumbnail', 'tags', 'visibility', 'slug')
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
