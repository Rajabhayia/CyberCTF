# users/fetchTeam_views.py
from ..mongoUsers import get_database
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['POST'])
def handleRemoval(request):
    if request.method == 'POST':
        username = request.data.get('username')
        points = request.data.get('points')
        teamLeader = request.data.get('teamLeader')
        
        # Get MongoDB database collections
        mydb = get_database('usersData')
        userTeam_col = mydb.get_collection('userTeam')
        mycol = mydb.get_collection('userCollection')
        
        # Find team where the user and points match
        team = userTeam_col.find_one({'members.username': username, 'members.points': points})
        
        if team:
            teamName = team.get('TeamName')
            teampoints = team.get('points')
            
            # Find user in the team
            user = mycol.find_one({'username': username, 'points': points, 'team': teamName})
            
            if user:
                # Check if the request is coming from the team leader
                if teamLeader != team.get('leaderName'):
                    return Response({'detail': 'Only Team Leader can remove a member.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                
                # Update team points and remove the user from the members array
                new_points = teampoints - points
                userTeam_col.update_one(
                    {'TeamName': teamName},
                    {'$pull': {'members': {'username': username, 'points': points}}, '$set': {'points': new_points}}
                )
                
                # Remove user from the team in userCollection
                mycol.update_one(
                    {'username': username}, 
                    {'$set': {'team': None}}
                )
                
                return Response({'detail': 'Teammate successfully removed.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'User not found in the team with the given points.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': 'Team not found or user not part of the team.'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({'detail': 'Method incorrect. Please use POST method.'}, status=status.HTTP_400_BAD_REQUEST)
