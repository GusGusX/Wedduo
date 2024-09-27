from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.contrib import messages
import json

@csrf_exempt
def edit_booking(request, booking_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_date = data.get('new_date')

        try:
            booking = booking.objects.get(id=booking_id)
            booking.date = new_date
            booking.save()
            return JsonResponse({'success': True})
        except booking.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'ไม่พบการจองที่ระบุ'})
    return JsonResponse({'success': False, 'error': 'วิธีการไม่ถูกต้อง'})

@login_required
def notifications_view(request):
    # ตัวอย่างข้อมูลการแจ้งเตือน
    notifications = [
        {'message': 'การจองห้อง 101 สำเร็จ'},
        {'message': 'มีการยกเลิกการจองในห้อง 102'},
        {'message': 'การจองห้อง 103 กำลังรอการยืนยัน'}
    ]
    return JsonResponse({'notifications': notifications})

# ฟังก์ชันตรวจสอบว่าเป็นผู้ดูแลระบบ


def is_admin(user):
    return user.groups.filter(name='Admin').exists()

# มุมมองสำหรับผู้ดูแลระบบ
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# มุมมองสำหรับผู้ใช้ทั่วไป
@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')

# ฟังก์ชันสำหรับสมัครสมาชิก
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'บัญชีถูกสร้างเรียบร้อยแล้ว!')
            return redirect('login')
        else:
            messages.error(request, 'ข้อมูลที่กรอกไม่ถูกต้อง!')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# ฟังก์ชันสำหรับเข้าสู่ระบบ
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # ตรวจสอบว่าเป็นผู้ดูแลระบบหรือผู้ใช้ทั่วไปแล้วเปลี่ยนเส้นทางไปที่หน้า Dashboard ที่เหมาะสม
            if user.groups.filter(name='Admin').exists():
                return redirect('admin_dashboard')  # เปลี่ยนเส้นทางไปยังแดชบอร์ดของผู้ดูแลระบบ
            else:
                return redirect('user_dashboard')  # เปลี่ยนเส้นทางไปยังแดชบอร์ดของผู้ใช้ทั่วไป
        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง.')
            
    return render(request, 'login.html')

# ฟังก์ชันสำหรับออกจากระบบ
def logout_view(request):
    logout(request)
    return redirect('login')  # เปลี่ยนเส้นทางไปที่หน้า login