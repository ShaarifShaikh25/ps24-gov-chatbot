import streamlit as st
import openai
from prompt import SYSTEM_PROMPT
from utils import load_schemes, find_relevant_scheme, check_eligibility

# Page setup
st.set_page_config(page_title="PS-24 Gov Assistant", layout="centered")
st.title("🇮🇳 Government Scheme Assistant (PS-24)")

# API key from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Load dataset
schemes = load_schemes()

# Language selection
language = st.selectbox(
    "Select Language / भाषा / भाषा निवडा",
    ["English", "Hindi", "Marathi"]
)

# User inputs
user_query = st.text_input("Ask about a government scheme:")

st.subheader("Eligibility Details (Optional)")
age = st.number_input("Age", min_value=0, max_value=100, value=25)
income = st.number_input("Annual Income (₹)", min_value=0, value=300000)

if st.button("Get Answer"):
    scheme = find_relevant_scheme(user_query, schemes)

    if not scheme:
        st.warning("Scheme not found in government records.")
    else:
        eligible, reasons = check_eligibility(
            {"age": age, "income": income},
            scheme
        )

        context = f"""
Scheme Name: {scheme['name']}
Benefits: {scheme['benefits']}
Documents: {', '.join(scheme['documents'])}
Application Process: {scheme['apply']}
Eligibility Result: {"Eligible" if eligible else "Not Eligible"}
Reason: {', '.join(reasons)}
"""

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": context}
            ]
        )

        st.success(response.choices[0].message.content)
