from django.contrib import admin
from .models import User, Room, Booking, AccessControl, Feedback

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'created_at')
    search_fields = ('username', 'role')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'booking_status', 'price', 'created_at')
    search_fields = ('room_name',)
    list_filter = ('booking_status',)

@admin.register(Booking)
class BookingAadmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'start_date', 'end_date', 'status', 'booking_date')
    search_fields = ('user__username', 'room__room_name')
    list_filter = ('status',)

@admin.register(AccessControl)
class AccessControlAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'access_level')
    search_fields = ('user__username', 'room__room_name')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'rating', 'created_at')
    search_fields = ('user__username', 'room__room_name')
    list_filter = ('rating',)