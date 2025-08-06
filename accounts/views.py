from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, UserProfileSerializer, ChangePasswordSerializer, EmailAuthSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .utils import send_verification_email
from .models import User
from django.contrib.auth.tokens import default_token_generator

# /accounts/register/
# convert to class-based views
class RegisterView(APIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_verification_email(user, request)
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def get(self, request):
        uid = request.query_params.get('uid')
        token = request.query_params.get('token')

        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response({"detail": "Invalid user."}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save()
            return Response({"detail": "Email verified successfully."})
        else:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

class EmailTokenLoginView(APIView):
    serializer_class = EmailAuthSerializer
    @extend_schema(
        request=EmailAuthSerializer,
        responses={
            200: OpenApiResponse(
                description="Success - Returns authentication token",
            ),
            400: OpenApiResponse(
                description="Bad request - Invalid input",
            ),
            401: OpenApiResponse(
                description="Unauthorized - Invalid credentials",
            )
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# /accounts/logout/
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None
    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(description="Successfully logged out."),
            400: OpenApiResponse(description="Token not found."),
        }
    )
    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()  # Deletes token
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)
        
# /accounts/profile/
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(description="Password updated successfully."),
            400: OpenApiResponse(description="Validation error or wrong password."),
        }
    )
    def put(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)