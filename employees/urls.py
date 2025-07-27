# employees/urls.py
from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('designations/', views.designation_list, name='designation_list'),
    path('designations/create/', views.designation_create, name='designation_create'),
    path('designations/<int:pk>/edit/', views.designation_edit, name='designation_edit'),
    path('designations/<int:pk>/delete/', views.designation_delete, name='designation_delete'),

    path('departments/', views.department_list, name='department_list'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/<int:pk>/edit/', views.department_edit, name='department_edit'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),



]
