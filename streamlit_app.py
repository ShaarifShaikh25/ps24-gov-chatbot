import streamlit as st
from openai import OpenAI
from prompt import SYSTEM_PROMPT
from utils import load_schemes, find_relevant_schemes

st.set_page_config(page_title="IN Government Scheme Assistant (PS-24)")
st.title("🇮🇳 Government Scheme Assistant (PS-24)")

# Initialize OpenAI client (NO openai.api_key anywhere)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Load dataset
schemes = load_schemes()

query = st.text_input("Ask about any government scheme:")

if st.button("Get Information"):
    matched = find_relevant_schemes(query, schemes)

    if matched:
        context = ""
        for s in matched:
            context += f"""
Scheme Name: {s['name']}
Benefits: {s['benefits']}
Documents: {', '.join(s['documents'])}
Apply: {s['apply']}
"""

        prompt = f"""
User Question: {query}

Dataset Information:
{context}

Explain clearly.
"""
    else:
        prompt = f"""
User Question: {query}

The scheme is not present in the dataset.
Use only official Indian government portals.
Mention source clearly.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    st.success(response.choices[0].message.content)
