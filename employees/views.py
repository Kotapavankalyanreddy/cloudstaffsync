from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, ProfilePageForm
from .models import Attendance, Task, ProfilePage, StaffLeaveRequest , PerformanceReport,Payroll,StaffProfilePage
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime
from datetime import timedelta
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, ProfilePage
from cloud_utils.user_auth import process_login

def home(request):
    return render(request, 'home.html')




@csrf_exempt
def login_view(request): 
    if request.method == "POST":
        role = request.POST.get("role")  
        user = process_login(request, role)  

        if user:
            if role == "staff":
                return render(request, "staff_dashboard.html")
            elif role == "management":
                return render(request, "dashboard.html")
        else:
            form = AuthenticationForm(request, data=request.POST)
            return render(request, "login.html", {"form": form, "error": "Invalid credentials"})

    form = AuthenticationForm()
    return render(request, "login.html", {"form": form})



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data["role"]  
            user.save()

            # Create a profile with default values
            ProfilePage.objects.create(
                user=user,
                full_name=user.username,
                email=user.email,
                staff_id=00000,
                address="Default Address",
                mobile_no="0000000000"
            )

            login(request, user)  
            return redirect("dashboard")  

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

@login_required
def dashboard(request):
    if request.user.role != "management":
        return redirect("staff_dashboard")
    return render(request, "dashboard.html")

