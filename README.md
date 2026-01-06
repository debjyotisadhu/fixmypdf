# 📄 Fix My PDF

**Fix My PDF** is a lightweight, browser-based PDF utility built using **Streamlit**.  
It allows users to perform common PDF operations securely and locally without uploading files to third-party servers.

> Merge • Split • Unlock • Rotate • Extract • Watermark • Compress PDFs — all in one place.

---

## 🚀 Features

- ✅ Merge multiple PDFs into one
- ✂️ Split a PDF into two parts
- 🔓 Unlock password-protected PDFs
- 🔄 Rotate pages (90°, 180°, 270°)
- 📄 Extract selected pages (e.g. `1,3,5-7`)
- 💧 Add text watermark to all pages
- 🗜️ Compress PDFs (lossless)
- 🔐 Optional password handling for encrypted PDFs

---

## 🛠️ Tech Stack

- **Frontend / UI**: Streamlit  
- **PDF Processing**: `pypdf`  
- **Watermark Generation**: `reportlab`  
- **Language**: Python 3.0+

---

## 📦 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/fix-my-pdf.git
cd fix-my-pdf
```

### 2️⃣ Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```
### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt

