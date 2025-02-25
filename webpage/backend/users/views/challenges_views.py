from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework import status
from ..mongoUsers import get_database

class ChallengeService:
    def __init__(self, username ):
        self.db = get_database('usersData')
        self.userCollection = self.db['userCollection']
        self.userTeam = self.db['userTeam']
        
        self.db1 = get_database('challengesData')
        self.challenges = self.db1['challenges']
        self.flags = self.db1['flags']
        self.username = username
        
        self.user_data = self.get_user_data()
        self.correct_flags = self.solvedQuestions()
        
    def get_user_data(self):
        if self.username:
            user_data = self.userCollection.find_one(
                {'username': self.username}, 
                {'points':1, 'team':1, 'correct':1, '_id':0}
            )
            return user_data
        return None
    
    def get_team_data(self, TeamName):
        if TeamName:
            team_data = self.userTeam.find_one(
                {'TeamName': TeamName},
                {'leaderName':1, 'points':1, 'members':1, '_id':0}
            )
            return team_data
        return None


    def solvedQuestions(self):
        try:
            if self.username:
                correct_flags = self.user_data.get('correct')
                return correct_flags
        except:
            if self.user_data == {}:
                correct_flags = self.user_data.get('correct')
                return correct_flags
        return None
    
    def load_flag(self, challenge_id, flag):
        try:
            flag_data = self.flags.find_one({challenge_id: flag})
            
            if flag_data:
                return True
            return False

        except Exception as e:
            print(f"Error occured: {e}")
            return False


@api_view(['GET'])
def load_topics(request):
    if request.method == 'GET':
        username = request.query_params.get('userName')
        
        challenge_services = ChallengeService(username)

        challenges_data = list(challenge_services.challenges.find())
        correct_flags = challenge_services.solvedQuestions()
        
        challenge_id = []
        
        if correct_flags:
            for correct_flag in correct_flags:
                for key, value in correct_flag.items():
                    challenge_id.append(value)

        for challenge in challenges_data:
            challenge.pop('_id', None)
        return Response({'data': challenges_data, 'solved': challenge_id}, status=200)


class BurstRateThrottle(UserRateThrottle):
    rate = '5/minute'


@api_view(['POST'])
@throttle_classes([BurstRateThrottle])
def checkFlag(request):
    if request.method == 'POST':
        username = request.data.get('username')
        challenge_id = request.data.get('challengeID')
        flag = request.data.get('flag')
        challenge_services = ChallengeService(username)

        if not username:
            return Response({'detail': 'Login first'}, status=status.HTTP_401_UNAUTHORIZED)

        if not challenge_id or not flag:
            return Response({'detail': 'Missing challengeID or flag'}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(challenge_id, str) or not isinstance(flag, str):
            return Response({'detail': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_data = challenge_services.user_data
        for keys, values in user_data.items():
            if keys == 'points':
                possedPoints = values
            if keys == 'team':
                if values is None:
                    return Response({'detail': 'Create or join a team first'}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    TeamName = values
                
        team_data = challenge_services.get_team_data(TeamName)
        for key, value in team_data.items():
            if key == 'points':
                teamPoints = value
            if key =='leaderName':
                leaderName = value
        
        members = challenge_services.userTeam.find_one({'members.username': username})
        leaders = challenge_services.userTeam.find_one({'leaderName': leaderName} )
        if members:
            for member in members['members']:
                if member['username'] == username:
                    memberPoints = member['points']
        elif leaders :
            for leader in leaders['members']:
                if leader['username'] == username:
                    memberPoints = leader['points']
        else:
            print(members, username)
            return Response({'detail': 'Create or join a team first'}, status=status.HTTP_401_UNAUTHORIZED)

        if challenge_id and flag and username:
            is_valid_flag = challenge_services.load_flag(challenge_id, flag)

            if is_valid_flag:
                correct = {
                    'challenged_id': challenge_id,
                }
                newPoints = possedPoints + 5
                newTeamPoints = teamPoints + 5
                try:
                    newMemberPoints = memberPoints + 5
                except:
                    newMemberPoints = 0
                solved = challenge_services.user_data
                correct_flags = solved.get('correct')
                if correct_flags is None:
                    challenge_services.userCollection.update_one(
                        {'username': username},
                        {'$set': {'correct': []}}  # Set 'correct' to an empty array if it's None
                    ) 
                    correct_flags = []
                    
                correct_flags.append(correct)
                
                challenge_services.userCollection.update_one(
                    {'username': username},
                    {'$push': {'correct': correct}, '$set': {'points': newPoints}}
                )
                challenge_services.userTeam.update_one(
                    {'TeamName': TeamName},
                    {'$set': {'points': newTeamPoints}}
                )
                challenge_services.userTeam.update_one(
                    {'members.username': username},
                    {'$set': {'members.$.points': newMemberPoints}}
                )
                return Response({'detail': 'Correct'}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid Flag'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Missing challengeID or flag'}, status=status.HTTP_400_BAD_REQUEST)
