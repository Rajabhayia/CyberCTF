import json
from django.http import JsonResponse
from django.conf import settings
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .mongo import get_database

@api_view(['GET'])
def load_topics(request):
    db = get_database('challengesData')
    collection = db['challenges']
    
    #fetching all challenges in collection
    challenges_data = list(collection.find())
    
    for challenge in challenges_data:
        challenge.pop('_id', None)
    
    return JsonResponse(challenges_data, safe=False)


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

@api_view(['POST'])
def checkFlag(request):
    if request.method == 'POST':
        challenge_id = request.data.get('challengeID')
        flag = request.data.get('flag')

        if challenge_id and flag:
            is_valid_flag = load_flag(challenge_id, flag)
            if is_valid_flag:
                return Response({'detail': 'Correct'}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid Flag'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Missing challengeID or flag'}, status=status.HTTP_400_BAD_REQUEST)
