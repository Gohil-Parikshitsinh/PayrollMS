from calendar import month_name, monthrange
from datetime import date, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from datetime import date
from django.db.models import Sum
from django.shortcuts import render
from employees.models import Employee
from leaves.models import LeaveRequest, LeaveBalance
from attendance.models import Attendance
from payroll.models import SalaryRecord
from core.models import Holiday



def login_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'role') and request.user.role in ['ADMIN', 'HR', 'EMPLOYEE']:
            return redirect_based_on_role(request.user)  # Only once on first access

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Attempting login with: {username} / {password}")  # DEBUG
            user = authenticate(request, username=username, password=password)
            print(f"Authenticated user: {user}")  # DEBUG

            if user is not None:
                login(request, user)
                return redirect_based_on_role(user)  # Redirect after login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('users:login')

def redirect_based_on_role(user):
    if user.role == 'ADMIN':
        return redirect('/users/admin-dashboard/')
    elif user.role == 'HR':
        return redirect('/users/hr-dashboard/')
    elif user.role == 'EMPLOYEE':
        return redirect('/users/employee-dashboard/')
    else:
        return redirect('/')  # fallback to home, not login

def role_required(role):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'role') and request.user.role == role:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("🚫 Access Denied")
        return _wrapped_view
    return decorator

@role_required('ADMIN')
def admin_dashboard(request):
    today = date.today()
    current_month = today.month
    current_year = today.year

    # Total counts
    employee_count = Employee.objects.count()
    pending_leaves = LeaveRequest.objects.filter(status='PENDING').count()
    present_today = Attendance.objects.filter(date=today, status='PRESENT').count()

    # Payroll data for last 6 months
    month_labels = []
    payroll_totals = []

    for i in range(5, -1, -1):
        month_date = today.replace(day=1) - timedelta(days=30 * i)
        month = month_date.month
        year = month_date.year

        total = SalaryRecord.objects.filter(
            created_at__year=year,
            created_at__month=month
        ).aggregate(Sum('net_salary'))['net_salary__sum'] or 0

        month_labels.append(month_name[month][:3])  # 'Jan', 'Feb', etc.
        payroll_totals.append(float(total))

    context = {
        'employee_count': employee_count,
        'pending_leaves': pending_leaves,
        'present_today': present_today,
        'payroll_labels': month_labels,
        'payroll_totals': payroll_totals,
    }

    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def hr_dashboard(request):
    today = date.today()
    current_month = today.month
    current_year = today.year

    employee_count = Employee.objects.count()
    pending_leaves = LeaveRequest.objects.filter(status='PENDING').count()
    present_today = Attendance.objects.filter(date=today, status='PRESENT').count()
    absent_today = Attendance.objects.filter(date=today, status='ABSENT').count()

    payroll_total = SalaryRecord.objects.filter(
        created_at__month=current_month,
        created_at__year=current_year
    ).aggregate(Sum('net_salary'))['net_salary__sum'] or 0

    recent_leaves = LeaveRequest.objects.select_related('employee').order_by('-applied_on')[:5]

    context = {
        'employee_count': employee_count,
        'pending_leaves': pending_leaves,
        'present_today': present_today,
        'absent_today': absent_today,
        'payroll_total': payroll_total,
        'recent_leaves': recent_leaves,
    }

    return render(request, 'dashboard/hr_dashboard.html', context)

@login_required
def employee_dashboard(request):
    user = request.user
    print("User:", user.username, "| Role:", user.role)

    try:
        employee = user.employee
        print("Employee found:", employee)
    except Exception as e:
        print("Error fetching employee:", e)
        return redirect('/')

    try:
        today = date.today()
        start_date = today.replace(day=1)
        end_date = today.replace(day=monthrange(today.year, today.month)[1])

        attendance_records = Attendance.objects.filter(employee=employee, date__range=(start_date, end_date))
        total_present = attendance_records.filter(status='PRESENT').count()
        total_absent = attendance_records.filter(status='ABSENT').count()
        total_leaves = attendance_records.filter(status='LEAVE').count()

        leave_balance = LeaveBalance.objects.filter(employee=employee).first()
        recent_leaves = LeaveRequest.objects.filter(employee=employee).order_by('-applied_on')[:5]
        last_salary = SalaryRecord.objects.filter(employee=employee).order_by('-created_at').first()
        upcoming_holidays = Holiday.objects.filter(date__gte=today).order_by('date')[:3]

        context = {
            'employee': employee,
            'total_present': total_present,
            'total_absent': total_absent,
            'total_leaves': total_leaves,
            'leave_balance': leave_balance,
            'recent_leaves': recent_leaves,
            'last_salary': last_salary,
            'upcoming_holidays': upcoming_holidays,
        }

        print("Context prepared successfully.")
        return render(request, 'dashboard/employee_dashboard.html', context)

    except Exception as e:
        print("ERROR during dashboard preparation:", e)
        return redirect('/')