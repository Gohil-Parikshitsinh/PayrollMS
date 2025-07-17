from django.db import models
from employees.models import Employee

class SalaryStructure(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    basic_salary = models.FloatField()
    hra = models.FloatField()
    allowances = models.FloatField(default=0)
    deductions = models.FloatField(default=0)

    def __str__(self):
        return f"Salary Structure for {self.employee.user.username}"

class SalaryRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)  # e.g., July 2025
    year = models.IntegerField()
    gross_salary = models.FloatField()
    net_salary = models.FloatField()
    bonuses = models.FloatField(default=0)
    deductions = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'month', 'year')

    def __str__(self):
        return f"{self.employee.user.username} - {self.month} {self.year}"

class Payslip(models.Model):
    salary_record = models.OneToOneField(SalaryRecord, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='payslips/')  # optional: generate and upload

    def __str__(self):
        return f"Payslip - {self.salary_record}"
