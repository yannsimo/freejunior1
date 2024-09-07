from django.contrib import admin
from django.db import models
from django.forms import Textarea

from Blog.models import PostCategory, Post, Comment, PostImage, PostLink, PostSection

@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name',)

class PostSectionInline(admin.StackedInline):
    model = PostSection
    extra = 1

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1

class PostLinkInline(admin.TabularInline):
    model = PostLink
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'published',
        'created_at',
        'comments_count',
    )

    list_filter = (
        'category',
        'published',
    )
    search_fields = ('title', 'introduction')
    inlines = [PostSectionInline, PostImageInline, PostLinkInline]

    autocomplete_fields = ['category']

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 90})},
    }

    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = 'Comments'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ['post__title', 'author_name']
    list_display = (
        'post',
        'author_name',
        'status',
        'moderation_text',
        'created_at',
        'text',
    )

    list_editable = ('status', 'moderation_text')
    list_filter = ('status',)

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'image', 'caption')
    search_fields = ['post__title', 'caption']

@admin.register(PostLink)
class PostLinkAdmin(admin.ModelAdmin):
    list_display = ('post', 'url', 'text')
    search_fields = ['post__title', 'text']

@admin.register(PostSection)
class PostSectionAdmin(admin.ModelAdmin):
    list_display = ('post', 'subtitle', 'order')
    list_editable = ('order',)
    search_fields = ['post__title', 'subtitle']