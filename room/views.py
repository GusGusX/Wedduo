from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import UserRegisterForm, RoomForm, Booking
from .models import UserProfile
from .forms import UserProfileForm
from .models import Room
import json


def profile_view(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profile.html', {'user_profile': profile})

def user_profile(request):
    return render(request, 'profile.html')

def profile_view(request):
    return render(request, 'user_profile.html')

class UserProfileView(TemplateView):
    template_name = 'profile.html'

@login_required


@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')  # เปลี่ยนไปยังหน้าแดชบอร์ดของผู้ใช้
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {'form': form, 'user': request.user, 'user_profile': user_profile})

@login_required
def notifications_view(request):
    # ตัวอย่างข้อมูลการแจ้งเตือน
    notifications = [
        {'message': 'การจองห้อง 101 สำเร็จ'},
        {'message': 'มีการยกเลิกการจองในห้อง 102'},
        {'message': 'การจองห้อง 103 กำลังรอการยืนยัน'}
    ]
    return JsonResponse({'notifications': notifications})

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
                return redirect('user_dashboard')
        else:
            print("Authentication failed")
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')

    return render(request, 'login.html')



def dorm_dashboard(request):
    # ตรวจสอบว่าผู้ใช้เป็น dorm_owner หรือไม่
    if request.user.role != 'dorm_owner':
        return redirect('login')
      # หากไม่ใช่ให้ส่งกลับไปที่หน้า login
    return render(request, 'dorm_dashboard.html')



def user_dashboard(request):
    # ดึงข้อมูลห้องที่ถูกเพิ่มจากฐานข้อมูล
    rooms = Room.objects.all()  # ปรับตามการกรองห้องที่คุณต้องการแสดง
    
    context = {
        'rooms': rooms,
    }
    return render(request, 'user_dashboard.html', context)

def logout(request):
    return render(request,'login.html')


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