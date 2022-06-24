from utils.firebase import firebase
import os

FIREBASE_URL = os.environ.get('FIREBASE_URL')

def create_connection():

    base = firebase.FirebaseApplication(FIREBASE_URL, None)
    
    return base

def getAllFeeds():
    b = create_connection()

    com = b.get('/Commentaire', None)

    return com