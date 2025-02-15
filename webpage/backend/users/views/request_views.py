# users/request_views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..serializers import TeamSerializer
from ..mongoUsers import get_database


# Team API - Leader's approval functionality
@api_view(['POST'])
def leaderApproval(request):
    if request.method == 'POST':
        userTeam = request.data.get('userTeam') 
        username = request.data.get('username')  
        teamLeader = request.data.get('teamLeader')
        currentUser = request.data.get('currentUser')

        if not userTeam or not username or not teamLeader:
            return Response({'detail': 'Missing team, username, or team leader in request.'}, status=status.HTTP_400_BAD_REQUEST)

        # Database connections
        mydb = get_database('usersData')
        team_col = mydb.get_collection('userTeam')
        user_col = mydb.get_collection('userCollection')

        # Retrieve the requested team data
        userRequested_Team = team_col.find_one({'TeamName': userTeam, 'leaderName': teamLeader}, {'TeamName': 1, 'leaderName': 1, 'request': 1, 'members': 1, 'points': 1, '_id': 0})
        userPoints = user_col.find_one({'username': username, 'message': userTeam}, {'points':1, '_id':0})
        
        if userPoints:
            userPoint = userPoints.get('points')

        if not userRequested_Team:
            return Response({'detail': 'You are not permitted to accept this request'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the requester is the actual team leader
        if userRequested_Team['leaderName'] != currentUser:
            return Response({'detail': 'Only the team leader can approve or reject this request.'}, status=status.HTTP_403_FORBIDDEN)

        # Check for the pending request in the team's 'request' array
        pending_request = None
        for request_item in userRequested_Team.get('request', []):
            if request_item['username'] == username and request_item['status'] == 'pending':
                pending_request = request_item
                break

        if not pending_request:
            return Response({'detail': 'No pending join request found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        # Accept the request: Update the 'members' array and points
        new_points = userPoint + userRequested_Team.get('points', 0)

        # Update team data: If 'members' is None, initialize it with the new username
        if userRequested_Team.get('members') is None :
            join_request = {
                    'username': username,
                    'points': new_points
                }
            team_col.update_one(
                {'TeamName': userTeam, 'leaderName': teamLeader},
                {'$set': {'members': [join_request], 'points': new_points}, '$pull': {'request': {'username': username}}}
            )
        else:
            join_request = {
                    'username': username,
                    'points': userPoint
                }
            team_col.update_one(
                {'TeamName': userTeam, 'leaderName': teamLeader},
                {'$push': {'members': join_request}, '$set': {'points': new_points}, '$pull': {'request': {'username': username}}}
            )

        # Update the user data: Assign the team and clear the message
        user_col.update_one({'username': username}, {'$set': {'team': userTeam, 'message': None}})
        
        return Response({'detail': 'User successfully added to the team.'}, status=status.HTTP_200_OK)

    return Response({'detail': 'Method incorrect'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def rejectPendingRequest(request):
    if request.method == 'POST':
        userTeam = request.data.get('userTeam')
        username = request.data.get('username')
        teamLeader = request.data.get('teamLeader')
        currentUser = request.data.get('currentUser')

        if not userTeam or not username or not teamLeader:
            return Response({'detail': 'Missing team, username, or team leader in request.'}, status=status.HTTP_400_BAD_REQUEST)

        mydb = get_database('usersData')
        team_col = mydb.get_collection('userTeam')
        user_col = mydb.get_collection('userCollection')

        # Retrieve the requested team data
        userRequested_Team = team_col.find_one({'TeamName': userTeam, 'leaderName': teamLeader}, {'TeamName': 1, 'leaderName': 1, 'request': 1, '_id': 0})

        if not userRequested_Team:
            return Response({'detail': 'You are not permitted to reject this request'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the requester is the actual team leader
        if userRequested_Team['leaderName'] != currentUser:
            return Response({'detail': 'Only the team leader can reject this request.'}, status=status.HTTP_403_FORBIDDEN)

        # Find the join request in the team's 'request' array
        join_request = None
        for request_item in userRequested_Team.get('request', []):
            if request_item['username'] == username and request_item['status'] == 'pending':
                join_request = request_item
                break

        if not join_request:
            return Response({'detail': 'No pending join request found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        # Reject the request: Update the status to 'rejected'
        team_col.update_one({'TeamName': userTeam, 'leaderName': teamLeader}, {'$pull': {'request': {'username': username}}})
        user_col.update_one({'username': username}, {'$set': {'message': None}})

        return Response({'detail': 'Join request successfully rejected.'}, status=status.HTTP_200_OK)

    return Response({'detail': 'Method incorrect'}, status=status.HTTP_400_BAD_REQUEST)

