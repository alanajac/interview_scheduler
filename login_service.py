from os import path
import pickle

def get_calendar_service():
    creds = None
    if path.exists("token.txt"):
        open("token.txt")