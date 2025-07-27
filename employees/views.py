# employees/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Designation, Department
from .forms import DesignationForm, DepartmentForm
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