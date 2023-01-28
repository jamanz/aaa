import gspread
from google.oauth2.service_account import Credentials

import os
from kivy import Logger
from collections import OrderedDict
import pathlib
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SAMPLE_SPREADSHEET_ID = '1D6D-jEE5cBvrPABljLZla5d1NtjOhmCR76ymPgNN3r0'
TOKEN_FILE = pathlib.Path('gsheets_key.json')

cols_rus = [
 "Заметки",
 "Оценка дерева[шек]",
 "Общая оценка (0-20)",
 "Ценность вида (1-5)",
 "Ценность диаметра кроны(1-5)",
 "Расположение дерева (1-5)",
 "Состояние здоровья (1-5)",
 "Высота (м)",
 "Диаметр кроны дерева (м)",
 "Диаметр дерева (м)",
 "Кол-о стволов",
 "Вид",
 "Номер Дерева",
 "Название сесии",
 "Дата сессии"]

cols_heb = [
    "הערות",
    r"שווי העץ (ש\"ח)",
    "סך ערכיות העץ (0-20)",
    "ערך מין העץ (1-5)",
    "קוטר חופת העץ (1-5)",
    "מיקום העץ (1-5)",
    "מצב בריאותי (0-5)",
    "גובה העץ (מ')",
    "רוחב נוף (מ')",
    "קוטר גזע (מ')",
    "כמות גזעים",
    "סוג עץ",
    "מספר עץ",
    "כותרת הישיבה",
    "תאריך הישיבה"
]



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

DEFAULT_SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

cred_path = pathlib.Path('config')

DEFAULT_WORKSHEET_NAME = 'TreezTable'


def create_new_sheet_with_template(ws: gspread.Worksheet):
    ws.update("A1:O1", [cols_rus])
    ws.update("A2:02", [cols_heb])


def make_oauth():
    gc = gspread.oauth(
        scopes=DEFAULT_SCOPES,
        credentials_filename=str(cred_path.joinpath('credentials.json')),
        authorized_user_filename=str(cred_path.joinpath('authorized_user.json'))

    )
    return gc

def get_worksheet(client: gspread.Client):
    try:
        ws = client.open(DEFAULT_WORKSHEET_NAME)
    except gspread.exceptions.SpreadsheetNotFound:
        client.create(DEFAULT_WORKSHEET_NAME)
        ws = client.open(DEFAULT_WORKSHEET_NAME)
        create_new_sheet_with_template(ws.sheet1)
    return ws.sheet1

def get_user_email():
    with open(cred_path.joinpath('authorized_user.json')) as file:
        data = json.load(file)

    creds = Credentials.from_authorized_user_info(info=data, scopes=["https://www.googleapis.com/auth/userinfo.email"])
    email_service = build('oauth2', 'v2', credentials=creds)
    user_info = email_service.userinfo().get().execute()
    return user_info['email']


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


def next_available_row(worksheet: gspread.Worksheet):
    str_list = list(filter(None, worksheet.col_values(12)))
    return int(len(str_list)+1)


def receive_client_sheet_by_id(client=None, sheet_key=SAMPLE_SPREADSHEET_ID) -> gspread.spreadsheet:
    if client:
        return client.open_by_key(sheet_key)
    else:
        client = auth_in_gsheets()
        return client.open_by_key(sheet_key)


def get_g_sheet_client_sheet_list(client):
    return client.worksheets()




