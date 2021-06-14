from rest_framework import serializers
from .models import register
from django.contrib.auth.models import User
from myapp.models import access_key
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=16)
    access_key = serializers.CharField(max_length=16)
    access_email = serializers.EmailField()
    class Meta:
        model = register
        fields = "__all__"

    def create(self,validated_data):
        obj = register.objects.create(first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],
        email=validated_data['email'],
        password = make_password(validated_data['password'])
        )
        return obj
        

    def validate(self,data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password":"passwords must be equal"})
        try:
            access = User.objects.get(username=data['access_email'])
        except:
            raise serializers.ValidationError({"access_email":"enter registered email"})
        if data['access_key'] != access.access_key.key:
            raise serializers.ValidationError({"access_key":"access key not find."})
        return data

class OtpSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    def validate(self,data):
        if len(data['otp'])!=6:
            raise serializers.ValidationError({"otp":"otp length must be 6"})
        return data