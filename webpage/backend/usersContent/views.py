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
        user_data = []
        myDatabase = get_database('usersData')
        myCollection = myDatabase['userCollection']
        for collection in myCollection.find({}, {'username':1, 'points':1, '_id': 0}):
            user_data.append({
                'username': collection['username'],
                'points': collection['points']
                })
        return user_data
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
def load_team(request):
    if request.method == 'GET':
        username = request.GET.get('username')  

        if not username:
            return JsonResponse({'error': 'Username parameter is required'}, status=400)

        db = get_database('usersData')
        usercollection = db['usercollection']
        user = usercollection.find_one({'username': username},{'_id':0, 'username':1, 'points':1})
        if user:
            return Response({user.get('points', 0)}) 
        else:
            return JsonResponse({'error': 'User not found'}, status=404)