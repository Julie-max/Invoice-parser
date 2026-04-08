import re

def calculate_confidence(data):
    score = 0
    total_fields = 8

    # ---------------- INVOICE NUMBER ----------------
    if data.get("invoice_number"):
        val = data["invoice_number"]

        if (
            5 <= len(val) <= 12
            and any(ch.isdigit() for ch in val)
            and not re.match(r'\d{2}[/-]\d{2}[/-]\d{4}', val)  # not date
        ):
            score += 1

    # ---------------- DATE ----------------
    if data.get("date"):
        if re.match(
            r'\d{2}[/-]\d{2}[/-]\d{4}|\d{4}[/-]\d{2}[/-]\d{2}',
            data["date"]
        ):
            score += 1

    # ---------------- TOTAL ----------------
    if data.get("total"):
        try:
            val = float(data["total"])
            if 0 < val < 1e7:
                score += 1
        except:
            pass

    # ---------------- EMAIL ----------------
    if data.get("email"):
        if re.match(
            r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
            data["email"]
        ):
            score += 1

    # ---------------- PHONE ----------------
    if data.get("phone"):
        digits = re.sub(r'\D', '', data["phone"])
        if len(digits) >= 10:
            score += 1

    # ---------------- COMPANY ----------------
    if data.get("company"):
        val = data["company"]

        if (
            val.lower() not in ["name", "company"]
            and not any(char.isdigit() for char in val)
            and "@" not in val
            and ".com" not in val
            and len(val.split()) <= 5
        ):
            score += 1

    # ---------------- NAMES ----------------
    if data.get("names"):
        valid_names = [
            n for n in data["names"]
            if len(n.split()) >= 2  # first + last name
        ]

        if valid_names:
            score += 1

    # ---------------- ADDRESSES ----------------
    if data.get("addresses"):
        valid_addresses = [
            addr for addr in data["addresses"]
            if (
                len(addr) > 10
                and any(ch.isdigit() for ch in addr)
            )
        ]

        if valid_addresses:
            score += 1

    confidence = (score / total_fields) * 100
    return confidence