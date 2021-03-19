from django.shortcuts import render, HttpResponse, redirect,reverse
from django.contrib.auth.models import User
from .forms import register,login,forgot,reset_password
from django.contrib.auth import authenticate,login as Login,logout
from .utils import generate_token,reset_token
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from .send_email import sender
from background_task import background
from django.utils import timezone
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
            except Exception as e:
                user.delete()
                messages.success(request,e)
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
            if user is not None:
                Login(request,user)
                return redirect('home')
            else:
                messages.error(request, 'username or password wrong', extra_tags='login')
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
        messages.warning(request,'Link expired')
        return redirect('register')
    except:
        messages.warning(request,'Link expired')
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
            except:
                pass
            messages.success(request,'Successfully reset link send to your email')
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

@login_required(redirect_field_name='home', login_url='login')
def home_view(request):
    first_name = request.user.first_name
    return render(request, 'home.html',{'first_name':first_name})