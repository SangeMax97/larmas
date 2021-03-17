from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='translate_text'),
    path('search_translation', views.search_translation, name='search_translation'),
    path('add_translation', views.add_translation, name='add_translation'),
    path('get_text', views.get_text, name='get_text'),
    path('get_audio', views.get_audio, name='get_audio'),
    path('get_video', views.get_video, name='get_video'),
]