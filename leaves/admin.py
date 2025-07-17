from django.contrib import admin
from .models import LeaveBalance, LeaveRequest

# Register your models here.
admin.site.register(LeaveBalance)
admin.site.register(LeaveRequest)
