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
            sortedUsers = sorted(usernames, key=lambda x:x['points'], reverse=True)
            if sortedUsers:
                return Response({'users': sortedUsers}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'No users found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#API views to load points
@api_view(['GET'])
def load_team(request):
    if request.method == 'GET':
        db = get_database('usersData')
        usercollection = db['userTeam']
        team_data = []
        for Teams in usercollection.find({},{'_id':0, 'TeamName':1, 'points':1}):
            team_data.append({
                'TeamName': Teams['TeamName'],
                'points': Teams['points']
             })
        sortedTeams = sorted(team_data, key=lambda x:x['points'], reverse=True)
        if sortedTeams:
            return Response({'teams': sortedTeams}, status=status.HTTP_200_OK) 
        else:
            return Response({'detail': 'No users found.'}, status=status.HTTP_404_NOT_FOUND)
        