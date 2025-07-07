# agents/parse_agent.py

import re

def extract_clauses_from_text(text):
    """
    Takes full legal text and returns a list of clauses based on patterns like 'شق 1:', 'شق 2:' etc.
    """
    # Urdu pattern for شق
    pattern = r"(شق[\s\d:]+)"

    # Split using regex
    parts = re.split(pattern, text)

    # Rebuild clean clause blocks
    clauses = []
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        body = parts[i + 1].strip() if (i + 1) < len(parts) else ""
        full_clause = f"{heading} {body}".strip()
        if len(full_clause) > 20:
            clauses.append(full_clause)

    return clauses


# Test this code separately
if _name_ == "_main_":
    sample_text = """
    شق 1: کرایہ دار کو ہر ماہ کی 5 تاریخ تک کرایہ ادا کرنا ہوگا۔
    شق 2: مکان خالی کرنے کے لیے 30 دن کا نوٹس دینا لازمی ہے۔
    شق 3: مالک مکان بغیر اطلاع کے کرایہ نہیں بڑھا سکتا۔
    """
    extracted = extract_clauses_from_text(sample_text)
    for c in extracted:
        print("➡", c)