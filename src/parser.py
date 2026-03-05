import re
import logging

logger = logging.getLogger(__name__)

def parse_receipt(body):
    """
    Extract transaction fields from Yucho debit email body.
    Returns a dictionary with all fields, or None if parsing fails.
    """
    try:
        date_match = re.search(r'利用日時\s+(\d{4}/\d{2}/\d{2})\s+(\d{2}:\d{2}:\d{2})', body)
        store_match = re.search(r'利用店舗\s+(.+)', body)
        amount_match = re.search(r'利用金額\s+([-\d,]+)円', body)
        currency_match = re.search(r'利用通貨\s+(\w+)', body)
        approval_match = re.search(r'承認番号\s+(\d+)', body)

        if not all([date_match, store_match, amount_match, currency_match, approval_match]):
            logger.warning("Could not parse all fields from email body")
            return None

        return {
            'date': date_match.group(1),
            'time': date_match.group(2),
            'store': store_match.group(1).strip(),
            'amount': int(amount_match.group(1).replace(',', '').replace('-', '')),
            'currency': currency_match.group(1),
            'approval_no': approval_match.group(1)
        }
    except Exception as e:
        logger.error(f"Error parsing receipt: {e}")
        return None