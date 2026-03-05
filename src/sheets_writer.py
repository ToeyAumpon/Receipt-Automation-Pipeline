import gspread
from google.oauth2.service_account import Credentials
import logging
import os

logger = logging.getLogger(__name__)

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "Receipt Tracker")
CREDENTIALS_FILE = 'google_credentials.json'

def get_sheet():
    try:
        creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE, 
            scopes=SCOPES
        )
        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME).sheet1
        return sheet
    except Exception as e:
        logger.error(f"Error connecting to Google Sheets: {e}")
        raise

def is_duplicate(sheet, approval_no, time):
    """Check if this receipt already exists in the sheet"""
    try:
        records = sheet.get_all_records()
        for record in records:
            if (str(record.get('Approval No')).strip() == str(approval_no).strip() and
                str(record.get('Time')).strip() == str(time).strip()):
                return True
        return False
    except Exception as e:
        logger.error(f"Error checking duplicates: {e}")
        return False

def append_receipt(receipt):
    """Append a single receipt to Google Sheets if not duplicate"""
    try:
        sheet = get_sheet()
        
        if is_duplicate(sheet, receipt['approval_no'], receipt['time']):
            logger.info(f"Skipping duplicate: {receipt['store']} on {receipt['date']}")
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
        logger.info(f"Saved: {receipt['store']} ¥{receipt['amount']} on {receipt['date']}")
        print(f"✅ Saved: {receipt['store']} ¥{receipt['amount']} on {receipt['date']}")
        return True

    except Exception as e:
        logger.error(f"Error saving receipt: {e}")
        print(f"❌ Error saving receipt: {e}")
        return False