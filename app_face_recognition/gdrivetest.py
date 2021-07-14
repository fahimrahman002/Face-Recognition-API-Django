from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)

file1 = drive.CreateFile({'parents': [{'id': '1T_4PMG_3a7-nfHfO4qzTT7N0ZYR_yhGz'}],'title': 'Hello2.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
file1.SetContentString('Hello World!') # Set content of the file from given string.
file1.Upload()