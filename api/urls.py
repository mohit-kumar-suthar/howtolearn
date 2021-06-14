from django.urls import path
from . import views

urlpatterns = [
    path('api-overview',views.api_overview,name="api-overview"),
    path('register-with-otp',views.register_with_otp,name="register-with-otp"),
    path('register-with-otp/<str:pk>',views.register_with_otp,name="register-with-otp"),
    path('register-otp',views.otp_view,name="otp"),
]