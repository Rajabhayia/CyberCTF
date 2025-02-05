import json
from django.http import JsonResponse
from django.conf import settings
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def load_topics(request):
    file_path = os.path.join(settings.BASE_DIR, 'challengesData', 'challenges.json')

    with open(file_path, 'r') as f:
        topics_data = json.load(f)
    return JsonResponse(topics_data, safe=False)


def load_flag(challenge_id, flag):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'challengesData', 'flags.json')
        with open(file_path, 'r') as f:
            flags_data = json.load(f)

        for challenge in flags_data:
            for category, flags in challenge.items():
                if challenge_id in flags:
                    if flags[challenge_id] == flag:
                        return True 

        return False

    except FileNotFoundError:
        return None 

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
