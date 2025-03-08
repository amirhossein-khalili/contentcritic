import logging
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from utils import code_generator

from .models import User
from .serializers import (CustomTokenObtainPairSerializer,
                          SignupStepOneSerializer, SignupStepTwoSerializer)

logger = logging.getLogger(__name__)


# ==================================================
#   Authentication
# ==================================================


class SignupStepOneView(APIView):
    serializer_class = SignupStepOneSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]

            verification_code = self.send_verification_code(email)
            cache.set(
                f"signup_{email}_user_data",
                serializer.validated_data,
                3600,
            )
            cache.set(
                f"signup_{email}_verification_code",
                verification_code,
                180,
            )

            return Response(
                {"message": "Verification code sent to email"},
                status=status.HTTP_200_OK,
            )


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_verification_code(self, user_email):
        code = code_generator()
        print("--------------")
        print('this is you code :' , code )
        print("--------------")
        return code


class SignupStepTwoView(APIView):
    serializer_class = SignupStepTwoSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            code = serializer.validated_data["code"]

            user_data = cache.get(f"signup_{email}_user_data")

            if user_data:
                code_data = cache.get(f"signup_{email}_verification_code")

                if not code_data:
                    verification_code = self.send_verification_code(email)
                    cache.set(
                        f"signup_{email}_verification_code",
                        verification_code,
                        180,
                    )

                    return Response(
                        {
                            "message": "Your code has expired. A new code has been sent to you.",
                        },
                        status=status.HTTP_200_OK,
                    )

                  
                if code == code_data:
                    user = User(
                        phone_number=user_data["phone_number"], email=user_data["email"]
                    )
                    user.set_password(user_data["password"])
                    user.save()

                    # Delete user data from cache
                    cache.delete(f"signup_{email}_user_data")
                    cache.delete(f"signup_{email}_verification_code")

                    return Response(
                        {"message": "You have signed up successfully 🥳🎉."},
                        status=status.HTTP_201_CREATED,
                    )

                else:
                    return Response(
                        {"error": "invalid code"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            return Response(
                {"error": "Please complete the first step of the signup process."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_verification_code(self, user_email):
        code = code_generator()
        print("--------------")
        print('this is you code :' , code )
        print("--------------")
        return code


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
