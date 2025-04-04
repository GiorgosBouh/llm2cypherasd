import streamlit as st
import openai
import requests

# === Streamlit UI ===
st.set_page_config(page_title="ASD KG Chat", layout="centered")
st.title("🧠 Ερωτήσεις πάνω στο Knowledge Graph για Αυτισμό")

# Ask for OpenAI key securely (not exposed in logs)
api_key = st.text_input("🔑 Εισήγαγε το OpenAI API Key σου", type="password")

if not api_key:
    st.warning("Παρακαλώ εισήγαγε το OpenAI API Key σου για να συνεχίσεις.")
    st.stop()

openai.api_key = api_key
API_URL = "http://127.0.0.1:8080"  # FastAPI backend (πρέπει να τρέχει τοπικά)

user_input = st.text_input("📝 Κάνε μια ερώτηση σε φυσική γλώσσα", placeholder="Π.χ. Πόσα νήπια έχουν χαρακτηριστικά αυτισμού;")

if st.button("Ρώτησε") and user_input.strip():
    with st.spinner("🔍 Αναλύω την ερώτηση και ανακτώ δεδομένα..."):

        try:
            # 1. Φτιάξε το prompt
            prompt = f"""
You are a Cypher expert. Translate the question into Cypher only.

Question: "{user_input}"
"""

            # 2. Στείλε στο OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )

            raw_cypher = response["choices"][0]["message"]["content"].strip()

            # 3. Στείλε στο FastAPI backend
            api_response = requests.post(f"{API_URL}/query", json={
                "query": raw_cypher,
                "parameters": {}
            })

            if api_response.status_code != 200:
                st.error(f"Σφάλμα από Neo4j API: {api_response.status_code}")
                st.json(api_response.json())
            else:
                result = api_response.json()
                st.success("✅ Απάντηση βρέθηκε!")

                st.markdown("### 🧠 Cypher Εντολή")
                st.code(raw_cypher, language="cypher")

                st.markdown("### 📦 Αποτελέσματα από Neo4j")
                st.json(result["results"])

        except Exception as e:
            st.error(f"❌ Σφάλμα: {str(e)}")