from django.contrib import admin

from .models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'tag', 'app', 'image_id',
                    'size', 'local_build', 'built', 'last_version']
    list_filter = ['last_version', 'app']


admin.site.register(Image, ImageAdmin)
