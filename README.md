# 📄 PDF Text & Table Extractor

A Python command-line tool that extracts **text**, **tables**, and **metadata** from PDF files and stores the processed information in a structured JSON format.

---

# ✨ Features

* 📖 Extracts text from every page of a PDF
* 🧹 Cleans and normalizes extracted text
* 📊 Extracts tables using **pdfplumber**
* 🔄 Falls back to **pypdf** when text extraction fails
* 📑 Retrieves PDF metadata:

  * 📄 Title
  * ✍️ Author
  * 📚 Number of pages
* 🔢 Calculates word count for each page
* 💾 Saves all extracted information as a formatted JSON file
* 📁 Automatically creates the output directory if it doesn't exist

---

# 📂 Project Structure

```text
project/
│
├── task 12.py
├── output/
└── README.md
```

---

# ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/gayatori-san/unprof_pyai_12
```

### 2️⃣ Navigate to the project directory

```bash
cd pdf reader
```

### 3️⃣ (Optional) Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4️⃣ Install the required dependencies

```bash
pip install pdfplumber pypdf
```

---

# 🚀 Usage

### Basic Usage

```bash
python pdf_extractor.py input.pdf
```

### Specify a Custom Output File

```bash
python pdf_extractor.py input.pdf -o extracted_data.json
```

---

# 📦 Output

If no output path is specified, the JSON file is saved as:

```text
output/<pdf_filename>.json
```

Example:

```text
output/sample.json
```

---

# 🗂️ JSON Structure

```json
{
  "source_file": "sample.pdf",
  "metadata": {
    "num_pages": 5,
    "title": "Example",
    "author": "John Doe"
  },
  "pages": [
    {
      "page_number": 1,
      "raw_text": "...",
      "cleaned_text": "...",
      "word_count": 245,
      "tables": [],
      "table_count": 0
    }
  ],
  "total_pages_processed": 5,
  "total_tables_found": 2
}
```

---

# 🔄 Workflow

1. 📄 Read the input PDF.
2. 📑 Extract document metadata.
3. 📖 Process each page individually.
4. 🔍 Extract text using **pdfplumber**.
5. 🔄 Use **pypdf** as a fallback if necessary.
6. 🧹 Clean and normalize extracted text.
7. 📊 Extract tables from each page.
8. 🔢 Calculate page-wise word counts.
9. 💾 Save the processed data as a JSON file.

---

# 🛠️ Dependencies

* 📦 pdfplumber
* 📦 pypdf
* 📦 argparse
* 📦 json
* 📦 pathlib
* 📦 re
* 📦 sys
