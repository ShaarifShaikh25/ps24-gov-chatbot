import json
import requests

def load_schemes():
    with open("schemes.json", "r", encoding="utf-8") as f:
        return json.load(f)

def find_relevant_schemes(query, schemes):
    query = query.lower()
    matched = []

    for scheme in schemes:
        if scheme["name"].lower() in query:
            matched.append(scheme)
        else:
            for kw in scheme.get("keywords", []):
                if kw in query:
                    matched.append(scheme)
                    break
    return matched

# Internet fallback (official gov sites only)
def web_fallback_search(query):
    api_key = "YOUR_TAVILY_API_KEY"  # optional
    url = "https://api.tavily.com/search"
    payload = {
        "query": query + " site:gov.in OR site:nic.in",
        "max_results": 3
    }
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        res = requests.post(url, json=payload, headers=headers, timeout=10)
        return res.json()
    except:
        return None
