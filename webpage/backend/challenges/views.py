import json
from django.http import JsonResponse
from django.conf import settings
import os
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework import status
from mongo import get_database


def solvedQuestions(username):
    if username:
        db = get_database('usersData')
        usersColl = db['userCollection']
        correct_flags = usersColl.find_one(
            {'username': username}, {'correct': 1, '_id': 0})
        return correct_flags


@api_view(['GET'])
def load_topics(request):
    if request.method == 'GET':
        username = request.query_params.get('userName')
        db = get_database('challengesData')
        collection = db['challenges']

        challenges_data = list(collection.find())
        correct_flags = solvedQuestions(username)
        
        challenge_id = []
        
        if correct_flags and correct_flags.get('correct') is not None:
            for keys, values in correct_flags.items():
                for valued in values:
                    for key, value in valued.items():
                        challenge_id.append(value)

        for challenge in challenges_data:
            challenge.pop('_id', None)
        return Response({'data': challenges_data, 'solved': challenge_id}, status=200)


def load_flag(challenge_id, flag):
    try:
        db = get_database('challengesData')
        collection = db['flags']
        flags_data = list(collection.find())

        for challenge_data in flags_data:
            challenge_data.pop('_id', None)
            for category, flags in challenge_data.items():
                if challenge_id in flags:
                    if flags[challenge_id] == flag:
                        return True

        return False

    except Exception as e:
        print(f"Error occured: {e}")
        return False


class BurstRateThrottle(UserRateThrottle):
    rate = '5/minute'


@api_view(['POST'])
@throttle_classes([BurstRateThrottle])
def checkFlag(request):
    if request.method == 'POST':
        username = request.data.get('username')
        challenge_id = request.data.get('challengeID')
        flag = request.data.get('flag')

        if not username:
            return Response({'detail': 'Login first'}, status=status.HTTP_401_UNAUTHORIZED)

        if not challenge_id or not flag:
            return Response({'detail': 'Missing challengeID or flag'}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(challenge_id, str) or not isinstance(flag, str):
            return Response({'detail': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)
        
        db = get_database('usersData')
        usersColl = db['userCollection']
        userTeam = db['userTeam']
        points = usersColl.find_one({'username': username}, {'points':1, 'team':1, "_id":0})
        for keys, values in points.items():
            if keys == 'points':
                possedPoints = values
            if keys == 'team':
                if values is None:
                    return Response({'detail': 'Create or join a team first'}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    TeamName = values
                
        team = userTeam.find_one({'TeamName': TeamName}, {'points':1, 'members':1, '_id':0})
        for key, value in team.items():
            if key == 'points':
                teamPoints = value
        
        members = userTeam.find_one({'members.username': username})
        if members:
            for member in members['members']:
                if member['username'] == username:
                    memberPoints = member['points']
        else:
            return Response({'detail': 'Create or join a team first'}, status=status.HTTP_401_UNAUTHORIZED)

        if challenge_id and flag and username:
            is_valid_flag = load_flag(challenge_id, flag)

            if is_valid_flag:
                correct = {
                    'challenged_id': challenge_id,
                }
                newPoints = possedPoints + 5
                newTeamPoints = teamPoints + 5
                newMemberPoints = memberPoints + 5
                solved = solvedQuestions(username)
                for key, value in solved.items():
                    if key == 'correct':
                        if value is None:
                            usersColl.update_one(
                                {'username': username},
                                {'$set': {'correct': [correct], 'points': newPoints}}
                            )
                            userTeam.update_one(
                                {'TeamName': TeamName},
                                {'$set': {'points': newTeamPoints}}
                            )
                            userTeam.update_one(
                                {'members.username': username},
                                {'$set': {'members.$.points': newMemberPoints}}
                            )
                        else:
                            usersColl.update_one(
                                {'username': username},
                                {'$push': {'correct': correct}, '$set': {'points': newPoints}}
                            )
                            userTeam.update_one(
                                {'TeamName': TeamName},
                                {'$set': {'points': newTeamPoints}}
                            )
                            userTeam.update_one(
                                {'members.username': username},
                                {'$set': {'members.$.points': newMemberPoints}}
                            )
                return Response({'detail': 'Correct'}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid Flag'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Missing challengeID or flag'}, status=status.HTTP_400_BAD_REQUEST)
