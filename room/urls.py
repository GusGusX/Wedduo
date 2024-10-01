from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


urlpatterns = [
    path('', user_login, name='login'),
    path('dorm_dashboard/', dorm_dashboard, name='dorm_dashboard'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('register/', register, name='register'),
    path('login/',user_login, name='login'),
    path('logout/',logout, name='user_login'),
    path('add_room/',add_room, name='add_room'),
    path('profile/', profile_view, name='profile'),
    path('profile/', user_profile, name='user_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('booking_success/', TemplateView.as_view(template_name='booking_success.html'), name='booking_success'),
    path('book/', book_room, name='book_room'),
]