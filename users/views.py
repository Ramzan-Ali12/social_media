from django.contrib.auth import authenticate, get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    permission_classes = [AllowAny]
    """
    POST email, username, password → creates a new user.
    """
    @swagger_auto_schema(request_body=RegisterSerializer)
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not confirm_password:
            return Response({'error': 'Confirm password is required'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(ObtainAuthToken):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=user.username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    """
    POST (authenticated) → 200 OK
    Deletes the user’s token on logout.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # simply delete this user’s token
        request.user.auth_token.delete()
        return Response(
            {'detail': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )
