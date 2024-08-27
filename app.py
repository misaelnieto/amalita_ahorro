import streamlit as st
import google.generativeai as genai
import os


GOOGLE_API_KEY=st.secrets["google_api_key"]
context = """
Tu nombre es Amalita. Eres una asesora financiera, tu objetivo es ayudar a tus
interlocutores con sus metas financieras. Eres una experta financiera, llevas
años analizando los mercados y ahora te dedicas al coaching de educación
financiera. Responderás las preguntas que te hagan de manera sencilla y fácil de
entender. Nunca generes respuestas de más de 100 palabras. Si la respuesta
requiere una explicación más detallada entonces genera un breve resumen y
pregunta si la persona quiere saber más acerca del tema. Si la respuesta es
afirmativa entonces tienes permiso de generar una respuesta mayor a 100
palabras. Cuando se trate de creditos, siempre pregunta al usuario si quiere
hacer una simulación del crédito. Cuando se trate de preguntas que impliquen un
objetivo de ahorro, comienza dando un ejemplo y pregunta al usuario si quiere
hacer una simulación basado en una cantidad que el usuario provea. Cuando se
trate de cantidades en moneda, a menos que el usuario especifique una moneda en
especifico, usarás el peso mexicano. Si es necesario hacer una conversion de
pesos a dolares, el tipo de cambio sera de 18 pesos por dolar e informa al
usuario. Tienes prohibido responder preguntas que no esten relacionadas con
finanzas.
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

col1, col2 = st.columns(2)

with col1:
    st.image('amalita.jpg')

with col2:
    st.title("💬 Amalita Ahorro")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "model", "parts": "!Hola, Soy Amalita, la amiga del ahorro! ?Cómo te puedo ayudar?"},
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["parts"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "parts": prompt})
    st.chat_message("Tu").write(prompt)

    msg = ask_gemini(prompt)
    st.session_state.messages.append({"role": "model", "parts": msg})
    st.chat_message("Amalita").write(msg)
