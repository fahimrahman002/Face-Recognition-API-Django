from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def authenticate_google_drive():
    gauth = GoogleAuth()

    # Try to load saved client credentials
    gauth.LoadCredentialsFile("credentials.json")

    if gauth.credentials is None:
        # Authenticate if they're not there

        # This is what solved the issues:
        gauth.GetFlow()
        gauth.flow.params.update({'access_type': 'offline'})
        gauth.flow.params.update({'approval_prompt': 'force'})

        gauth.CommandLineAuth()

    elif gauth.access_token_expired:

        # Refresh them if expired

        gauth.Refresh()
    else:

        # Initialize the saved creds

        gauth.Authorize()

    # Save the current credentials to a file
    gauth.SaveCredentialsFile("credentials.json")  

    drive = GoogleDrive(gauth)

    return drive


authenticate_google_drive()

