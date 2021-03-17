from . import views
from django.urls import path


urlpatterns = [
    # path('savefile', views.savefile, name='savefile'),
    path('', views.record, name='record'),
    path('audio_video_container', views.audio_video, name='audio_video_container'),
    path('audio_container', views.audio_container, name='audio_container'),
    path('video_container', views.video_container, name='video_container'),
]