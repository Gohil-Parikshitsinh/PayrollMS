# employees/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Designation, Department, Employee
from .forms import DesignationForm, DepartmentForm, EmployeeForm, UserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def designation_list(request):
    designations = Designation.objects.all()
    return render(request, 'employees/designation_list.html', {'designations': designations})

@login_required
def designation_create(request):
    if request.method == 'POST':
        form = DesignationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Designation created successfully.')
            return redirect('employees:designation_list')
    else:
        form = DesignationForm()
    return render(request, 'employees/designation_form.html', {'form': form, 'title': 'Add Designation'})

@login_required
def designation_edit(request, pk):
    designation = get_object_or_404(Designation, pk=pk)
    if request.method == 'POST':
        form = DesignationForm(request.POST, instance=designation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Designation updated successfully.')
            return redirect('employees:designation_list')
    else:
        form = DesignationForm(instance=designation)
    return render(request, 'employees/designation_form.html', {'form': form, 'title': 'Edit Designation'})

@login_required
def designation_delete(request, pk):
    designation = get_object_or_404(Designation, pk=pk)
    if request.method == 'POST':
        designation.delete()
        messages.success(request, 'Designation deleted.')
        return redirect('employees:designation_list')
    return render(request, 'employees/designation_confirm_delete.html', {'designation': designation})

def is_admin(user):
    return user.is_authenticated and user.role == 'ADMIN'

@login_required
@user_passes_test(is_admin)
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'employees/department_list.html', {'departments': departments})

@login_required
@user_passes_test(is_admin)
def department_create(request):
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('employees:department_list')
    return render(request, 'employees/department_form.html', {'form': form, 'title': 'Add Department'})

@login_required
@user_passes_test(is_admin)
def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=department)
    if form.is_valid():
        form.save()
        return redirect('employees:department_list')
    return render(request, 'employees/department_form.html', {'form': form, 'title': 'Edit Department'})

@login_required
@user_passes_test(is_admin)
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('employees:department_list')
    return render(request, 'employees/department_confirm_delete.html', {'object': department})


@login_required
@user_passes_test(is_admin)
def employee_list(request):
    employees = Employee.objects.select_related('user', 'department', 'designation').all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

# Create Employee
@login_required
@user_passes_test(is_admin)
def employee_create(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        emp_form = EmployeeForm(request.POST)
        if user_form.is_valid() and emp_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'EMPLOYEE'
            user.set_password(user.password)
            user.save()
            employee = emp_form.save(commit=False)
            employee.user = user
            employee.save()
            messages.success(request, 'Employee created successfully.')
            return redirect('employees:employee_list')
    else:
        user_form = UserForm()
        emp_form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {
        'user_form': user_form,
        'emp_form': emp_form,
        'title': 'Create Employee'
    })

# View Employee Detail
@login_required
@user_passes_test(is_admin)
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})

@login_required
@user_passes_test(is_admin)
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    user = employee.user
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        emp_form = EmployeeForm(request.POST, instance=employee)
        if user_form.is_valid() and emp_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            emp_form.save()
            messages.success(request, 'Employee updated successfully.')
            return redirect('employees:employee_list')
    else:
        user_form = UserForm(instance=user)
        emp_form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {
        'user_form': user_form,
        'emp_form': emp_form,
        'title': 'Edit Employee'
    })

# Delete Employee
@login_required
@user_passes_test(is_admin)
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.user.delete()  # This also deletes employee due to OneToOne
        messages.success(request, 'Employee deleted.')
        return redirect('employees:employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})