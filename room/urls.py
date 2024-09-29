from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('', user_login, name='login'),
    path('dorm_dashboard/', dorm_dashboard, name='dorm_dashboard'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('register/', register, name='register'),
    path('login/',user_login, name='login'),
    path('logout/',logout, name='user_login'),
    path('add_room/',add_room, name='add_room'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

  

]