from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    username= forms.CharField(widget=forms.TextInput(
            attrs={'class':'form-control','placeholder':'Enter Username'}),required=True, max_length=20)
    email= forms.CharField(widget=forms.EmailInput(
            attrs={'class':'form-control','placeholder':'john-doe@mail.com'}),required=True, max_length=200)
    first_name= forms.CharField(widget=forms.TextInput(
            attrs={'class':'form-control','placeholder':'Enter First Name'}), required=False, max_length=20)
    last_name= forms.CharField(widget=forms.TextInput(
            attrs={'class':'form-control','placeholder':'Enter Last Name'}), required=False, max_length=20)
    password1= forms.CharField(widget=forms.PasswordInput(
            attrs={'class':'form-control','placeholder':'Enter Password'}),required=True, max_length=20)
    password2= forms.CharField(widget=forms.PasswordInput(
            attrs={'class':'form-control','placeholder':'Enter Same Password To Confirm'}),required=True, max_length=20)

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

    def clean_username(self):
        user= self.cleaned_data['username']
        try:
            check= User.objects.get(username=user)
        except:
            return user
        raise forms.ValidationError('User with this name already exsts')

    def clean_email(self):
        email= self.cleaned_data['email']
        try:
            v_email= validate_email(email)
        except:
            raise forms.ValidationError('Email is not in correct format.')
        return email

    def clean_password2(self):
        password1= self.cleaned_data['password1']
        password2= self.cleaned_data['password2']
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Password donnot match')
            else:
                if len(password2)<8:
                    raise forms.ValidationError('Password must be more than 8 characters.')
                if password2.isdigit():
                    raise forms.ValidationError('Password must be combination of letters and numbers.')
                if password2.isalpha():
                    raise forms.ValidationError('Password must be combination of letters and numbers.')
