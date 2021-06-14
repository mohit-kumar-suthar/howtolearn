from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view,name='home'),
    path('register',views.register_view,name='register'),
    path('login',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('chat',views.chat_view,name='chat'),
    path('settings',views.settings_view,name='settings'),
    path('login/forgot',views.forgot_view,name='forgot'),
    path('login/forgot/reset/<slug:uidb64>/<slug:token>',views.reset_password_view,name='reset_password'),
    path('register/activate/<slug:uidb64>/<slug:token>',views.activate_view,name='activate'),
]
