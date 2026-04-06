def calculate_confidence(data):
    score = 0
    total = 6

    # Invoice number
    if data.get("invoice_number"):
        score += 1

    # Date
    if data.get("date"):
        score += 1

    # Total
    if data.get("total"):
        score += 1

    # Email (valid format)
    if data.get("email") and "@" in data["email"]:
        score += 1

    # Phone (basic length check)
    if data.get("phone") and len(data["phone"]) >= 10:
        score += 1

    # Company
    if data.get("company"):
        score += 1

    confidence = (score / total) * 100
    return confidence