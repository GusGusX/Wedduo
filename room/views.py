<<<<<<< HEAD

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .forms import UserRegisterForm, RoomForm, BookingForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.http import JsonResponse 
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from .models import UserProfile
from django.conf import settings
from django.core.mail import send_mail
from .forms import UserProfileForm
from .models import Room, Booking
import json

@login_required
def book_room(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        
        if form.is_valid():
            room = form.cleaned_data['room']
            start_date = form.cleaned_data['start_date']
            start_time = request.POST['start_time']
            end_date = form.cleaned_data['end_date']
            end_time = request.POST['end_time']
            
            # Check if the room is available for the selected dates
            if Booking.objects.filter(room=room, start_date__lt=end_date, end_date__gt=start_date).exists():
                messages.error(request, 'ห้องนี้มีการจองในช่วงวันที่เลือกแล้ว.')
            else:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.status = 'pending'  # Set initial status
                booking.save()
                messages.success(request, 'การจองห้องของคุณสำเร็จ!')
                return redirect('booking_success')  # Redirect to a success page
    else:
        form = BookingForm()

    return render(request, 'book_room.html', {'form': form})


class CustomPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'password_change.html'
    login_url = 'login'
    success_url = reverse_lazy('user_dashboard')
    success_message = "รหัสผ่านของคุณได้ถูกเปลี่ยนเรียบร้อยแล้ว!"

    def form_valid(self, form):
        if form.cleaned_data['new_password1'] == form.user.password:
            form.add_error('new_password1', 'รหัสผ่านใหม่ไม่สามารถซ้ำกับรหัสผ่านเก่าได้')
            return self.form_invalid(form)
        return super().form_valid(form)



@login_required
def profile_view(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)  # เพื่อให้อยู่ในระบบหลังจากเปลี่ยนรหัสผ่าน
            messages.success(request, 'รหัสผ่านของคุณถูกเปลี่ยนเรียบร้อยแล้ว!')
            return redirect('profile')  # กลับไปที่หน้าโปรไฟล์
    else:
        password_change_form = PasswordChangeForm(user=request.user)

    context = {
        'password_change_form': password_change_form,
    }
    return render(request, 'user_profile.html', context)

def user_profile(request):
    return render(request, 'user_profile.html')

class UserProfileView(TemplateView):
    template_name = 'user_profile.html'

@login_required
def edit_profile(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            # Redirect after successful save
            return redirect('user_dashboard')  # หรือ redirect ไปยังหน้าที่คุณต้องการ
        else:
            print(form.errors)  # แสดงข้อผิดพลาดจากฟอร์ม

    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {'form': form})

@login_required
def notifications_view(request):
    # ตัวอย่างข้อมูลการแจ้งเตือน
    notifications = [
        {'message': 'การจองห้อง 101 สำเร็จ'},
        {'message': 'มีการยกเลิกการจองในห้อง 102'},
        {'message': 'การจองห้อง 103 กำลังรอการยืนยัน'}
    ]
    return JsonResponse({'notifications': notifications})
=======
from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login 
from django.contrib import messages
from .forms import RoomForm ,BookingForm
from django.shortcuts import render
from .models import Room, Booking
from .models import Booking
from .models import User

# register logot login---------------------------------------------------------------
def logout(request):
    return render(request,'login.html')
>>>>>>> 81dd2abc103a00730d177ff73732224cef677520

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # บันทึกผู้ใช้
            print(f"User {user.username} created with role {user.role}")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        print(f"Attempting to login with Username: {username}, Password: {password}")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print(f"User authenticated: {user.username}, Role: {user.role}")
            login(request, user)
            # ตรวจสอบบทบาทของผู้ใช้และเปลี่ยนเส้นทาง
            if user.role == 'dorm_owner':
                return redirect('dorm_dashboard')
            elif user.role == 'user':
                return redirect('create_booking')
        else:
            print("Authentication failed")
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')

    return render(request, 'login.html')

#---------------------------------------------------------------------------------------------

# หน้าต่าง---------------------------------------------------------------------------------------


def dorm_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'dorm_owner':
        return redirect('login')
    
    # ดึงข้อมูลจำนวนห้องและจำนวนผู้ใช้
    users = User.objects.all().values('username', 'email')
    room_count = Room.objects.count()  # จำนวนห้องทั้งหมด
    user_count = User.objects.count()  # จำนวนผู้ใช้ทั้งหมด (ใช้โมเดลผู้ใช้ที่กำหนดเอง)
    
    context = {
        'room_count': room_count,
        'user_count': user_count,
        'users': users,
    }
    
    return render(request, 'dorm_dashboard.html', context)


def user_dashboard(request):
    # ตรวจสอบว่าผู้ใช้เป็น user หรือไม่
    if request.user.role != 'user':
        return redirect('login')  # หากไม่ใช่ให้ส่งกลับไปที่หน้า login
    return render(request, 'user_dashboard.html')

def history(request):
    bookings = Booking.objects.select_related('user', 'room').all()  # ดึงข้อมูล booking ที่มีความสัมพันธ์กับ user และ room
    return render(request, 'history.html', {'bookings': bookings})
# -----------------------------------------------------------------------------------------------------




# method----------------------------------------------------------------------------------------------

# เพิ่มห้อง
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'บันทึกสำเร็จแล้ว')
            return redirect('add_room')  # Redirect to clear the form
    else:
        form = RoomForm()
    
    return render(request, 'add_room.html', {'form': form})




 # ฟังก์ชั่นการจอง
def create_booking(request):

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # ตั้งค่าผู้ใช้ที่ทำการจองเป็นผู้ใช้ที่เข้าสู่ระบบ
            booking.save()  # บันทึกการจองลงในฐานข้อมูล
            return redirect('booking_list')  # ไปที่หน้ารายการจองเมื่อทำเสร็จ
    else:
        form = BookingForm()
    
    return render(request, 'create_booking.html', {'form': form})

def booking_list(request):

    bookings = Booking.objects.filter(user=request.user)  
    return render(request, 'booking_list.html', {'bookings': bookings})








# ฟังก์ชันตรวจสอบสิทธิ์ Dorm Owner
# def is_dorm_owner(user):
#     return user.role == 'dorm_owner'

def check_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        new_status = request.POST.get('status')
        booking = Booking.objects.get(id=booking_id)
        booking.status = new_status
        booking.save()   
        return redirect('check_booking')

    # ดึงข้อมูลการจองทั้งหมด
    bookings = Booking.objects.all()
    return render(request, 'check_booking.html', {'bookings': bookings})




