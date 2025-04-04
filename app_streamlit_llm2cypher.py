import streamlit as st
import openai
import requests

# === OpenAI Setup ===
client = openai.OpenAI(
    api_key="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"
)
MODEL = "gpt-4o-2024-08-06"
API_URL = "http://127.0.0.1:8080"  # FastAPI backend (app_kg_api.py)

# === Streamlit UI ===
st.set_page_config(page_title="ASD KG Chat", layout="centered")
st.title("🧠 Ερωτήσεις πάνω στο Knowledge Graph για Αυτισμό")

user_input = st.text_input("Κάνε μια ερώτηση σε φυσική γλώσσα", placeholder="Π.χ. Πόσα νήπια έχουν χαρακτηριστικά αυτισμού;")

if st.button("Ρώτησε") and user_input.strip():
    with st.spinner("Αναλύω την ερώτηση και ανακτώ δεδομένα..."):

        # 1. Στέλνει στο backend `/ask`
        try:
            response = requests.post(f"{API_URL}/ask", json={"question": user_input})
            if response.status_code != 200:
                st.error(f"Σφάλμα από το API: {response.status_code}")
            else:
                result = response.json()
                st.success("✅ Απάντηση βρέθηκε!")

                st.markdown(f"### ✨ Απάντηση\n{result['answer']}")
                with st.expander("🧠 Cypher Εντολή"):
                    st.code(result["cypher"], language="cypher")

                with st.expander("📦 Ακατέργαστα αποτελέσματα"):
                    st.json(result["results"])

        except Exception as e:
            st.error(f"❌ Σφάλμα: {str(e)}")
