from django.urls import path
from .views import *


urlpatterns = [
    path('', user_login, name='login'),
    path('dorm_dashboard/', dorm_dashboard, name='dorm_dashboard'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('register/', register, name='register'),
    path('login/',user_login, name='login'),
    path('logout/',logout, name='logout'),
    path('history/',history, name='history'),

    #เพิ่มห้อง admin
    path('add_room/',add_room, name='add_room'),


    #ฟังก์ชั่นbooking user
    path('bookings/', booking_list, name='booking_list'),
    path('booking/create/', create_booking, name='create_booking'),
    
    path('check-booking/', check_booking, name='check_booking'),



]