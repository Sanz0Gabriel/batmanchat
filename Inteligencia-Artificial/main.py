import streamlit as st
from groq import Groq 

clave_usuario = ""
usuario = ""
modelo_actual = ""
mensaje = ""
MODELOS = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]


def crear_usuario_groq():
    clave_usuario = st.secrets["CLAVE_API"]
    return Groq(api_key = clave_usuario)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream=True
)

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar":avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_de_chat():
    contenedor_del_chat = st.container(height=700, border=True)
    with contenedor_del_chat:
        mostrar_historial()

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def configurar_pagina():
    st.set_page_config("Bati-Chat")
    st.title("BATICOMPUTADOR")
    st.sidebar.title("Sidebar de modelos")
    m = st.sidebar.selectbox("Modelos", MODELOS, index = 0)
    return m

def main():
    inicializar_estado()
    usuario = crear_usuario_groq()
    modelo_actual = configurar_pagina()
    area_de_chat()
    mensaje = st.chat_input("Escribe algo...:")
    respuesta_chat_bot = ""
    
    if mensaje:
        actualizar_historial("user", mensaje, "🦇")
        respuesta_chat_bot = configurar_modelo(usuario, modelo_actual, mensaje)
    
    if respuesta_chat_bot:
        with st.chat_message("assistant"):
            respuesta_completa = st.write_stream(generar_respuesta(respuesta_chat_bot))
            actualizar_historial("assistant", respuesta_completa,"📺")
        
            st.rerun()

if __name__ == "__main__":
    main()