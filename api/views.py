from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import register
from .serializers import RegisterSerializer,OtpSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from myapp.send_email import sender
import random
from django.views.decorators.csrf import csrf_protect

# Create your views here.
@api_view(["GET"])
def api_overview(request):
    if request.method == "GET":
        data = {'api overview':'/api-overview',
        'register api':'/register-with-otp',
        'login api':'/api/login'}
        return Response(data)

@csrf_protect
@api_view(["POST","DELETE"])
def register_with_otp(request,pk=None):
    if pk != None:
        try:
            user = register.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    
    if request.method == "POST":
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            rand_otp = random.randint(000000,999999)
            request.session['user_data'] = [data['email'],data['first_name'],data['last_name'],data['password'],rand_otp]
            request.session.set_expiry(60)
            email_obj = sender('otp',data['email'],data['first_name'],rand_otp)
            email_obj.send()
            return Response(status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET","POST"])
def otp_view(request):
    if request.method == "GET":
        return Response(data={"One Time Password":"XXXXXX"})
    if request.session.get('user_data'):
        if request.method == "POST":
            serializer = OtpSerializer(data = request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                if int(request.session.get('user_data')[4]) == int(data['otp']) :
                    print(request.session.get('user_data')[4], data['otp'])
                    register.objects.create(first_name=request.session.get('user_data')[1],
                    last_name=request.session.get('user_data')[2],
                    email=request.session.get('user_data')[0],
                    password=make_password(request.session.get('user_data')[3]))
                    return Response(data={"account":"register successfully"})
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    return Response(data={"error":"session expired"})
