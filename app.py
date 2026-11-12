import streamlit as st  
from groq import Groq

st.set_page_config(page_title="Mi Chat de IA", page_icon="🙂")
st.title("Mi primera aplicación con Streamlit")
nombre = st.text_input("¿Cuál es tu nombre?")
if st.button("Saludar"):
    st.write(f"¡Hola, {nombre}! ¡Bienvenido! ")

MODELOS = ['llama-3.3-70b-versatile', 'openai/gpt-oss-20b', 'openai/gpt-oss-120b']


def crear_usuario_groq():
    # Obtenemos la clave API de la carpeta 'streamlit'
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)  # Conectamos a la API


def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model=modelo,  # Selecciona el modelo de la IA
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream=True  # Funcionalidad para que la IA responda a tiempo real
    )


def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []  # Historial de mensajes


def confiigurar_pagina():
    st.title("Mi chat de IA")
    st.sidebar.title("Configuración")
    opcion = st.sidebar.selectbox("Elegí un modelo", options=MODELOS, index=0)
    return opcion

# .append() agrega datos a la lista


def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar": avatar})


def mostrar_historial():  # Estrucutra visual del mensaje
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])


def area_chat():
    contenedorDeChat = st.container(height=400, border=True)
    with contenedorDeChat:
        mostrar_historial()


def generar_respuesta(chat_completo):
    respuesta_completa = ""  # Variable vacía
    for frase in chat_completo:
        if frase.choices[0].delta.content:  # Evita el dato None
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content

    return respuesta_completa


def main():

    # INVOCACION DE FUNCIONES
    modelo = confiigurar_pagina()  # Modelo seleccionado
    clienteUsuario = crear_usuario_groq()  # Conecta con la API GROQ
    inicializar_estado()  # Crea en memoria historial vacío
    area_chat()  # Crea el contenedor de mensaje
    mensaje = st.chat_input("Escribí un mensaje...")

    if mensaje:
        actualizar_historial("user", mensaje, "🙋‍♂️")
        # Obtiene la respuesta de la IA
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(
                    generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "😆")
                st.rerun()  # Actualizar


if __name__ == "__main__":
    main()
    # Para ejecutar: python -m streamlit run app.py
