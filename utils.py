import json

def load_schemes():
    with open("schemes.json", "r", encoding="utf-8") as f:
        return json.load(f)

def find_relevant_scheme(user_query, schemes):
    for scheme in schemes:
        if scheme["name"].lower() in user_query.lower():
            return scheme
    return None

def check_eligibility(user_data, scheme):
    eligibility = scheme.get("eligibility", {})
    reasons = []

    if "income" in eligibility:
        limit = int(eligibility["income"].replace("<", "").strip())
        if user_data["income"] >= limit:
            reasons.append("Income exceeds eligibility limit")

    if "age" in eligibility:
        if user_data["age"] < 18:
            reasons.append("Age below minimum requirement")

    if reasons:
        return False, reasons

    return True, ["Eligible based on provided details"]
