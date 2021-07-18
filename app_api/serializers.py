from rest_framework import serializers
from .models import GroupImage, SelectedThumbnail,Thumbnail,GeneratedTimeline
from app_api import models


class GroupImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=GroupImage
        fields='__all__'

class ThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Thumbnail
        fields='__all__'

class SelectedThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model=SelectedThumbnail
        fields='__all__'

class GeneratedTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model=GeneratedTimeline
        fields='__all__'