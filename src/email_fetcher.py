from O365 import Account, FileSystemTokenBackend
import os
from dotenv import load_dotenv

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
    
    # Get the Yucho folder instead of inbox
    yucho_folder = mailbox.get_folder(folder_name='Yucho')
    
    # Fetch last 10 emails
    messages = yucho_folder.get_messages(limit=10)
    
    for message in messages:
        print("---")
        print(f"From: {message.sender}")
        print(f"Subject: {message.subject}")
        print(f"Date: {message.received}")
        print(f"Body preview: {message.body_preview}")

if __name__ == "__main__":
    print("Fetching emails...")
    get_receipt_emails()
    print("Done!")