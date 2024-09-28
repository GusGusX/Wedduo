
from django.contrib.auth.models import Group
from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login 
from django.contrib import messages
from .forms import RoomForm



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
    # ตรวจสอบว่าผู้ใช้เป็น user หรือไม่
    if request.user.role != 'user':
        return redirect('login')  # หากไม่ใช่ให้ส่งกลับไปที่หน้า login
    return render(request, 'user_dashboard.html')

def logout(request):
    return render(request,'login.html')


def add_room(request):
    return render(request,'add_room.html')
