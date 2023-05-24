from django.contrib import admin
from . models import Article, Comment, Category, Profile, Story



admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Story)
# admin.site.register(Payment)