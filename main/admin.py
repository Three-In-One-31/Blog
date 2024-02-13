from django.contrib import admin
from .models import *

# Register your models here.
class SearchPost(admin.ModelAdmin):
    search_fields = ['title']

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)