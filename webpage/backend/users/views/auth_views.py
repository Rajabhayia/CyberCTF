# users/views.py
import bcrypt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..serializers import UserSignupSerializer, UserLoginSerializer
from ..mongoUsers import get_database
from .utils import load_user_data

    
# Login API
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user_data = load_user_data(username)
            if user_data:
                stored_password = user_data['password']
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    return Response({'detail': 'Login successful.'}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Signup API
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username'].capitalize() 
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            confirm_password = serializer.validated_data['confirm_password']
            
            if password != confirm_password:
                return Response({'detail': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

            if load_user_data(username):
                return Response({'detail': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            user_data = {
                'username': username,
                'email': email,
                'password': hashed_password,
                'points': 0, 
                'team': None,
                'message': None
            }

            db = get_database('usersData')
            userCollection = db['userCollection']
            
            userCollection.insert_one(user_data)

            # Return a response indicating success
            return Response({'detail': 'User created successfully.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    