from django.urls import path

from . import views

urlpatterns = [
    path('chunk', views.chunk_view, name='chunk'),
    path('tokenize', views.tokenize_view, name='tokenize'),
    path('', views.index, name='chunk_text'),
]