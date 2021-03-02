from django.urls import path
from . import views

urlpatterns = [
    path('',views.register_view,name='register'),
    path('login',views.login_view,name='login'),
    path('register/forgot',views.forgot_view,name='forgot'),
    path('activate/<slug:uidb64>/<slug:token>',views.activate_view,name='activate'),
]
