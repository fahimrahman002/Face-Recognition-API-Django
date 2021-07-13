from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def authenticate_google_drive():
    gauth = GoogleAuth()
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)
    return drive

google_drive=authenticate_google_drive()