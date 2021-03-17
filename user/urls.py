from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(redirect_authenticated_user=True), name='signup'),
    path('profile/', views.Profile.as_view(redirect_authenticated_user=True), name='profile'),
    path('profile/edit', views.edit_profile, name='edit_profile')
    # path('profile/', views.profile, name='profile')
]