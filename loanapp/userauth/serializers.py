from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()  #get the current usermodel added in settings.py

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username','email','password','role']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

