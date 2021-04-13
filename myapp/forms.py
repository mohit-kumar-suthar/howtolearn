from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import re
from django.contrib.auth import authenticate

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
            raise ValidationError(_("please enter registered email"),code='invalid')
        user = User.objects.get(username=email)
        if not user.is_active:
            raise ValidationError(_("please enter registered email"),code='invalid')
        return email


class reset_password(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'autocomplete':'off',
        'readonly':True,
    }))
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'New Password',
        'autocomplete':'off',
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Confirm New Password',
        'autocomplete':'off',
    }))

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if(len(password)<=8 and len(confirm_password)<=8):
            raise ValidationError(_("Password length must 8 "))
        if re.search('[A-Z]', password)!=None and re.search('[0-9]', password)!=None and re.search('[^A-Za-z0-9]', password)!=None:
            pass
        else:
            raise ValidationError(_("password must strong"),code='invalid')
        if(password != confirm_password):
            raise ValidationError(_("Password must match"),code='invalid')
        return confirm_password

class user_setting(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    old_password = forms.CharField(max_length=20)
    new_password = forms.CharField(max_length=20, required=False)
    confirm_new_password = forms.CharField(max_length=20, required=False)
    delete_account = forms.BooleanField(required=False)
    
    def __init__(self,*args,**kwargs):
        super(user_setting, self).__init__(*args,**kwargs)
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
            'readonly':True,
        })
        self.fields['old_password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder':'Enter your Password',
            'autocomplete':'off'
        })
        
        self.fields['new_password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder':'New Password',
            'autocomplete':'off',
        })

        self.fields['confirm_new_password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder':'Confirm New Password',
            'autocomplete':'off',
        })

        self.fields['delete_account'].widget = forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id':'flexCheckDefault',
        })

    def clean_confirm_new_password(self):
        user = User.objects.get(username=self.cleaned_data.get('email'))
        password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_new_password')
        if not user.check_password(self.cleaned_data.get('old_password')):
            raise ValidationError(_("your password is incorrect"))
        if len(password) != 0 and len(confirm_password) != 0:
            if len(password) ==0 or len(confirm_password) ==0:
                raise ValidationError(_("enter both password and confirm password"))
            if(len(password)<=8 and len(confirm_password)<=8):
                raise ValidationError(_("New Password length must 8 char"))
            if re.search('[A-Z]', password)!=None and re.search('[0-9]', password)!=None and re.search('[^A-Za-z0-9]', password)!=None:
                pass
            else:
                raise ValidationError(_("New password contain symboll,small letter and capital letter"),code='invalid')
            if(password != confirm_password):
                raise ValidationError(_("New Password must match"),code='invalid')
        if len(password) == 0 and len(confirm_password) != 0:
            raise ValidationError(_("Enter new password in both fields"),code='invalid')
        if len(password) != 0 and len(confirm_password) == 0:
            raise ValidationError(_("Enter new password in both fields"),code='invalid')
        return confirm_password
