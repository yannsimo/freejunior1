from django.db import models
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

class PostCategory(models.Model):
    name = models.CharField(max_length=50)

    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey('PostCategory',
                                 null=True,
                                 blank=True,
                                 on_delete=models.DO_NOTHING)
    published = models.BooleanField(default=False)
    introduction = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

class PostSection(models.Model):
    post = models.ForeignKey(Post, related_name='sections', on_delete=models.CASCADE)
    subtitle = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.post.title} - {self.subtitle}"


class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/')
    caption = models.CharField(max_length=200, blank=True)


    def __str__(self):
        return f"Image for {self.post.title}"

class PostLink(models.Model):
    post = models.ForeignKey(Post, related_name='links', on_delete=models.CASCADE)
    url = models.URLField(max_length=200)
    text = models.CharField(max_length=100)

    def __str__(self):
        return f"Link for {self.post.title}: {self.text}"
class Comment(models.Model):
    STATUS_VISIBLE = 'visible'
    STATUS_HIDDEN = 'hidden'
    STATUS_MODERATED = 'moderated'

    STATUS_CHOICES = (
        (STATUS_VISIBLE, 'Visible'),
        (STATUS_HIDDEN, 'Hidden'),
        (STATUS_MODERATED, 'Moderated'),
    )

    post = models.ForeignKey('Post',
                             on_delete=models.CASCADE,
                             related_name='comments')
    author_name = models.CharField(max_length=100)
    text = models.TextField()
    status = models.CharField(max_length=20,
                              default=STATUS_VISIBLE,
                              choices=STATUS_CHOICES)
    moderation_text = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {} (status={})'.format(self.author_name, self.text[:20], self.status)
