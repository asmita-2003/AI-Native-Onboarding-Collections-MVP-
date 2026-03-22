def verify_transactions(data):
    txns = data.get("transactions", [])
    if not txns:
        return False, "No transactions found"

    balance = txns[0]["balance"]

    for i in range(1, len(txns)):
        t = txns[i]
        debit = t.get("debit") or 0
        credit = t.get("credit") or 0

        expected = balance - debit + credit
        actual = t["balance"]

        if abs(expected - actual) > 0.02:
            return False, f"Row {i} mismatch: expected {expected}, got {actual}"

        balance = actual

    return True, "Verified"
