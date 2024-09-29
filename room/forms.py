from django import forms
from .models import Room, Booking, Feedback, User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'phone', 'profile_picture'] 

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
        help_texts = {
            'username': None,  # ลบข้อความอธิบายสำหรับชื่อผู้ใช้
            'email': None,     # ลบข้อความอธิบายสำหรับอีเมล
            'password1': None, # ลบข้อความอธิบายสำหรับรหัสผ่าน
            'password2': None, # ลบข้อความอธิบายสำหรับการยืนยันรหัสผ่าน
            'role': None,      # ลบข้อความอธิบายสำหรับบทบาท
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_name', 'room_image', 'booking_status', 'price']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'start_date', 'end_date']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['room', 'rating', 'comment']