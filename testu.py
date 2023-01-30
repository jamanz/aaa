import gspread
import os
from google.oauth2.credentials import Credentials
from google.oauth2.credentials import UserAccessTokenCredentials
from pathlib import Path
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# print(os.path)
# print(os.listdir(os.environ['APPDATA']))

DEFAULT_SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

cred_path = Path('config')
print('step1')
print('step2')
gc = gspread.oauth(
    scopes=DEFAULT_SCOPES,
    credentials_filename=str(cred_path.joinpath('credentials.json')),
    authorized_user_filename=str(cred_path.joinpath('authorized_user.json'))

)#credentials_filename='./credentials.json')
# print(gc.list_spreadsheet_files())
sh = gc.open("agroTablez")

with open(cred_path.joinpath('authorized_user.json')) as file:
    data = json.load(file)
    # print(data)

creds = Credentials.from_authorized_user_info(info=data, scopes=["https://www.googleapis.com/auth/userinfo.email"])
email_service = build('oauth2', 'v2', credentials=creds)
user_info = email_service.userinfo().get().execute()
print(user_info)
