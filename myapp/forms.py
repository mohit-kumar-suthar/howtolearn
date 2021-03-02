from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import re

class register(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(max_length=20)
    confirm_password = forms.CharField(max_length=20)

    def __init__(self,*args,**kwargs):
        super(register, self).__init__(*args,**kwargs)
        self.fields['first_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder':'First Name',
            'autocomplete':'off',
        })
        self.fields['last_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder':'Last Name',
            'autocomplete':'off',
        })
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder':'Email',
            'autocomplete':'off',
        })
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder':'Password',
            'autocomplete':'off'
        })
        
        self.fields['confirm_password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder':'Confirm Password',
            'autocomplete':'off',
        })

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise ValidationError(_("%(email)s Already Exists"),code='invalid',params={'email':email})
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if(len(password)<=8 and len(confirm_password)<=8):
            raise ValidationError(_("Password length must 8 "))
        if re.search('[A-Z]', password)!=None and re.search('[0-9]', password)!=None and re.search('[^A-Za-z0-9]', password)!=None:
            pass
        else:
            raise ValidationError(_("password contain symboll,small letter and capital letter"),code='invalid')
        if(password != confirm_password):
            raise ValidationError(_("Password must match"),code='invalid')
        return confirm_password

class login(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(max_length=20)

    def __init__(self,*args,**kwargs):
        super(login, self).__init__(*args,**kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder':'Email',
            'autocomplete':'off',
        })

        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder':'Password',
            'autocomplete':'off',
        })


class forgot(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Enter your registered email',
        'autocomplete':'off',
        }))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(username=email).exists():
            print('mohit')
            raise ValidationError(_("please enter registered email"),code='invalid')
        user = User.objects.get(username=email)
        if not user.is_active:
            raise ValidationError(_("please enter registered email"),code='invalid')
        return email
