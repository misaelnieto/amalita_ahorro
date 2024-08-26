import streamlit as st
import google.generativeai as genai
import os


GOOGLE_API_KEY=st.secrets["google_api_key"]
context = """
Tu nombre es Amalita. Eres una asesora financiera,
tu objetivo es ayudar a las personas con sus metas financieras.
Tienes prohibido responder preguntas que no esten relacionadas con finanzas.
"""

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=context
)

def ask_gemini(message):
    chat_session = model.start_chat(
        history=st.session_state.messages
    )

    response = chat_session.send_message(message)
    return response.text


st.title("💬 Amalita Ahorro")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "model", "parts": "Hola, Soy Amalita, la amiga del ahorro. Como te puedo ayudar?"},
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["parts"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "parts": prompt})
    st.chat_message("Tu").write(prompt)

    msg = ask_gemini(prompt)
    st.session_state.messages.append({"role": "model", "parts": msg})
    st.chat_message("Amalita").write(msg)
