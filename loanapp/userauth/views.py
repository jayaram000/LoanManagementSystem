from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate,get_user_model
from .serializers import RegisterSerializer,OTPVerifySerializer,LoginSerializer
import random
from rest_framework.permissions import IsAuthenticated
import requests


User = get_user_model()

class UserRegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            email = user.email

            response = requests.post("http://localhost:5000/send-otp", json={"email": email})

            if response.status_code == 200:
                otp_data = response.json()
                user.otp = otp_data['otp']
                user.save()
                return Response({"message":"OTP sent to email"},status=status.HTTP_201_CREATED)
            else:
                return Response({"errors":"Failed to send OTP"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class OTPVerifyView(APIView):
    def post(self,request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
                if user.otp == serializer.validated_data['otp']:
                    user.is_verified = True
                    user.save()
                    refresh = RefreshToken.for_user(user)
                    return Response({"access": str(refresh.access_token)}, status=status.HTTP_200_OK)
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class User_LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'],
                                password=serializer.validated_data['password'])
            if user:
                if not user.is_verified:
                    return Response({"error": "User not verified"}, status=status.HTTP_400_BAD_REQUEST)
                refresh = RefreshToken.for_user(user)
                return Response({"access": str(refresh.access_token),"refresh": str(refresh)}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid tokenn"}, status=status.HTTP_400_BAD_REQUEST)




