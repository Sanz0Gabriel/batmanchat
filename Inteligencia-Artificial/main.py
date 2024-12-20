import streamlit as st
from groq import Groq

MODELOS = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]

def crear_usuario_groq():
    clave_usuario = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_usuario)

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def filtrar_historial(historial):
    seen = set()
    historial_filtrado = []
    for msg in historial:
        if msg["content"] not in seen:
            historial_filtrado.append(msg)
            seen.add(msg["content"])
    return historial_filtrado

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def configurar_pagina():
    st.set_page_config("Bati-Chat")
    st.title("BATICOMPUTADOR")
    st.sidebar.title("Sidebar de modelos")
    modelo_seleccionado = st.sidebar.selectbox("Modelos", MODELOS, index=0)
    
    if st.sidebar.button("Recargar conversación"):
        st.session_state.mensajes = []  
    
    return modelo_seleccionado

def main():
    inicializar_estado()
    usuario = crear_usuario_groq()
    modelo_actual = configurar_pagina()
    
    mensaje = st.chat_input("Escribe algo...:")

    if mensaje:
        actualizar_historial("user", mensaje, "🦇")
        
        historial = filtrar_historial([{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.mensajes])
        
        respuesta_chat_bot = usuario.chat.completions.create(
            model=modelo_actual,
            messages=historial + [{"role": "user", "content": mensaje}],
            stream=True
        )
        
        respuesta_completa = "".join([r.choices[0].delta.content for r in respuesta_chat_bot if r.choices[0].delta.content is not None])
        actualizar_historial("assistant", respuesta_completa, "📺")
        
    mostrar_historial()

if __name__ == "__main__":
    main()
