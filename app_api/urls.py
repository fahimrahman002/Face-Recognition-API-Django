from django.urls import path, include
from app_api import views
urlpatterns = [
    path('home', views.home, name='home'),
    path('videoTimeline/<int:pk>', views.videoTimeline, name='videoTimeline'),
    path('getSelectedThumbnails/<int:pk>', views.getSelectedThumbnails, name='getSelectedThumbnails'),
    path('deleteSelectedThumbnails/<str:group_img_name>', views.deleteSelectedThumbnails, name='deleteSelectedThumbnails'),
    path('uploadGroupImage/', views.groupImageUpload, name='group_image-upload'),
    path('thumbnailList', views.thumbnailList, name='thumbnailList'),
    path('groupImageList', views.groupImageList, name='groupImageList'),
    path('selectedThumbnailList', views.selectedThumbnailList, name='selectedThumbnailList'),
    path('testUpload/', views.testUpload, name='test_upload'),
    path('uploadThumbnails/', views.uploadThumbnails, name='uploadThumbnails'),
    path('postGeneratedTimeline/<int:pk>/', views.postGeneratedTimeline, name='postGeneratedTimeline'),
    path('deleteGeneratedTimeline/<int:pk>', views.deleteGeneratedTimeline, name='deleteGeneratedTimeline'),
    path('deleteGroupImage/<int:pk>', views.deleteGroupImage, name='deleteGroupImage'),
    path('removeImageFromS3', views.removeImageFromS3, name='removeImageFromS3'),
    
]
