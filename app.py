import streamlit as st
from pptx import Presentation
import requests
from io import BytesIO
import datetime

# Configuración inicial de la página
st.set_page_config(page_title="Informe Policial Automático", layout="centered")

st.title("🚔 Generador de Informe de Dispositivo Policial")

# ---- FORMULARIO DE CAPTURA ----
with st.form("formulario_informe"):
    st.subheader("🔹 Datos del Informe")
    nombre_dispositivo = st.text_input("Nombre del Dispositivo")
    direccion_regional = st.selectbox("Dirección Regional", [
        "Cartago", "San José", "Alajuela", "Heredia", "Guanacaste", "Puntarenas", "Limón"
    ])
    fecha_ejecucion = st.date_input("Fecha del Informe")
    responsable_dispositivo = st.text_input("Responsable del Informe")

    enviar = st.form_submit_button("📤 Generar Informe PPTX")

# ---- FUNCIÓN PARA CARGAR LA PLANTILLA ----
@st.cache_resource
def cargar_plantilla(url):
    respuesta = requests.get(url)
    return BytesIO(respuesta.content)

# ---- FUNCIÓN PARA GENERAR EL POWERPOINT ----
def generar_pptx(datos, plantilla_bytes):
    prs = Presentation(plantilla_bytes)

    # Portada personalizada (primera diapositiva)
    portada = prs.slides[0]
    for shape in portada.shapes:
        if shape.has_text_frame:
            texto = shape.text_frame.text
            texto = texto.replace("NOMBRE_DISPOSITIVO", datos['nombre_dispositivo'])
            texto = texto.replace("FECHA_EJECUCION", datos['fecha_ejecucion'])
            texto = texto.replace("RESPONSABLE", datos['responsable_dispositivo'])
            texto = texto.replace("DIRECCION_REGIONAL", datos['direccion_regional'])
            shape.text_frame.text = texto

    # Guardar la presentación en memoria
    ppt_buffer = BytesIO()
    prs.save(ppt_buffer)
    ppt_buffer.seek(0)
    return ppt_buffer

# ---- ACCIONES DESPUÉS DEL ENVÍO DEL FORMULARIO ----
if enviar:
    campos = [nombre_dispositivo, direccion_regional, fecha_ejecucion, responsable_dispositivo]
    if not all(campos):
        st.error("⚠️ Debes completar todos los campos para generar el informe.")
    else:
        st.success("✅ Informe generado, listo para descargar.")

        # URL CORRECTA de tu plantilla en GitHub
        plantilla_url = "https://github.com/CB230494/Formulario-a-Presentacion-Streamlit/raw/refs/heads/main/plantilla_personalizada.pptx"
        plantilla_bytes = cargar_plantilla(plantilla_url)

        datos = {
            'nombre_dispositivo': nombre_dispositivo,
            'fecha_ejecucion': fecha_ejecucion.strftime("%d/%m/%Y"),
            'direccion_regional': f"Dirección Regional {direccion_regional}",
            'responsable_dispositivo': responsable_dispositivo
        }

        ppt_buffer = generar_pptx(datos, plantilla_bytes)

        nombre_archivo = f"Informe_{nombre_dispositivo.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d')}.pptx"

        st.download_button(
            label="📥 Descargar Informe PPTX",
            data=ppt_buffer,
            file_name=nombre_archivo,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
