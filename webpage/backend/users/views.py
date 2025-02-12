# # users/views.py
# import bcrypt
# import json
# import os
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework import status
# from .serializers import UserSignupSerializer, UserLoginSerializer, UserProfileSerializer, TeamSerializer
# from mongoUsers import get_database


# def load_user_data(username):
#     try:
#         db = get_database('usersData')
#         userCollection = db['userCollection']
#         user = userCollection.find_one({'username': username}, {'username':1, 'password':1, 'email':1, 'points':1, 'team':1, 'message':1, '_id':0,})
#         if user:
#             return user
#         else:
#             return None
#     except Exception as e:
#         print(f"Error loading user data: {e}")
#         return None
    
# # Login API
# @api_view(['POST'])
# def login(request):
#     if request.method == 'POST':
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']
            
#             user_data = load_user_data(username)
#             if user_data:
#                 stored_password = user_data['password']
#                 if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
#                     return Response({'detail': 'Login successful.'}, status=status.HTTP_200_OK)
#             return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # Signup API
# @api_view(['POST'])
# def signup(request):
#     if request.method == 'POST':
#         serializer = UserSignupSerializer(data=request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data['username'].capitalize() 
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']
#             confirm_password = serializer.validated_data['confirm_password']
            
#             if password != confirm_password:
#                 return Response({'detail': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

#             if load_user_data(username):
#                 return Response({'detail': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

#             hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

#             user_data = {
#                 'username': username,
#                 'email': email,
#                 'password': hashed_password,
#                 'points': 0, 
#                 'team': None,
#                 'message': None
#             }

#             db = get_database('usersData')
#             userCollection = db['userCollection']
            
#             userCollection.insert_one(user_data)

#             # Return a response indicating success
#             return Response({'detail': 'User created successfully.'}, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # Profile API
# @api_view(['GET'])
# def profile(request):
#     username = request.query_params.get('username')
#     if username:
#         user_data = load_user_data(username)
#         if user_data:
#             serializer = UserProfileSerializer(user_data)
#             return Response(serializer.data)
#         return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
#     return Response({'detail': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)

# # create Team API
# @api_view(['POST'])
# def createTeam(request):
#     if request.method == 'POST':
#         teamName = request.data.get('teamName')
#         username = request.data.get('username')

#         mydb = get_database('usersData')
#         mycol = mydb.get_collection('userCollection')

#         data_username = mycol.find_one({'username': username}, {'username': 1, 'team': 1, 'points': 1, '_id': 0})
#         all_teamNames = mycol.find({}, {'team': 1, '_id': 0})
#         all_teamNames = [team['team'] for team in all_teamNames if team['team'] is not None]

#         userTeam = mydb.get_collection('userTeam')

#         if data_username:
#             if data_username['team'] is not None:
#                 return Response({'detail': 'You already have a team. Leave your current team to create a new one.'}, 
#                                 status=status.HTTP_400_BAD_REQUEST)
#             elif teamName in all_teamNames:
#                 return Response({'detail': 'This team already exists. Please create another.'}, 
#                                 status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 mycol.update_one({'username': username}, {'$set': {'team': teamName}})
#                 userTeam.insert_one({
#                     'TeamName': teamName,
#                     'leaderName': username,
#                     'points': data_username['points'],
#                     'members': None,
#                     'requests': None
#                 })
#                 return Response({'detail': 'Team created successfully.'}, status=status.HTTP_201_CREATED)

#         return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

#     return Response({'detail': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)


# # Team API
# @api_view(['POST'])
# def joinTeam(request):
#     if request.method == 'POST':
#         teamName = request.data.get('teamName')
#         username = request.data.get('username')
        
#         mydb = get_database('usersData')
#         teamCollection = mydb.get_collection('userTeam')
        
#         collected_team = teamCollection.find_one({'TeamName': teamName}, {'TeamName': 1, 'leaderName': 1, 'request': 1, '_id': 0})
        
#         mycol = mydb.get_collection('userCollection')
#         data_username = mycol.find_one({'username': username}, {'username': 1, 'team': 1, 'points': 1, '_id': 0})
        
