from django.db import models
# User Model สำหรับข้อมูลผู้ใช้
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.models import User
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)  
    phone = models.CharField(max_length=20, blank=True)  

class User(AbstractUser):
    ROLE_CHOICES = [
        
        ('user', 'User'),
        ('dorm_owner', 'Dorm_Owner'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)

    # เพิ่ม related_name เพื่อป้องกันการชนกันของชื่อ
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='rooms_user_set',  # เปลี่ยนชื่อ related_name เพื่อไม่ให้ชนกัน
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='rooms_user_permissions_set',  # เปลี่ยนชื่อ related_name เพื่อไม่ให้ชนกัน
        blank=True
    )

    def __str__(self):
        return self.username


# Room Model สำหรับข้อมูลห้องพัก
class Room(models.Model):
    room_name = models.CharField(max_length=100)
    room_image = models.ImageField(upload_to='room_images/')
    booking_status = models.BooleanField(default=True)  # True สำหรับว่าง, False สำหรับไม่ว่าง
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name


# Booking Model สำหรับข้อมูลการจอง
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Booking by {self.user.username} for {self.room.room_name}"


# Access Control Model สำหรับการจัดการสิทธิ์การเข้าถึงห้อง
class AccessControl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    access_level = models.BooleanField(default=True)  # True สำหรับเข้าถึงได้, False สำหรับไม่เข้าถึง

    def __str__(self):
        return f"Access for {self.user.username} to {self.room.room_name}"


# Feedback Model สำหรับรับความคิดเห็นจากผู้ใช้
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} for {self.room.room_name}"
