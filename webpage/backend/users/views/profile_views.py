# users/profile_views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..serializers import UserProfileSerializer
from ..mongoUsers import get_database
from .utils import load_user_data

# Profile API
@api_view(['GET'])
def profile(request):
    username = request.query_params.get('username')
    if username:
        user_data = load_user_data(username)
        if user_data:
            serializer = UserProfileSerializer(user_data)
            return Response(serializer.data)
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'detail': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)

