from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', "was_published_recently")
    list_filter = ['publish_date']


admin.site.register(Post, PostAdmin)
