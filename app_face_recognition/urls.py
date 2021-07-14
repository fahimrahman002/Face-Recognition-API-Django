from django.urls import path
from app_face_recognition import views

urlpatterns=[
    path('',views.test,name='home'),
    path('test',views.test,name='test'),
]