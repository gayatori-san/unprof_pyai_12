import argparse
import json
import re
import sys
from pathlib import Path

import pdfplumber  # type: ignore
from pypdf import PdfReader  # type: ignore


def clean_text(raw_text: str) -> str:
    """Normalize whitespace: collapse spaces/tabs, trim lines, max 1 blank line."""
    if not raw_text:
        return ""

    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = "\n".join(line.strip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_metadata(pdf_path: Path) -> dict:
    """Extract page count and metadata using pypdf."""
    try:
        reader = PdfReader(str(pdf_path))
        meta = reader.metadata or {}
        return {
            "num_pages": len(reader.pages),
            "title": meta.title if meta.title else None,
            "author": meta.author if meta.author else None,
        }
    except Exception as e:
        return {"num_pages": None, "title": None, "author": None, "metadata_error": str(e)}


def extract_pdf_data(pdf_path: Path) -> dict:
    """Extract text and tables from each page using pdfplumber, with pypdf fallback."""
    result = {
        "source_file": pdf_path.name,
        "metadata": extract_metadata(pdf_path),
        "pages": [],
    }

    fallback_reader = None
    try:
        fallback_reader = PdfReader(str(pdf_path))
    except Exception:
        pass

    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            raw_text = page.extract_text() or ""

            if not raw_text.strip() and fallback_reader:
                try:
                    # pypdf pages are 0-indexed; our loop is 1-indexed
                    raw_text = fallback_reader.pages[i - 1].extract_text() or ""
                except Exception:
                    pass

            tables = page.extract_tables() or []
            cleaned = clean_text(raw_text)

            result["pages"].append({
                "page_number": i,
                "raw_text": raw_text,
                "cleaned_text": cleaned,
                "word_count": len(cleaned.split()) if cleaned else 0,
                "tables": tables,
                "table_count": len(tables),
            })

    result["total_pages_processed"] = len(result["pages"])
    result["total_tables_found"] = sum(p["table_count"] for p in result["pages"])

    return result


def save_json(data: dict, output_path: Path) -> None:
    """Write data to JSON, creating parent directories if needed."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text and tables from a PDF into JSON.")
    parser.add_argument("pdf_path", help="Path to the input PDF file")
    parser.add_argument("-o", "--output", default=None, help="Output JSON file path (default: output/<filename>.json)")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"❌ File not found: {pdf_path}")
        sys.exit(1)

    output_path = Path(args.output) if args.output else Path(f"output/{pdf_path.stem}.json")

    print(f"📄 Reading PDF: {pdf_path}")
    data = extract_pdf_data(pdf_path)

    print(f"📝 Extracted text from {data['total_pages_processed']} page(s)")
    print(f"📊 Found {data['total_tables_found']} table(s)")

    save_json(data, output_path)
    print(f"💾 Saved processed data to: {output_path}")


if __name__ == "__main__":
    main()