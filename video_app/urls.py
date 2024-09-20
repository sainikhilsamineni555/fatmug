from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_video, name='upload_video'),
    path('videos/', views.list_videos, name='list_videos'),
    path('videos/<int:video_id>/', views.video_detail, name='video_detail'),
]
