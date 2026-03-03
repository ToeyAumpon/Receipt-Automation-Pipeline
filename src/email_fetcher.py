from O365 import Account, FileSystemTokenBackend
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

credentials = (CLIENT_ID, CLIENT_SECRET)

def get_account():
    token_backend = FileSystemTokenBackend(
        token_path='.', 
        token_filename='o365_token.txt'
    )
    account = Account(
        credentials,
        auth_flow_type='authorization',
        tenant_id='consumers',
        token_backend=token_backend,
        redirect_uri='https://login.microsoftonline.com/common/oauth2/nativeclient'
    )
    return account

def authenticate():
    account = get_account()
    if not account.is_authenticated:
        account.authenticate(scopes=['basic', 'message_all'])
    return account

if __name__ == "__main__":
    print("Testing connection...")
    account = authenticate()
    print("Connected successfully!")