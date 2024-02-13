from django.db import models
from django.urls import reverse
from django_resized import ResizedImageField
from django.conf import settings
from accounts import models as accounts_model

# Create your models here.
class Category(models.Model):
    owner = models.ForeignKey(accounts_model.User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('main:main')


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='1')
    TAG_CHOICES = [
        ('RESTAURANT', '맛집'),
        ('HOBBY', '취미'),
    ]
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = ResizedImageField(
        size = [500, 500],
        crop = ['middle', 'center'],
        upload_to = 'image/%Y/%m',
        blank=True,
        null=True
    )
    tag = models.CharField(max_length=30, choices = TAG_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')


    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20]


class Reply(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20]