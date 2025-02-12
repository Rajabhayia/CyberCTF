from ..mongoUsers import get_database

def load_user_data(username):
    try:
        db = get_database('usersData')
        userCollection = db['userCollection']
        user = userCollection.find_one({'username': username}, {'username':1, 'password':1, 'email':1, 'points':1, 'team':1, 'message':1, '_id':0,})
        if user:
            return user
        else:
            return None
    except Exception as e:
        print(f"Error loading user data: {e}")
        return None