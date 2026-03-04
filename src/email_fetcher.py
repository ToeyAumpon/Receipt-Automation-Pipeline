from O365 import Account, FileSystemTokenBackend
import os
import sys
from dotenv import load_dotenv

# Add src to path so we can import parser
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from parser import parse_receipt
from sheets_writer import append_receipt

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")

credentials = (CLIENT_ID, )

def get_account():
    token_backend = FileSystemTokenBackend(
        token_path='.', 
        token_filename='o365_token.txt'
    )
    account = Account(
        credentials,
        auth_flow_type='public',
        tenant_id='consumers',
        token_backend=token_backend
    )
    return account

def get_receipt_emails():
    account = get_account()
    mailbox = account.mailbox()
    yucho_folder = mailbox.get_folder(folder_name='Yucho')
    messages = yucho_folder.get_messages(limit=10)

    saved = 0
    skipped = 0

    for message in messages:
        body = message.body_preview
        parsed = parse_receipt(body)
        if parsed:
            result = append_receipt(parsed)
            if result:
                saved += 1
            else:
                skipped += 1
        else:
            print(f"❌ Could not parse: {message.subject}")

    print(f"\n✅ Saved: {saved} new receipts")
    print(f"⏭️  Skipped: {skipped} duplicates")

if __name__ == "__main__":
    print("Fetching and saving receipts...")
    get_receipt_emails()
    print("Done!")