import gspread
from google.oauth2.service_account import Credentials
import os
from kivy import Logger

SAMPLE_SPREADSHEET_ID = '1D6D-jEE5cBvrPABljLZla5d1NtjOhmCR76ymPgNN3r0'
TOKEN_FILE = 'gsheets_key.json'


def authorize_gsheets():
    scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_service_account_file(TOKEN_FILE, scopes=scope)
    else:
        raise Exception('No Google credentials file specified')

    client = gspread.authorize(creds)

    Logger.info(f"{__name__}: Goggle sheet client auth Success, client: {client}")
    return client


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return int(len(str_list)+1)

def get_g_sheet(client=None, sheet_key=SAMPLE_SPREADSHEET_ID):
    if client:
        return client.open_by_key(sheet_key).sheet1
    else:
        client = authorize_gsheets()
        return client.open_by_key(sheet_key).sheet1

