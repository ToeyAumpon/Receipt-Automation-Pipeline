from O365 import Account, FileSystemTokenBackend
import os
from dotenv import load_dotenv
from parser import parse_receipt

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

    results = []
    for message in messages:
        body = message.body_preview
        parsed = parse_receipt(body)
        if parsed:
            print(f"✅ Parsed: {parsed}")
            results.append(parsed)
        else:
            print(f"❌ Could not parse: {message.subject}")
    
    return results

if __name__ == "__main__":
    print("Fetching and parsing emails...")
    data = get_receipt_emails()
    print(f"\nTotal parsed: {len(data)} receipts")