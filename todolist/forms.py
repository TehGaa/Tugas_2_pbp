from django import forms
from django.db import models

class TaskForm(forms.Form):
    judul_task = forms.CharField(max_length = 225)
    deskripsi = forms.CharField(max_length = 225)

    
