import fitz  # PyMuPDF

# 📄 List of PDFs to extract
pdf_files = [
    ("data/rent_act.pdf", "data/rent_act_clean.txt"),
    ("data/contract_act.pdf", "data/contract_act_clean.txt"),
]

for pdf_path, txt_path in pdf_files:
    doc = fitz.open(pdf_path)
    with open(txt_path, "w", encoding="utf-8") as f:
        for page in doc:
            text = page.get_text()
            f.write(text)
            f.write("\n--- PAGE BREAK ---\n")
    print(f"✅ Extraction done! {txt_path} is ready.")