#         if data_username:
#             if data_username['team'] is not None:
#                 return Response({'detail': 'You are already part of a team.'}, status=status.HTTP_400_BAD_REQUEST)
            
#             if collected_team:
#                 join_request = {
#                     'username': username,
#                     'teamName': teamName,
#                     'points': data_username['points'],
#                     'status': 'pending',
#                 }
                
#                 if 'request' in collected_team:
#                     requests_col = mydb.get_collection('userTeam')
#                     requests_col.update_one(
#                         {'TeamName': teamName},
#                         {'$push': {'request': join_request}}
#                     )
#                 else:
#                     requests_col = mydb.get_collection('userTeam')
#                     requests_col.update_one(
#                         {'TeamName': teamName},
#                         {'$set': {'request': [join_request]}}
#                     )
                
#                 mycol.update_one({'username': username}, {'$set': {'message': f'{teamName}'}})
                
#                 return Response({'detail': 'Join request sent. Waiting for approval.'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'detail': 'Team not found.'}, status=status.HTTP_404_NOT_FOUND)
#     return Response({'detail': 'Method incorrect'}, status=status.HTTP_400_BAD_REQUEST)


# #Revoke request API
# @api_view(['POST'])
# def deleteRequest(request):
#     if request.method == 'POST':
#         teamName = request.data.get('teamName')
#         username = request.data.get('username')
        
#         mydb = get_database('usersData')
#         userTeam_col = mydb.get_collection('userTeam')
#         mycol = mydb.get_collection('userCollection')
        
#         team = userTeam_col.find_one({'TeamName': teamName, 'request.username': username, 'request.status': 'pending'})
        
#         if team:
#             userTeam_col.update_one(
#                 {'TeamName': teamName},
#                 {'$pull': {'request': {'username': username}}}
#             )
#             mycol.update_one({'username': username}, {'$set': {'message': None}})
#             return Response({'detail': 'Join request successfully revoked.'}, status=status.HTTP_200_OK)
        
#         return Response({'detail': 'No pending join request found for this user.'}, status=status.HTTP_404_NOT_FOUND)
    
#     return Response({'detail': 'Method incorrect'}, status=status.HTTP_400_BAD_REQUEST)

# #fetch Team details API
# @api_view(['GET'])
# def fetchTeamDetails(request):
#     if request.method =='GET':
#         teamName = request.query_params.get('teamName')
        
#         if not teamName:
#             return Response({'detail': 'teamName is required'}, status=status.HTTP_400_BAD_REQUEST)
        
#         mydb =get_database('usersData')
#         team_coll = mydb.get_collection('userTeam')
#         teamData = team_coll.find_one({'TeamName': teamName}, {'TeamName':1, 'leaderName':1, 'points':1, 'members':1, 'request':1, '_id':0})
#         if teamData:
#             serializer = TeamSerializer(teamData)
#             return Response(serializer.data)
#     return Response({'detail': 'Method incorrect'}, status=status.HTTP_400_BAD_REQUEST)

# # Team API - Leader's approval functionality
# @api_view(['POST'])
# def leaderApproval(request):
#     if request.method == 'POST':
#         userTeam = request.data.get('userTeam')  # The team to which the user wants to join
#         username = request.data.get('username')  # The username of the user whose request is to be approved
#         teamLeader = request.data.get('teamLeader')
#         teamPoints = request.data.get('teamPoints')
#         currentUser = request.data.get('currentUser')

#         if not userTeam or not username or not teamLeader:
#             return Response({'detail': 'Missing team, username, or team leader in request.'}, status=status.HTTP_400_BAD_REQUEST)

#         # Database connections
#         mydb = get_database('usersData')
#         team_col = mydb.get_collection('userTeam')
#         user_col = mydb.get_collection('userCollection')

#         # Retrieve the requested team data
#         userRequested_Team = team_col.find_one({'TeamName': userTeam, 'leaderName': teamLeader}, {'TeamName': 1, 'leaderName': 1, 'request': 1, 'members': 1, 'points': 1, '_id': 0})

