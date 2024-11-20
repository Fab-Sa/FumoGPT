import streamlit as st
from groq import Groq

# Modelos y configuraciones iniciales
modelos = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]
fumos = ["Cirno", "Yuyuko", "Reimu"]
modelo_en_uso = ""
cliente_usuario = ""
clave_secreta = ""
mensaje = ""

def crear_usuario():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def configurar_modelo(cliente, modelo, mensaje_de_entrada):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensaje_de_entrada}],
        stream=True
    )

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def configurar_pagina():
    icon = "images/FumoPAGINA.png"
    st.set_page_config(page_title="FumoGPT", page_icon=icon, layout="wide")
    
    # SIDEBAR CON OPCIONES
    st.sidebar.title("⚙️ CONFIGURACIÓN")
    m = st.sidebar.selectbox("Modelo", modelos, 0)
    st.sidebar.selectbox("Fumos", fumos, 0)

    # BOTÓN PARA REINICIAR LA PÁGINA
    if st.sidebar.button("Borrar Chat"):
        st.session_state.mensajes = []
        st.rerun()
    # EL PELUCHE
    fumo_icon = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/174d49c1-37d9-4645-812b-fbe3e77d8955/dg8h9n2-2872dedb-68a3-4409-97b4-3f5ed7c86d4d.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzE3NGQ0OWMxLTM3ZDktNDY0NS04MTJiLWZiZTNlNzdkODk1NVwvZGc4aDluMi0yODcyZGVkYi02OGEzLTQ0MDktOTdiNC0zZjVlZDdjODZkNGQucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.KRJdK4iX5I7qbTh2MDtCyBAIB00PLFeMZBZLmyfPbRM"
    
    # EL ICONO JUNTO AL TEXTO "GPT"
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 0px;">
            <img src="{fumo_icon}" alt="Fotito del fumo" style="width: 75px; height: 100px;">
            <h1 style="margin: 0; color: #85D3F7;">GPT</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    return m

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container()
    with contenedorDelChat:
        mostrar_historial()

def main():
    # Inicialización
    modelo_en_uso = configurar_pagina()
    cliente_usuario = crear_usuario()
    inicializar_estado()
    area_chat()
    
    # Entrada de chat
    mensaje = st.chat_input(placeholder="Escribe aquí tu mensaje")
    chat_completo = None

    if mensaje:
        avatar_usuario = "images/User.png"
        avatar_ia = "https://media.tenor.com/iPKa5SFvaKAAAAAj/touhou-cirno.gif"
        
        actualizar_historial("user", mensaje, avatar_usuario)
        chat_completo = configurar_modelo(cliente_usuario, modelo_en_uso, mensaje)

    if chat_completo:
        with st.chat_message("assistant"):
            respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
        actualizar_historial("assistant", respuesta_completa, avatar_ia)
        st.rerun()

if __name__ == "__main__":
    main()
