from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Circle, Post, Membership

admin.site.register(Circle)
admin.site.register(Post)
admin.site.register(Membership)

