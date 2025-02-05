import json
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse

# Directory where user profile JSON files are stored
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Helper function to save profile data in a JSON file
def save_user_profile(username, data):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    with open(os.path.join(DATA_DIR, f'{username}.json'), 'w') as f:
        json.dump(data, f)

# Helper function to load user profile data from JSON
def load_user_profile(username):
    try:
        with open(os.path.join(DATA_DIR, f'{username}.json'), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# Helper function to load all usernames from the data directory
def load_all_usernames():
    try:
        usernames = []
        for filename in os.listdir(DATA_DIR):
            if filename.endswith('.json'):
                username = filename.split('.')[0]  # Extract username from the filename
                usernames.append(username)
        return usernames
    except Exception as e:
        return str(e)

# Profile API - Create, Update, or Load User Profile
@api_view(['POST'])
def update_profile(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')

        if not username:
            return Response({'detail': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user profile already exists
        existing_profile = load_user_profile(username)

        if existing_profile:
            # If the profile exists, load and return it (no update needed)
            return Response({'detail': 'Profile loaded successfully.', 'profile': existing_profile}, status=status.HTTP_200_OK)
        else:
            # If no existing profile, create and save a new one
            user_profile_data = {
                'username': username,
                'email': email,
                'points': 0,
            }
            save_user_profile(username, user_profile_data)
            return Response({'detail': 'Profile created successfully.'}, status=status.HTTP_201_CREATED)

# API View to load all users
@api_view(['GET'])
def load_users(request):
    try:
        usernames = load_all_usernames()
        if usernames:
            return Response({'users': usernames}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No users found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#API views to load points
@api_view(['GET'])
def load_points(request):
    if request.method == 'GET':
        username = request.GET.get('username')  # Fetch username from query params

        if not username:
            return JsonResponse({'error': 'Username parameter is required'}, status=400)

        file_path = os.path.join(DATA_DIR, f'{username}.json')

        if not os.path.exists(file_path):
            return JsonResponse({'error': f'No data found for user {username}'}, status=404)

        try:
            with open(file_path, 'r') as f:
                fetchedPoints = json.load(f)
                
                if 'points' in fetchedPoints:
                    points_str = str(fetchedPoints['points'])
                    return Response({points_str})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Failed to decode JSON data'}, status=500)