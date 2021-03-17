from django.urls import path
from . import views
 
urlpatterns = [ 
    # all pages urls _______________________________________
    # path('', views.index, name='corpus'),

    path('change_filter', views.change_filter, name='change_filter'),
    path('dictionary_search', views.dictionary_search, name='dictionary_search'),
    path('add_prompt', views.add_prompt, name='add_prompt'),
    path('add_prompt_first_time', views.add_prompt_first_time, name='add_prompt_first_time'),
    path('vote', views.vote, name='vote'),
    path('qa', views.qa, name='qa'),
    path('get_metadata', views.get_metadata, name='get_metadata'),
    path('get_thesaurus', views.get_thesaurus, name='get_thesaurus'),
    path('add_thesaurus', views.add_thesaurus, name='add_thesaurus'),

    # sidebar urls _________________________________________
    path('', views.index, name='dictionary'),
    path('audio', views.audio, name='dictionary_audio'),
    path('video', views.video, name='dictionary_video'),
    path('dict_2', views.dict_2, name='dict_2'),
    path('translate', views.translate, name='translate'),
    path('<str:language>', views.dictionary, name='dictionary'),


]  