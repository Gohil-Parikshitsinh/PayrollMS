from django.db import models
from employees.models import Employee
from users.models import User

class LeaveBalance(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    total_leaves = models.IntegerField(default=12)
    used_leaves = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.employee.user.username} - Leave Balance"

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=(
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ), default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'role': 'HR'})

    def __str__(self):
        return f"{self.employee.user.username} - {self.status}"
