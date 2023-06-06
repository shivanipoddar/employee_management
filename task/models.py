from django.db import models
from employee.models import EmployeeModel


class TaskModel(models.Model):
    assign_to = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now=True)
    task = models.TextField()
    is_closed = models.BooleanField(default=False)
