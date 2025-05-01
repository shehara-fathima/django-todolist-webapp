from django import forms
from .models import Drawing
class regform(forms.Form):
    name = forms.CharField(max_length=15)
    email = forms.EmailField()
    password = forms.CharField(max_length=10)
    cpass = forms.CharField(max_length=10)

class TaskForm(forms.Form):
    CATEGORY_CHOICES = [
        ('Work', 'Work'),
        ('Personal', 'Personal'),
        ('Other', 'Other'),
    ]
    title = forms.CharField(max_length=255)
    description = forms.CharField(max_length=300)
    category = forms.MultipleChoiceField(choices=CATEGORY_CHOICES)

class status_form(forms.Form):
    status_choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    status=forms.MultipleChoiceField(choices=status_choices)

class DrawingForm(forms.ModelForm):
    image_data=forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model=Drawing
        fields=['image_data']


