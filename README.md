# 🧾 Invoice Parser (OCR + Regex)

A lightweight invoice parsing system that extracts structured information from PDF invoices using **OCR (Tesseract)** and **rule-based parsing (Regex + Contextual Logic)**.

---

## 🚀 Features

- 📄 Upload invoice PDF
- 🔍 Extract key fields:
  - Invoice Number
  - Date
  - Total Amount
  - Email
  - Phone
  - Company Name
  - Names (if present)
  - Address(es)
- 📊 Confidence Score for extracted data
- 🌐 Interactive UI built with **Streamlit**

---

## 🧠 Approach

This project follows a **hybrid extraction strategy**:

### 1. OCR Layer (`ocr.py`)
- Converts PDF → Images using `pdf2image`
- Extracts raw text using `pytesseract`

---

### 2. Parsing Layer (`parser.py`)
- Cleans OCR text
- Splits into structured lines
- Uses:
  - Regex-based pattern matching (for email, phone, date)
  - Context-based extraction (for invoice, total, company, address)
  - Fallback strategies for robustness

---

### 3. Validation Layer (`validator.py`)
- Evaluates extracted data
- Assigns **confidence score**
- Ensures:
  - Correct format (email, date, phone)
  - Logical values (total range, invoice format)
  - Reduces false positives

---

### 4. UI Layer (`app.py`)
- Built using **Streamlit**
- Allows:
  - File upload
  - Display extracted fields
  - Show JSON output
  - Show confidence score

---

## 📁 Project Structure

```
invoice_parser/
│
├── app.py
├── ocr.py
├── parser.py
├── validator.py
├── sample_invoice.pdf
├── requirements.txt
├── packages.txt
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the repository

```
git clone https://github.com/julie-max/Invoice-parser.git
cd Invoice-parser
```

---

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Install system dependencies

- Install **Tesseract OCR**
- Install **Poppler**
- Add both to system PATH

---

## ▶️ Run Locally

```
streamlit run app.py
```

---

## 🌐 Deployment

Deployed using **Streamlit Cloud** : [link](https://invoice-parser-julie.streamlit.app/)

---

## 📊 Example Output

```json
{
  "invoice_number": "F1000876/23",
  "date": "14/08/2023",
  "total": "702.0",
  "email": "info@localstore.com",
  "phone": "000 255 6678",
  "company": "LOCAL STORE",
  "addresses": ["123 Main Street, NY 10001"]
}
```

---

## ⚠️ Limitations

- Rule-based system (not ML-based)
- May struggle with:
  - Highly unstructured invoices
  - Poor OCR quality
  - Missing keywords

---

## 🔮 Future Improvements

- Use ML/NLP models for semantic extraction
- Layout-aware parsing (LayoutLM / Donut)
- Better confidence scoring
- Multi-language support

---

## 👨‍💻 Author

**Briant Julian C**

---

## ⭐ Key Insight

This project balances recall (parser) and precision (validator) to achieve robust and explainable invoice extraction.
