# mongo.py
from pymongo import MongoClient
from django.conf import settings

def get_mongo_connection():
    client = MongoClient(settings.MONGO_URI)
    return client

def get_database(database_name):
    client = get_mongo_connection()
    return client[database_name] 
