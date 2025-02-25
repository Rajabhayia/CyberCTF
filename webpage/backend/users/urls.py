# users/urls.py
from django.urls import path
from .views import login, signup, profile
from .views import createTeam, joinTeam, leaderApproval, rejectPendingRequest
from .views import fetchTeamDetails, deleteRequest, handleRemoval
from .views import load_topics, checkFlag

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
    path('createTeam/', createTeam, name='createTeam'),
    path('fetchTeamDetails/', fetchTeamDetails, name='fetchTeamDetails'),
    path('joinTeam/', joinTeam, name='joinTeam'),
    path('leaderApproval/', leaderApproval, name='leaderApproval'),
    path('deleteRequest/', deleteRequest, name='deleteRequest'),
    path('rejectPendingRequest/', rejectPendingRequest, name='rejectPendingRequest'),
    path('handleRemoval/', handleRemoval, name='handleRemoval' ),
    path('challengesData/', load_topics, name='load_topics'),
    path('checkFlag/', checkFlag, name='checkFlag' ),
]
