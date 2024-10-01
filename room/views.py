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




