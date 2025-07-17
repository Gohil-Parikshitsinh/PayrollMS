from django.contrib import admin
from .models import SalaryRecord,SalaryStructure,Payslip
# Register your models here.

admin.site.register(SalaryRecord)
admin.site.register(SalaryStructure)
admin.site.register(Payslip)
