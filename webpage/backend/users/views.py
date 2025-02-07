# users/views.py
import bcrypt
import json
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import UserSignupSerializer, UserLoginSerializer, UserProfileSerializer
from mongo import get_database


# Helper function to load user data from JSON
def load_user_data(username):
    try:
        db = get_database('usersData')
        collection = db[username]
        
        usersData = list(collection.find())
        for Data in usersData:
            Data.pop('_id', None)
        return usersData
    except FileNotFoundError:
        return None

# Signup API
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username'].capitalize()  # Capitalize the first letter
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

            # Prepare user data to be inserted into MongoDB, including points
            user_data = {
                'username': username,
                'email': email,
                'password': hashed_password,
                'points': 0  # Initialize points to 0
            }

            # Get the database and create a collection for the user
            db = get_database('usersData')  # Assuming the database is 'usersData'
            collection = db[username]  # Use the username as the collection name
            
            # Insert the user data into the collection
            collection.insert_one(user_data)

            # Return a response indicating success
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
            print(user_data)
            if user_data:
                user_data = user_data[0]
                if bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
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
            user_data = user_data[0]
            serializer = UserProfileSerializer(user_data)
            return Response(serializer.data)
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'detail': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)

