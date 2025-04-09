from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ProfilePage, StaffProfilePage,CustomUser

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[("staff", "Staff"), ("management", "Management")])

    class Meta:
        model = CustomUser  
        fields = ["username", "password", "password_confirm","role"]        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = ProfilePage
        fields = ['full_name', 'email', 'staff_id', 'Dob', 'mobile_no','address','profile_pic']
        widgets = {
            'Dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_mobile_no(self):
        mobile_no = self.cleaned_data.get('mobile_no')
        if not mobile_no.isdigit() or len(mobile_no) != 10:
            raise forms.ValidationError("Mobile number must be exactly 10 digits and contain only digits.")
        return mobile_no



class StaffProfilePageForm(forms.ModelForm):
    class Meta:
        model = StaffProfilePage
        fields = ['full_name', 'email', 'staff_id', 'Dob', 'mobile_no','address','profile_pic']
        widgets = {
            'Dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_mobile_no(self):
        mobile_no = self.cleaned_data.get('mobile_no')
        if not mobile_no.isdigit() or len(mobile_no) != 10:
            raise forms.ValidationError("Mobile number must be exactly 10 digits and contain only digits.")
        return mobile_no