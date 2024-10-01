from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from .models import Room, Booking, Feedback, User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Your name", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label=_("รหัสผ่านใหม่"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("ยืนยันรหัสผ่านใหม่"), widget=forms.PasswordInput)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'address', 'phone'] 

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
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
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['room', 'rating', 'comment']