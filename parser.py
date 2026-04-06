import re

# --- KEYWORD GROUPS ---
TOTAL_KEYWORDS = [
    "total", "amount", "amount due", "grand total",
    "balance", "amount payable", "invoice total"
]

EMAIL_KEYWORDS = ["email", "e-mail", "email address"]

PHONE_KEYWORDS = ["phone", "mobile", "contact"]

COMPANY_KEYWORDS = ["company", "business", "seller"]

ADDRESS_KEYWORDS = ["address", "billing", "shipping"]


# --- CLEANING FUNCTION ---
def clean_text(text):
    text = text.replace("  ", " ")
    text = text.replace("\n\n", "\n")
    text = text.replace(" @ ", "@")
    return text


# --- MAIN PARSER ---
def extract_invoice_data(text):
    data = {}

    text = clean_text(text)
    lines = text.split("\n")

    # ---------------- INVOICE NUMBER ----------------
    invoice_candidates = []

    for i, line in enumerate(lines):
        if "invoice" in line.lower():

            # same line
            matches = re.findall(r'[A-Z0-9/-]+', line)
            invoice_candidates.extend(matches)

            # next line
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                matches = re.findall(r'[A-Z0-9/-]+', next_line)
                invoice_candidates.extend(matches)

    # filter valid candidates
    filtered = [
        c for c in invoice_candidates
        if any(char.isdigit() for char in c)
        and len(c) >= 5
    ]

    if filtered:
        data["invoice_number"] = max(filtered, key=len)

    # ---------------- DATE ----------------
    for line in lines:
        match = re.search(r'\d{2}/\d{2}/\d{4}', line)
        if match:
            data["date"] = match.group()
            break

    # ---------------- TOTAL ----------------
    for i, line in enumerate(lines):
        line_lower = line.lower()

        if any(k in line_lower for k in TOTAL_KEYWORDS):

            # extract numbers (handles 2280, 2,280, 1,200.50)
            numbers = re.findall(r'\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+', line)

            if numbers:
                values = [float(n.replace(",", "")) for n in numbers]
                data["total"] = str(max(values))

            # check next line
            elif i + 1 < len(lines):
                next_line = lines[i + 1]
                numbers = re.findall(r'\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+', next_line)

                if numbers:
                    values = [float(n.replace(",", "")) for n in numbers]
                    data["total"] = str(max(values))

            # OPTIONAL: check previous line (advanced)
            elif i - 1 >= 0:
                prev_line = lines[i - 1]
                numbers = re.findall(r'\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+', prev_line)

                if numbers:
                    values = [float(n.replace(",", "")) for n in numbers]
                    data["total"] = str(max(values))

    # ---------------- EMAIL ----------------
    for i, line in enumerate(lines):
        if any(k in line.lower() for k in EMAIL_KEYWORDS):

            match = re.search(r'\S+@\S+', line)
            if match:
                data["email"] = match.group()

            elif i + 1 < len(lines):
                data["email"] = lines[i + 1].strip().replace(" ", "")

    # ---------------- PHONE ----------------
    for i, line in enumerate(lines):
        if any(k in line.lower() for k in PHONE_KEYWORDS):

            match = re.search(r'\(?\d{3}\)?[-\s]\d{3}[-\s]\d{4}', line)
            if match:
                data["phone"] = match.group()

            elif i + 1 < len(lines):
                data["phone"] = lines[i + 1].strip()

    # ---------------- COMPANY ----------------
    for i, line in enumerate(lines):
        if any(k in line.lower() for k in COMPANY_KEYWORDS):

            if i + 1 < len(lines):
                candidate = lines[i + 1].strip()

                if (
                    not any(char.isdigit() for char in candidate)
                    and "@" not in candidate
                    and ".com" not in candidate
                    and len(candidate.split()) <= 6
                ):
                    data["company"] = candidate

    # ---------------- ADDRESS ----------------
    for i, line in enumerate(lines):
        if any(k in line.lower() for k in ADDRESS_KEYWORDS):

            if i + 1 < len(lines):
                addr = lines[i + 1].strip()

                if (
                    len(addr) > 10
                    and any(char.isdigit() for char in addr)
                ):
                    data.setdefault("addresses", []).append(addr)

    return data