@login_required
def staff_dashboard(request):
    if request.user.role != "staff":
        return redirect("dashboard")
    return render(request, "staff_dashboard.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    try:
        profile_page = ProfilePage.objects.get(user=request.user)
    except ProfilePage.DoesNotExist:
        profile_page = ProfilePage.objects.create(
            user=request.user,
            full_name=request.user.get_full_name(),
            email=request.user.email,
            staff_id=00000,   
            address='Your Address Here',
            mobile_no='0000000000'  
        )
    context = {
        'profile_page': profile_page
    }
    return render(request, 'profile.html', context)


@login_required
def staff_profile(request):
    try:
        staff_profile_page = StaffProfilePage.objects.get(user=request.user)
    except StaffProfilePage.DoesNotExist:
        staff_profile_page = StaffProfilePage.objects.create(
            user=request.user,
            full_name=request.user.get_full_name(),
            email=request.user.email,
            staff_id=00000,   
            address='Your Address Here',
            mobile_no='0000000000'  
        )
    context = {
        'staff_profile_page': staff_profile_page
    }
    return render(request, 'staff_profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    profile = user.profilepage
    if request.method == 'POST':
        form = ProfilePageForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()  
            return redirect('profile')  
    else:
        form = ProfilePageForm(instance=profile)  

    return render(request, 'edit_profile.html', {'form': form})



@login_required
def staff_leave_request(request):
    """Staff members submit leave requests."""
    if request.method == "POST":
        reason = request.POST.get("reason")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        StaffLeaveRequest.objects.create(
            staff=request.user,
            reason=reason,
            start_date=start_date,
            end_date=end_date,
            status="Pending"
        )
        messages.success(request, "Your leave request has been submitted successfully!")

    leave_requests = StaffLeaveRequest.objects.filter(staff=request.user)
    return render(request, "staff_leave_request.html", {"leave_requests": leave_requests})


@login_required
def leave_request(request):
    """Admin can view and approve/reject leave requests."""
    if not request.user.is_superuser:  # Restrict to admin
        return redirect('dashboard')

    leave_requests = StaffLeaveRequest.objects.all()
    return render(request, "leave_request.html", {"leave_requests": leave_requests})


@login_required
def manage_leave(request, leave_id):
    """Handles approving or rejecting leave requests."""
    if not request.user.is_superuser:  # Ensure only admins can approve/reject
        return redirect('dashboard')

    leave_request = get_object_or_404(StaffLeaveRequest, id=leave_id)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "approve":
            leave_request.status = "Approved"
            messages.success(request, "Leave request approved successfully!")
        elif action == "reject":
            leave_request.status = "Rejected"
            messages.warning(request, "Leave request rejected.")
        
        leave_request.save()

    return redirect("leave_request")



@login_required
def staff_performance(request):
    return render(request,'staff_performance.html')

@login_required
def performance(request):
    reports = PerformanceReport.objects.all()
    return render(request, "performance.html", {"performance": reports})

@login_required
def add_performance(request):
    if request.method == "POST":
        score = request.POST.get("score")
        remarks = request.POST.get("remarks")

        PerformanceReport.objects.create(employee=request.user, score=score, remarks=remarks)
        messages.success(request, "Performance added successfully!")
        return redirect("performance.html")

    return render(request, "add_performance.html")

@login_required
def edit_performance(request, report_id):
    report = get_object_or_404(PerformanceReport, id=report_id)

    if request.method == "POST":
        report.score = request.POST.get("score")
        report.remarks = request.POST.get("remarks")
        report.save()
        messages.success(request, "Performance updated successfully!")
        return redirect("performance.html")

    return render(request, "edit_performance.html", {"report": report})

@login_required
def delete_performance(request, report_id):
    report = get_object_or_404(PerformanceReport, id=report_id)
    report.delete()
    messages.success(request, "Performance record deleted successfully!")
    return redirect("performance.html")

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
def notifications(request):
    return render(request, 'notifications.html')

@login_required
def upload(request):
    return render(request, 'upload.html')

def staff_attendance(request):
    attendance_records = Attendance.objects.all().order_by("-date")  
    return render(request, "staff_attendance.html", {"attendance_records": attendance_records})


@login_required
def attendance(request):
    user_attendance = Attendance.objects.filter(employee=request.user)
    
    schedule = [
        {
            'title': f"{record.status}",
            'start': str(record.date),
            'color': 'green' if record.status == 'Present' else 'red'
        }
        for record in user_attendance
    ]

    return render(request, 'attendance.html', {'schedule': schedule})

@login_required
def add_attendance(request):
    if request.method == "POST": 
        staff_id = request.POST.get("name")
        date = request.POST.get("date")
        status = request.POST.get("status")

        if not all([staff_id, date, status]):
            messages.error(request, "All fields are required")
            return redirect("employees/add_attendance")

        
        if Attendance.objects.filter(staff_id=staff_id,status=status, date=date).exists():
                messages.warning(request, "Attendance for this date already exists!")
        else:
                Attendance.objects.create(staff_id=staff_id, date=date, status=status)
                messages.success(request, "Attendance added successfully!")

        return redirect("attendance")


    return render(request, "employees/add_attendance.html")

@login_required
def get_attendance_data(request):
    user_attendance = Attendance.objects.filter(employee=request.user)
    
    events = [
        {
            "title": f"{record.status}",
            "start": record.date.strftime('%Y-%m-%d'),
            "color": "green" if record.status == "Present" else "red"
        }
        for record in user_attendance
    ]
    
    return JsonResponse(events, safe=False)

@login_required
def staff_payroll(request):
    return render(request,'staff_payroll.html')


@login_required
def payroll(request):
    """Handles payroll creation and listing."""
    if request.method == "POST":
        month = request.POST.get("month")
        staff_id=request.POST.get("staff_id")
        gross_pay = float(request.POST.get("gross_pay"))
        pf_amount = float(request.POST.get("pf_amount"))
        taxes = float(request.POST.get("taxes"))
        benefits = float(request.POST.get("benefits"))

        payroll, created = Payroll.objects.get_or_create(
            employee=request.user, month=month,
            defaults={'gross_pay': gross_pay, 'pf_amount': pf_amount, 'taxes': taxes, 'benefits': benefits}
        )

        if not created:
            payroll.gross_pay = gross_pay
            payroll.pf_amount = pf_amount
            payroll.taxes = taxes
            payroll.benefits = benefits
            payroll.calculate_net_pay()
            payroll.save()
            messages.success(request, f"Payroll for {month} updated successfully!")
        else:
            messages.success(request, f"Payroll for {month} added successfully!")

        return redirect("payroll")

    payrolls = Payroll.objects.filter(employee=request.user)
    return render(request, "payroll.html", {"payrolls": payrolls})


@login_required
def edit_payroll(request, payroll_id):
    """Allows user to edit payroll only at the end of the month."""
    payroll = get_object_or_404(Payroll, id=payroll_id, employee=request.user)

    if request.method == "POST":
        payroll.gross_pay = float(request.POST.get("gross_pay"))
        payroll.pf_amount = float(request.POST.get("pf_amount"))
        payroll.taxes = float(request.POST.get("taxes"))
        payroll.benefits = float(request.POST.get("benefits"))
        payroll.calculate_net_pay()
        payroll.save()

        messages.success(request, "Payroll updated successfully!")
        return redirect("payroll")

    return render(request, "edit_payroll.html", {"payroll": payroll})
