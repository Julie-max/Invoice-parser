import re

# --- KEYWORDS ---
TOTAL_KEYWORDS = [
    "total", "amount", "amount due", "grand total",
    "balance", "amount payable", "invoice total"
]

DATE_PATTERNS = [
    r'\d{2}/\d{2}/\d{4}',
    r'\d{2}-\d{2}-\d{4}',
    r'\d{4}-\d{2}-\d{2}'
]


# --- CLEAN TEXT ---
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s*@\s*', '@', text)

    # add structure hints
    keywords = [
        "Invoice", "Total", "Phone", "Email",
        "Address", "Billing", "Shipping",
        "Company", "Description", "Name"
    ]

    for kw in keywords:
        text = re.sub(rf'(?i)\s({kw})', r'\n\1', text)

    return text.strip()


# --- MAIN PARSER ---
def extract_invoice_data(text):

    data = {
        "invoice_number": None,
        "date": None,
        "total": None,
        "email": None,
        "phone": None,
        "company": None,
        "names": [],
        "addresses": []
    }

    text = clean_text(text)
    lines = text.split("\n")

    # ---------------- INVOICE NUMBER ----------------
    invoice_candidates = []

        # PRIMARY: context-based
    for i, line in enumerate(lines):
        if "invoice" in line.lower():

            matches = re.findall(r'[A-Z0-9/-]{5,}', line)
            invoice_candidates.extend(matches)

            if i + 1 < len(lines):
                matches = re.findall(r'[A-Z0-9/-]{5,}', lines[i + 1])
                invoice_candidates.extend(matches)

    # FALLBACK: global search
    if not invoice_candidates:
        candidates = re.findall(r'\b[A-Z0-9/-]{5,}\b', text)
        invoice_candidates = [
            c for c in candidates if any(ch.isdigit() for ch in c)
        ]

    # FILTER
    invoice_candidates = [
        c for c in invoice_candidates
        if any(ch.isdigit() for ch in c)
        and not re.match(r'\d{2}[/-]\d{2}[/-]\d{4}', c)
        and len(c) <= 12
    ]

    if invoice_candidates:
        data["invoice_number"] = invoice_candidates[0]

    # ---------------- DATE ----------------
    for pattern in DATE_PATTERNS:
        match = re.search(pattern, text)
        if match:
            data["date"] = match.group()
            break

    # ---------------- TOTAL ----------------
    totals = []

    for line in lines:
        if any(k in line.lower() for k in TOTAL_KEYWORDS):
            nums = re.findall(r'\d+(?:,\d{3})*(?:\.\d+)?', line)

            for n in nums:
                val = float(n.replace(",", ""))
                if val > 500:  # ignore unit prices
                    totals.append(val)

    if not totals:
        all_nums = re.findall(r'\d+(?:,\d{3})*(?:\.\d+)?', text)
        vals = [float(n.replace(",", "")) for n in all_nums]
        if vals:
            totals.append(max(vals))

    if totals:
        data["total"] = str(max(totals))

    # ---------------- EMAIL ----------------
    email_match = re.search(
        r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', text)
    if email_match:
        data["email"] = email_match.group()

    # ---------------- PHONE ----------------
    phone_match = re.search(
        r'\(?\d{3}\)?[\s\-]\d{3}[\s\-]\d{4}', text)
    if phone_match:
        data["phone"] = phone_match.group()

    # ---------------- COMPANY + NAMES ----------------
    # Extract chunk between Company Name Name and Address
    pattern = r'Company\s+Name\s+Name\s+(.*?)\s+Address'
    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        chunk = match.group(1).strip()

        # Remove noise words
        noise_words = {"lane", "road", "street"}
        words = [w for w in chunk.split() if w.lower() not in noise_words]

        # -------- COMPANY --------
        if len(words) >= 2:
            data["company"] = " ".join(words[:2])

        # -------- NAMES --------
        name_pattern = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b'
        names = re.findall(name_pattern, chunk)

        # remove company from names
        names = [n for n in names if data["company"] not in n]

        if names:
            data["names"] = list(set(names))

    # fallback (if above fails)
    if not data["company"]:
        for line in lines:
            if "company" in line.lower():
                parts = line.split()
                if len(parts) > 1:
                    data["company"] = " ".join(parts[1:])
                    break

    # ---------------- ADDRESSES ----------------
    address_pattern = r'\d{3,}[^A-Z]+?(?:\d{5,6})'
    matches = re.findall(address_pattern, text)

    addresses = []
    for addr in matches:
        addr = addr.strip()
        if len(addr) > 15:
            addresses.append(addr)

    if not addresses:
        for line in lines:
            if "address" in line.lower() and any(c.isdigit() for c in line):
                addresses.append(line.strip())

    if addresses:
        data["addresses"] = list(set(addresses))

    return data