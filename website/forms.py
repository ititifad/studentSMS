from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
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

#class LoginForm(forms.Form):
    #username = forms.CharField()
    #password = forms.CharField(widget=forms.PasswordInput)
    
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class StudentsForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user', 'results', 'reports']
        
class StaffForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        
class ResultsForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = '__all__'