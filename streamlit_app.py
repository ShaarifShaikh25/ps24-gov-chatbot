import streamlit as st
import openai
from prompt import SYSTEM_PROMPT
from utils import load_schemes, find_relevant_schemes

# Page config
st.set_page_config(page_title="PS-24 Government Assistant", layout="centered")
st.title("🇮🇳 Government Scheme Assistant (PS-24)")

# OpenAI Key
openai.api_key = "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"

# Load schemes
schemes = load_schemes()

# Language selector
language = st.selectbox(
    "Select Language / भाषा / भाषा निवडा",
    ["English", "Hindi", "Marathi"]
)

# User input
query = st.text_input("Ask about any government scheme:")

# Optional eligibility
st.subheader("Eligibility Details (Optional)")
age = st.number_input("Age", min_value=0, max_value=100, value=25)
income = st.number_input("Annual Income (₹)", min_value=0, value=300000)

if st.button("Get Information"):

    matched = find_relevant_schemes(query, schemes)

    if matched:
        context = ""
        for s in matched:
            context += f"""
Scheme Name: {s['name']}
Benefits: {s['benefits']}
Documents Required: {', '.join(s['documents'])}
How to Apply: {s['apply']}
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
Use only official Indian government portals to explain.
Clearly mention that information is sourced from government websites.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    st.success(response.choices[0].message.content)
