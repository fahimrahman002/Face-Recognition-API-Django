from django.urls import path, include
from app_api import views
urlpatterns = [
    path('home', views.home, name='home'),
    path('videoTimeline', views.videoTimeline, name='videoTimeline'),
    path('getSelectedThumbnails/<str:group_img_name>', views.getSelectedThumbnails, name='getSelectedThumbnails'),
    path('uploadGroupImage/', views.groupImageUpload, name='group_image-upload'),
    path('thumbnailList', views.get_thumbnails, name='thumbnail_list'),
    path('testUpload/', views.testUpload, name='test_upload'),
    path('uploadThumbnails/', views.uploadThumbnails, name='uploadThumbnails'),
    path('postGeneratedTimeline/', views.postGeneratedTimeline, name='postGeneratedTimeline'),
]
