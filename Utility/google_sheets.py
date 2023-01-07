import gspread
from google.oauth2.service_account import Credentials
import os
from kivy import Logger
from collections import OrderedDict
import pathlib

SAMPLE_SPREADSHEET_ID = '1D6D-jEE5cBvrPABljLZla5d1NtjOhmCR76ymPgNN3r0'
TOKEN_FILE = pathlib.Path('gsheets_key.json')

features_name_to_sheets_columns_map = OrderedDict({
    'Session date': 'O',
    'Session name': 'N',


    'Tree Number': 'M',
    'Tree specie': 'L',
    'Stem number': 'K',
    'Tree diameter': 'J',
    'Crown diameter': 'I',
    'Tree height': 'H',

    'Health condition': 'G',
    'Tree location': 'F',

    'Crown value': 'E',
    'Specie value': 'D'


})


def auth_in_gsheets() -> gspread.client:
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


def receive_client_sheet_by_id(client=None, sheet_key=SAMPLE_SPREADSHEET_ID) -> gspread.spreadsheet:
    if client:
        return client.open_by_key(sheet_key)
    else:
        client = auth_in_gsheets()
        return client.open_by_key(sheet_key)


def get_g_sheet_client_sheet_list(client):
    return client.worksheets()




