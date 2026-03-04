import gspread
from google.oauth2.service_account import Credentials
import os

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

SHEET_NAME = 'Receipt Tracker'
CREDENTIALS_FILE = 'google_credentials.json'

def get_sheet():
    creds = Credentials.from_service_account_file(
        CREDENTIALS_FILE, 
        scopes=SCOPES
    )
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    return sheet

def is_duplicate(sheet, approval_no, date):
    """Check if this receipt already exists in the sheet"""
    records = sheet.get_all_records()
    for record in records:
        if (str(record.get('Approval No')) == str(approval_no) and 
            str(record.get('Date')) == str(date)):
            return True
    return False

def append_receipt(receipt):
    """Append a single receipt to Google Sheets if not duplicate"""
    sheet = get_sheet()
    
    if is_duplicate(sheet, receipt['approval_no'], receipt['date']):
        print(f"⏭️  Skipping duplicate: {receipt['store']} on {receipt['date']}")
        return False
    
    row = [
        receipt['date'],
        receipt['time'],
        receipt['store'],
        receipt['amount'],
        receipt['currency'],
        receipt['approval_no']
    ]
    
    sheet.append_row(row)
    print(f"✅ Saved: {receipt['store']} ¥{receipt['amount']} on {receipt['date']}")
    return True

if __name__ == "__main__":
    # Test with sample data
    test_receipt = {
        'date': '2026/03/03',
        'time': '16:59:01',
        'store': 'LAWSON',
        'amount': 293,
        'currency': 'JPY',
        'approval_no': '110020'
    }
    
    print("Testing Google Sheets connection...")
    append_receipt(test_receipt)
    print("Done!")