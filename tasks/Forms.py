from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'completed': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': False}),
        }
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'important': 'Importante',
            'completed': 'Fecha de Finalización',
        }