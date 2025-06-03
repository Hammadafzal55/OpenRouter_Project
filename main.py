import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

st.markdown("""
    <style>
    .stSelectbox > div > div {
        cursor: pointer !important;
    }
    </style>
""", unsafe_allow_html=True)

#Api key load krne k liye
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

#Models ki list
Models = {
    "Gemini 2.5 (Google)": "google/gemini-2.5-flash-preview-05-20",
    "Deepseek R1 (DeepSeek)": "deepseek/deepseek-r1-0528-qwen3-8b",
    "Phi 4 Reasoning Plus (Microsoft)": "microsoft/phi-4-reasoning-plus",
    "Devstral Small (Mistral)": "mistralai/devstral-small",
    "Llama 3.3 (Nividia)": "nvidia/llama-3.3-nemotron-super-49b-v1",
    "Gemma 3n 4B (Google)": "google/gemma-3n-e4b-it",
    "Sarvam-M (Sarvam AI)": "sarvamai/sarvam-m",
    "Llama 3.3 8B Instruct (Meta)": "meta-llama/llama-3.3-8b-instruct",
    "DeepHermes 3 (Nous)": "nousresearch/deephermes-3-mistral-24b-preview",
    "Qwen3 30B A3B (Qwen)": "qwen/qwen3-30b-a3b"
}

#Api Call krne k liye function
def get_response(model_id, prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": model_id,
        "messages": [{ "role": "user","content": prompt }],
        "max_tokens": max_tokens,
    }

    res = requests.post(url, headers=headers, data=json.dumps(body))
    data = res.json()

    if 'choices' in data:
        return data["choices"][0]["message"]["content"]
    else:
        return f"❌ Error: {data.get('error', {}).get('message', 'Unknown error')}"
    
#Stremlit ka User Interface
st.title("🧠 Ai Model Comparision tool using Openrouter and Streamlit")
st.write("Apne prompt ka mukhtalif AI models se jawab dekhein.")

#prompt dene k liye text input
prompt = st.text_area("Apna prompt likhein:", height=100)

#Model select karne k liye dropdown
model_options = list(Models.keys())
selected_model = st.selectbox(
    "🧠 Kaunsa model istemal karna chahte hain?",
    options=model_options
)

#Submit Button
if st.button("🚀 Submit"):
    if not prompt.strip():
        st.warning("⛔ Pehle prompt likhen.")
    elif not selected_model:
        st.warning("⛔ Kam az kam aik model select karein.")
    else:
        model_id = Models[selected_model]
        st.markdown(f"### 📌 Model: {selected_model}")
        with st.spinner("Thinking..."):
            result = get_response(model_id, prompt)
        st.markdown(result)
