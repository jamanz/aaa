import gspread
import os

print(os.path)
print(os.environ['APPDATA'])
gc = gspread.oauth()#credentials_filename='./credentials.json')
print(gc.list_spreadsheet_files())
sh = gc.open("agroTable")

print(sh.sheet1)