# users/team_views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..serializers import TeamSerializer
from ..mongoUsers import get_database


# create Team API
@api_view(['POST'])
def createTeam(request):
    if request.method == 'POST':
        teamName = request.data.get('teamName')
        username = request.data.get('username')

        mydb = get_database('usersData')
        mycol = mydb.get_collection('userCollection')

        data_username = mycol.find_one({'username': username}, {'username': 1, 'team': 1, 'points': 1, '_id': 0})
        all_teamNames = mycol.find({}, {'team': 1, '_id': 0})
        all_teamNames = [team['team'] for team in all_teamNames if team['team'] is not None]

        userTeam = mydb.get_collection('userTeam')

        if data_username:
            if data_username['team'] is not None:
                return Response({'detail': 'You already have a team. Leave your current team to create a new one.'}, 
                                status=status.HTTP_400_BAD_REQUEST)
            elif teamName in all_teamNames:
                return Response({'detail': 'This team already exists. Please create another.'}, 
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                mycol.update_one({'username': username}, {'$set': {'team': teamName}})
                userTeam.insert_one({
                    'TeamName': teamName,
                    'leaderName': username,
                    'points': data_username['points'],
                    'members': None,
                    'requests': None
                })
                return Response({'detail': 'Team created successfully.'}, status=status.HTTP_201_CREATED)

        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'detail': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)


# Team API
@api_view(['POST'])
def joinTeam(request):
    if request.method == 'POST':
        teamName = request.data.get('teamName')
        username = request.data.get('username')
        
        mydb = get_database('usersData')
        teamCollection = mydb.get_collection('userTeam')
        
        collected_team = teamCollection.find_one({'TeamName': teamName}, {'TeamName': 1, 'leaderName': 1, 'request': 1, 'members':1, '_id': 0})
        for keys,values in collected_team.items():
            if keys == 'members':
                if len(values) >= 2:
                    return Response({'detail': 'Team full request another team'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        mycol = mydb.get_collection('userCollection')
        data_username = mycol.find_one({'username': username}, {'username': 1, 'team': 1, 'points': 1, '_id': 0})
        
        if data_username:
            if data_username['team'] is not None:
                return Response({'detail': 'You are already part of a team.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if collected_team:
                join_request = {
                    'username': username,
                    'teamName': teamName,
                    'points': data_username['points'],
                    'status': 'pending',
                }
                
                if 'request' in collected_team:
                    requests_col = mydb.get_collection('userTeam')
                    requests_col.update_one(
                        {'TeamName': teamName},
                        {'$push': {'request': join_request}}
                    )
                else:
                    requests_col = mydb.get_collection('userTeam')
                    requests_col.update_one(
                        {'TeamName': teamName},
                        {'$set': {'request': [join_request]}}
                    )
                
                mycol.update_one({'username': username}, {'$set': {'message': f'{teamName}'}})
                
                return Response({'detail': 'Join request sent. Waiting for approval.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Team not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'detail': 'Method incorrect'}, status=status.HTTP_400_BAD_REQUEST)

#fetch Team details API
@api_view(['GET'])
def fetchTeamDetails(request):
    if request.method =='GET':
        teamName = request.query_params.get('teamName')
        
        if not teamName:
            return Response({'detail': 'teamName is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        mydb =get_database('usersData')
        team_coll = mydb.get_collection('userTeam')
        teamData = team_coll.find_one({'TeamName': teamName}, {'TeamName':1, 'leaderName':1, 'points':1, 'members':1, 'request':1, '_id':0})
        if teamData:
            serializer = TeamSerializer(teamData)
            return Response(serializer.data)
    return Response({'detail': 'Method incorrect'}, status=status.HTTP_400_BAD_REQUEST)


#Revoke request API
@api_view(['POST'])
def deleteRequest(request):
    if request.method == 'POST':
        teamName = request.data.get('teamName')
        username = request.data.get('username')
        
        mydb = get_database('usersData')
        userTeam_col = mydb.get_collection('userTeam')
        mycol = mydb.get_collection('userCollection')
        
        team = userTeam_col.find_one({'TeamName': teamName, 'request.username': username, 'request.status': 'pending'})
        
        if team:
            userTeam_col.update_one(
                {'TeamName': teamName},
                {'$pull': {'request': {'username': username}}}
            )
            mycol.update_one({'username': username}, {'$set': {'message': None}})
            return Response({'detail': 'Join request successfully revoked.'}, status=status.HTTP_200_OK)
        
        return Response({'detail': 'No pending join request found for this user.'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({'detail': 'Method incorrect'}, status=status.HTTP_400_BAD_REQUEST)
