from django.urls import path
from .views import user_login, dorm_dashboard, user_dashboard ,register ,logout ,add_room

urlpatterns = [
    path('', user_login, name='login'),
    path('dorm_dashboard/', dorm_dashboard, name='dorm_dashboard'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('register/', register, name='register'),
    path('login/',user_login, name='login'),
    path('logout',logout, name='user_login'),
    path('add_room',add_room, name='add_room'),

  

]