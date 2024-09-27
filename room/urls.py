from django.urls import path
from .views import user_dashboard, signup_view, login_view, logout_view, edit_booking
from . import views


urlpatterns = [

    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('edit-booking/<int:booking_id>/', edit_booking, name='edit_booking'),
]
