from django.shortcuts import render, HttpResponse, redirect,reverse
from django.contrib.auth.models import User
from .forms import register,login,forgot,reset_password,user_setting
from django.contrib.auth import authenticate,login as Login,logout
from .utils import generate_token,reset_token
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from .send_email import sender
from background_task import background
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def register_view(request):
    form = register()
    if request.method == 'POST':
        form = register(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name'].capitalize()
            last_name=form.cleaned_data['last_name'].capitalize()
            email=form.cleaned_data['email']
            user = User.objects.create_user(
                username = email, 
                first_name = first_name,
                last_name = last_name,
                password = form.cleaned_data['password'],
                is_active = False,
            )
            user.is_active = False
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('activate',kwargs={'uidb64':uidb64,
            'token':generate_token.make_token(user)})
            activate_link = 'http://'+domain+link
            email_obj = sender('register_user',email,first_name,activate_link)
            try:
                email_obj.send()
                user.save()
                notify_user(email,'register')
                messages.success(request, 'Activation link sent to your email address')
            except:
                user.delete()
                messages.success(request,'Please Connect to internet')
            return redirect('register')
    return render(request,'index.html',{'register_form':form})

@background(schedule=30)
def notify_user(email,action):
    user=User.objects.get(username=email)
    if not user.is_active and action=="register":
        user.delete()
    if user.is_active and action=="reset":
        user.last_login=timezone.now()
        user.save()


def login_view(request):
    form=login()
    if request.method == 'POST':
        form = login(request.POST)   
        if form.is_valid():  
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request,username=email,password=password)
            if not User.objects.filter(username=email).exists():
                messages.error(request, 'The user does not exist')
                return redirect('login')
            if user is not None:
                Login(request,user)
                return redirect('home')
            messages.error(request, 'Incorrect password. Please try again!')
            return redirect('login')
    return render(request,'login.html',{'login_form':form})

def activate_view(request,uidb64,token):
    try:
        uidb64= urlsafe_base64_decode(force_text(uidb64))
        user = User.objects.get(pk=uidb64)
        if not user.is_active and generate_token.check_token(user,token):
            user.is_active = True
            user.last_login = timezone.now()
            user.save()
            messages.success(request,'Successfully Activate your account')
            return redirect('login')
        messages.error(request,'Link expired')
        return redirect('register')
    except:
        messages.error(request,'Link expired')
        return redirect('register')

def forgot_view(request):
    form=forgot()
    if request.method == 'POST':
        form=forgot(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            user = User.objects.get(username=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('reset_password',kwargs={'uidb64':uidb64,
            'token':reset_token.make_token(user)})
            reset_password_link = 'http://'+domain+link
            email_obj = sender('reset_password',email,user.first_name,reset_password_link)
            try:
                email_obj.send()
                notify_user(email,'reset')
                messages.success(request,'Successfully reset link send to your email')
            except:
                messages.error(request,'Please Connect to internet')
            return redirect('forgot')
    return render(request,'forgot.html',{'forgot_form':form})

def reset_password_view(request,uidb64,token):
    try:
        uidb64_reset= urlsafe_base64_decode(force_text(uidb64))
        user = User.objects.get(pk=uidb64_reset)
        form = reset_password(initial={'email':user})
        if user is not None and reset_token.check_token(user,token):
            if request.method == 'POST':
                form=reset_password(request.POST)
                if form.is_valid():
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    messages.success(request,'sucessfully reset your password')
                    return redirect('login')
            return render(request,'reset_password.html',{'reset_form':form})

        else:
            messages.error(request,'Link Expired')
            return redirect('forgot')
    except:
        messages.error(request,'Link Expired')
        return redirect('forgot')

def apis_view(request):
    if not request.user.is_authenticated:
        messages.error(request,'Content not accessible plz login first')
        return redirect('%s?next=%s' % (reverse('login'), request.path))
    first_name = request.user.first_name
    return render(request, 'apis.html',{'first_name':first_name})

def logout_view(request):
    logout(request)
    messages.info(request,'Logged out')
    return redirect('login')

def home_view(request):
    if request.user.is_authenticated:
        first_name = request.user.first_name
        return render(request, 'home.html',{'first_name':first_name})
    return render(request, 'home.html')

def settings_view(request):
    if not request.user.is_authenticated:
        messages.error(request,'Content not accessible plz login first')
        return redirect('%s?next=%s' % (reverse('login'), request.path))
    user = request.user
    form = user_setting(initial={'email':user,'first_name':user.first_name,'last_name':user.last_name})
    first_name = request.user.first_name
    last_name = request.user.last_name
    if request.method == 'POST':
        form = user_setting(request.POST)
        if form.is_valid():
            if form.cleaned_data['delete_account']:
                user.delete()
                messages.success(request,'account deleted.')
                email_obj = sender('delete_user',user.username,user.first_name)
                email_obj.send()
                return redirect('login')
            password=form.cleaned_data['new_password']
            if password:
                user.set_password(password)
            user.first_name = form.cleaned_data['first_name']
            
            user.last_name = form.cleaned_data['last_name']
            user.save()
            messages.success(request,'Changes Saved Successfully.')
            return redirect('settings')
    return render(request, 'user_setting.html',{'first_name':first_name,'settings_form':form})