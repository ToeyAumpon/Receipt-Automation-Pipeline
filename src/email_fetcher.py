from O365 import Account, FileSystemTokenBackend
import os
import sys
import logging
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from parser import parse_receipt
from sheets_writer import append_receipt

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
credentials = (CLIENT_ID, )

def get_account():
    try:
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
    except Exception as e:
        logger.error(f"Error connecting to Outlook: {e}")
        raise

def get_receipt_emails():
    account = get_account()
    mailbox = account.mailbox()
    yucho_folder = mailbox.get_folder(folder_name='Yucho')
    messages = yucho_folder.get_messages(limit=50)

    saved = 0
    skipped = 0
    failed = 0

    for message in messages:
        try:
            body = message.body_preview
            parsed = parse_receipt(body)
            if parsed:
                result = append_receipt(parsed)
                if result:
                    saved += 1
                else:
                    skipped += 1
            else:
                logger.warning(f"Could not parse email: {message.subject}")
                failed += 1
        except Exception as e:
            logger.error(f"Error processing email: {e}")
            failed += 1

    logger.info(f"Run complete — Saved: {saved}, Skipped: {skipped}, Failed: {failed}")
    print(f"\n✅ Saved: {saved} new receipts")
    print(f"⏭️  Skipped: {skipped} duplicates")
    print(f"❌ Failed: {failed} emails")

if __name__ == "__main__":
    logger.info("Starting receipt fetch...")
    print("Fetching and saving receipts...")
    get_receipt_emails()
    print("Done!")