#         if not userRequested_Team:
#             return Response({'detail': 'You are not permitted to accept this request'}, status=status.HTTP_404_NOT_FOUND)

#         # Check if the requester is the actual team leader
#         if userRequested_Team['leaderName'] != currentUser:
#             return Response({'detail': 'Only the team leader can approve or reject this request.'}, status=status.HTTP_403_FORBIDDEN)

#         # Check for the pending request in the team's 'request' array
#         pending_request = None
#         for request_item in userRequested_Team.get('request', []):
#             if request_item['username'] == username and request_item['status'] == 'pending':
#                 pending_request = request_item
#                 break

#         if not pending_request:
#             return Response({'detail': 'No pending join request found for this user.'}, status=status.HTTP_404_NOT_FOUND)

#         # Accept the request: Update the 'members' array and points
#         new_points = teamPoints + userRequested_Team.get('points', 0)

#         # Update team data: If 'members' is None, initialize it with the new username
#         if userRequested_Team.get('members') is None :
#             join_request = {
#                     'username': username,
#                     'points': userRequested_Team.get('points',0)
#                 }
#             team_col.update_one(
#                 {'TeamName': userTeam, 'leaderName': teamLeader},
#                 {'$set': {'members': [join_request], 'points': new_points}, '$pull': {'request': {'username': username}}}
#             )
#         else:
#             join_request = {
#                     'username': username,
#                     'points': userRequested_Team.get('points',0)
#                 }
#             team_col.update_one(
#                 {'TeamName': userTeam, 'leaderName': teamLeader},
#                 {'$push': {'members': join_request}, '$set': {'points': new_points}, '$pull': {'request': {'username': username}}}
#             )

#         # Update the user data: Assign the team and clear the message
#         user_col.update_one({'username': username}, {'$set': {'team': userTeam, 'message': None}})
        
#         return Response({'detail': 'User successfully added to the team.'}, status=status.HTTP_200_OK)

#     return Response({'detail': 'Method incorrect'}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def rejectPendingRequest(request):
#     if request.method == 'POST':
#         userTeam = request.data.get('userTeam')
#         username = request.data.get('username')
#         teamLeader = request.data.get('teamLeader')
#         currentUser = request.data.get('currentUser')

#         if not userTeam or not username or not teamLeader:
#             return Response({'detail': 'Missing team, username, or team leader in request.'}, status=status.HTTP_400_BAD_REQUEST)

#         mydb = get_database('usersData')
#         team_col = mydb.get_collection('userTeam')
#         user_col = mydb.get_collection('userCollection')

#         # Retrieve the requested team data
#         userRequested_Team = team_col.find_one({'TeamName': userTeam, 'leaderName': teamLeader}, {'TeamName': 1, 'leaderName': 1, 'request': 1, '_id': 0})

#         if not userRequested_Team:
#             return Response({'detail': 'You are not permitted to reject this request'}, status=status.HTTP_404_NOT_FOUND)

#         # Check if the requester is the actual team leader
#         if userRequested_Team['leaderName'] != currentUser:
#             return Response({'detail': 'Only the team leader can reject this request.'}, status=status.HTTP_403_FORBIDDEN)

#         # Find the join request in the team's 'request' array
#         join_request = None
#         for request_item in userRequested_Team.get('request', []):
#             if request_item['username'] == username and request_item['status'] == 'pending':
#                 join_request = request_item
#                 break

#         if not join_request:
#             return Response({'detail': 'No pending join request found for this user.'}, status=status.HTTP_404_NOT_FOUND)

#         # Reject the request: Update the status to 'rejected'
#         team_col.update_one({'TeamName': userTeam, 'leaderName': teamLeader}, {'$pull': {'request': {'username': username}}})
#         user_col.update_one({'username': username}, {'$set': {'message': None}})

#         return Response({'detail': 'Join request successfully rejected.'}, status=status.HTTP_200_OK)

#     return Response({'detail': 'Method incorrect'}, status=status.HTTP_400_BAD_REQUEST)

