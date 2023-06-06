from django import forms
from .models import TaskModel


class TaskForm(forms.ModelForm):

    class Meta:
        model = TaskModel
        fields = ['assign_to', 'task']