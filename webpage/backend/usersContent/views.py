import json
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
from mongo import get_database


# Helper function to load all usernames from the data directory
def load_all_usernames():
    try:
        usernames = []
        db = get_database('usersData')
        collection_names = db.list_collection_names()
        for collection in collection_names:
            usernames.append(collection)
        return usernames
    except Exception as e:
        return str(e)


# API View to load all users
@api_view(['GET'])
def load_users(request):
    try:
        if request.method == "GET":
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
        username = request.GET.get('username')  

        if not username:
            return JsonResponse({'error': 'Username parameter is required'}, status=400)

        db = get_database('usersData')
        usersContent = db[username]

        try:
            user_Data = list(usersContent.find())
            for data in user_Data:
                data.pop('_id', None)
            
            if user_Data:
                points = user_Data[0].get('points', 0)
                return Response({points})
            else:
                return JsonResponse({'error': 'User not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Failed to decode JSON data'}, status=500)