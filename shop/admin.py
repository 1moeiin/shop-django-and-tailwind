from django.contrib import admin
from .models import *

# Register your models here.


class FeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 0


class ImageInline(admin.TabularInline):
    model = Image
    

class CommentInline(admin.TabularInline):
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'status']
    list_filter = ['author', 'publish', 'status']
    search_fields = ['title', 'description']
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status']
    inlines = [ImageInline, CommentInline, FeatureInline]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject']
    
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'product', 'active']
    list_filter = ['product', 'created', 'active']
    search_fields = ['name', 'body']
    list_editable = ['active']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'created', 'title']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


