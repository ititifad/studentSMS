from django import forms
from django.forms import ModelForm
from .models import *

class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        exclude=['completed']
        
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields= '__all__'
        widgets = {
            'gender': forms.Select(attrs={'class': 'custom-select md-form'}),
        }
        
class StudentSearchForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name']
        
class StudentFeeSearchForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['student']
        
class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = '__all__'
        
class ClassroomSearchForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)