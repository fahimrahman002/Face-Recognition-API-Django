from django.contrib import admin
from .models import GroupImage,Thumbnail,SelectedThumbnail,GeneratedTimeline

# Register your models here.

admin.site.register(GroupImage)
admin.site.register(Thumbnail)
admin.site.register(SelectedThumbnail)
admin.site.register(GeneratedTimeline)