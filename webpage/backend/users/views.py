# users/views.py
import bcrypt
import json
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import UserSignupSerializer, UserLoginSerializer, UserProfileSerializer

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Helper function to save data in a JSON file
def save_user_data(username, data):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    with open(os.path.join(DATA_DIR, f'{username}.json'), 'w') as f:
        json.dump(data, f)

# Helper function to load user data from JSON
def load_user_data(username):
    try:
        with open(os.path.join(DATA_DIR, f'{username}.json'), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# Signup API
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            confirm_password = serializer.validated_data['confirm_password']
            
            # Check if passwords match
            if password != confirm_password:
                return Response({'detail': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if username or email already exists
            if load_user_data(username):
                return Response({'detail': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            # Hash the password using bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Save user data in JSON file
            user_data = {
                'username': username,
                'email': email,
                'password': hashed_password
            }
            save_user_data(username, user_data)
            return Response({'detail': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login API
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            # Load user data
            user_data = load_user_data(username)
            if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
                return Response({'detail': 'Login successful.'}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Profile API
@api_view(['GET'])
def profile(request):
    username = request.query_params.get('username')
    if username:
        user_data = load_user_data(username)
        if user_data:
            serializer = UserProfileSerializer(user_data)
            return Response(serializer.data)
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'detail': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)

