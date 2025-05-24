import streamlit as st
from chatbot.chat_engine import LGPDChatBot

# Configuração da página
st.set_page_config(page_title="Chatbot LGPD", layout="centered", page_icon=":robot:")


# Título e descrição
st.title("🤖 Chatbot LGPD")
st.markdown("Converse com um assistente especializado na **Lei Geral de Proteção de Dados (LGPD)**.")

# Inicializa o chatbot
if "chatbot" not in st.session_state:
    st.session_state.chatbot = LGPDChatBot()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de mensagens
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada do usuário
prompt = st.chat_input("Digite a sua dúvida sobre LGPD...")

# Processamento da entrada
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        resposta = st.session_state.chatbot.ask(prompt)
    except Exception as e:
        resposta = f"❌ Erro ao conectar com o chatbot: {e}"

    st.session_state.messages.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        st.markdown(resposta)
