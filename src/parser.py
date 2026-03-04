import re

def parse_receipt(body):
    """
    Extract transaction fields from Yucho debit email body.
    Returns a dictionary with all fields, or None if parsing fails.
    """

    # Extract date and time
    date_match = re.search(r'利用日時\s+(\d{4}/\d{2}/\d{2})\s+(\d{2}:\d{2}:\d{2})', body)
    
    # Extract store name
    store_match = re.search(r'利用店舗\s+(.+)', body)
    
    # Extract amount (remove yen symbol and commas)
    amount_match = re.search(r'利用金額\s+([-\d,]+)円', body)
    
    # Extract currency
    currency_match = re.search(r'利用通貨\s+(\w+)', body)
    
    # Extract approval number
    approval_match = re.search(r'承認番号\s+(\d+)', body)

    # Check all fields were found
    if not all([date_match, store_match, amount_match, currency_match, approval_match]):
        print("Warning: could not parse all fields")
        return None

    return {
        'date': date_match.group(1),
        'time': date_match.group(2),
        'store': store_match.group(1).strip(),
        'amount': int(amount_match.group(1).replace(',', '').replace('-', '')),
        'currency': currency_match.group(1),
        'approval_no': approval_match.group(1)
    }

if __name__ == "__main__":
    # Test with a sample email body
    test_body = """
    ソンブッド　アンポン 様

    ゆうちょデビットのご利用を受け付けました。

    利用日時  2026/03/03 16:59:01
    利用店舗  LAWSON
    利用金額  293円
    利用通貨  JPY
    承認番号  110020
    """

    result = parse_receipt(test_body)
    print(result)