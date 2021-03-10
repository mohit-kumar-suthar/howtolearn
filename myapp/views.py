from django.shortcuts import render, HttpResponse, redirect,reverse
from django.contrib.auth.models import User
from .forms import register,login,forgot,reset_password
from .utils import generate_token,reset_token
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from .send_email import sender

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
            )
            user.is_active = False
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('activate',kwargs={'uidb64':uidb64,
            'token':generate_token.make_token(user)})
            activate_link = 'http://'+domain+link
            email = sender(email,first_name,activate_link)
            try:
                email.send()
                user.save()
                messages.success(request, 'Activation link sent to your email address')
            except:
                messages.success(request, 'Unable to send Activation link')
            return redirect('register')
    return render(request,'index.html',{'register_form':form})

def login_view(request):
    form=login()
    return render(request,'login.html',{'login_form':form})

def activate_view(request,uidb64,token):
    try:
        uidb64= urlsafe_base64_decode(force_text(uidb64))
        user = User.objects.get(pk=uidb64)
        if not user.is_active and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            messages.success(request,'Successfully Activate your account')
            return redirect('login')
        messages.warning(request,'Link expired')
        return redirect('register')
    except:
        return HttpResponse('invaild')

def forgot_view(request):
    form=forgot()
    if request.method == 'POST':
        form=forgot(request.POST)
        if form.is_valid():
            messages.success(request,'Successfully reset link send to your email')
            return redirect('forgot')
    return render(request,'forgot.html',{'forgot_form':form})

def reset_password_view(request,uidb64,token):
    try:
        uidb64_reset= urlsafe_base64_decode(force_text(uidb64))
        user = User.objects.get(pk=uidb64_reset)
        form = reset_password(initial={'email':user.email})
        if user.is_active:
            if request.method == 'POST':
                form = reset_password(request.POST)
                if reset_token.check_token(user,token):
                    if form.is_valid():
                        user.set_password(form.cleaned_data['password'])
                        user.save()
                        messages.success(request,'Successfully reset your password')
                        return ('login')
                    else:
                        return render(request, 'reset_password.html',{'reset_form':form})
                else:
                    messages.warning(request,'Link expired')
                    return redirect('reset_password')
            else:
                return render(request, 'reset_password.html',{'reset_form':form})
        else:
            return HttpResponse('invaild')
    except:
        return HttpResponse('invaild')