# agents/user_profile.py

import os
import json
from datetime import datetime

def save_user_query(user_id, clause, explanation, risk=None, notice=None):
    """
    Save user's interaction to a JSON file.
    Each query stores clause + its explanation (+ optional risk, notice)
    """
    profile_dir = "user_profiles"
    os.makedirs(profile_dir, exist_ok=True)

    profile_path = os.path.join(profile_dir, f"{user_id}_profile.json")

    entry = {
        "timestamp": datetime.now().isoformat(),
        "clause": clause,
        "explanation": explanation,
        "risk": risk,
        "notice": notice
    }

    # Load old profile or create new
    profile = []
    if os.path.exists(profile_path):
        with open(profile_path, "r", encoding="utf-8") as f:
            try:
                profile = json.load(f)
            except json.JSONDecodeError:
                profile = []

    # Add new entry
    profile.append(entry)

    # Save updated
    with open(profile_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

    return True


# Sample test
if __name__ == "__main__":
    save_user_query(
        user_id="user123",
        clause="شق 2: مالک مکان کرایہ دار کو 30 دن کا نوٹس دے گا۔",
        explanation="مالک کو 30 دن پہلے نوٹس دینا ہوگا۔",
        risk="تحریری نوٹس کا طریقہ واضح نہیں",
        notice="محترم کرایہ دار، براہ کرم 30 دن میں مکان خالی کریں۔"
    )
    print("✅ Saved to user123_profile.json")
