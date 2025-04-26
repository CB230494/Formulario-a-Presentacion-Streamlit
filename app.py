import streamlit as st
from pptx import Presentation
import requests
from io import BytesIO
import datetime

st.set_page_config(page_title="Informe del Dispositivo", layout="centered")

st.markdown("# 🚔 **Informe del Dispositivo Policial**")

with st.form("form_dispositivo"):
    st.subheader("🔹 Información General")
    nombre_dispositivo = st.text_input("Nombre del dispositivo")
    direccion_regional = st.selectbox("Dirección Regional", ["San José", "Alajuela", "Heredia", "Cartago", "Guanacaste", "Puntarenas", "Limón"])
    fecha_ejecucion = st.date_input("Fecha de Ejecución")
    responsable_dispositivo = st.text_input("Responsable del Dispositivo")

    st.subheader("🔹 Resultados Obtenidos")
    descripcion_resultados = st.text_area("Descripción de Resultados")

    st.subheader("🔹 Análisis o Balance Operativo")
    analisis_operativo = st.text_area("Análisis Operativo del Dispositivo")

    st.subheader("🔹 Recomendaciones o Sugerencias")
    recomendaciones = st.text_area("Recomendaciones para Mejorar")

    enviar = st.form_submit_button("📤 Generar Informe PPTX")

# --- Cargar plantilla personalizada desde GitHub ---
@st.cache_resource
def cargar_plantilla(url):
    resp = requests.get(url)
    return BytesIO(resp.content)

# --- Generar presentación personalizada usando plantilla ---
def generar_pptx(datos, plantilla_bytes):
    prs = Presentation(plantilla_bytes)

    # Portada personalizada (Slide 1)
    portada = prs.slides[0]
    for shape in portada.shapes:
        if shape.has_text_frame:
            texto = shape.text_frame.text
            texto = texto.replace("NOMBRE_DISPOSITIVO", datos['nombre_dispositivo'])
            texto = texto.replace("DIRECCION_REGIONAL", datos['direccion_regional'])
            texto = texto.replace("FECHA_EJECUCION", datos['fecha_ejecucion'])
            texto = texto.replace("RESPONSABLE", datos['responsable_dispositivo'])
            shape.text_frame.text = texto

    # Resultados obtenidos (Slide 2)
    resultados_slide = prs.slides[1]
    for shape in resultados_slide.shapes:
        if shape.has_text_frame:
            texto = shape.text_frame.text
            texto = texto.replace("DESCRIPCION_RESULTADOS", datos['descripcion_resultados'])
            shape.text_frame.text = texto

    # Análisis operativo (Slide 3)
    analisis_slide = prs.slides[2]
    for shape in analisis_slide.shapes:
        if shape.has_text_frame:
            texto = shape.text_frame.text
            texto = texto.replace("ANALISIS_OPERATIVO", datos['analisis_operativo'])
            shape.text_frame.text = texto

    # Recomendaciones (Slide 4)
    recomendaciones_slide = prs.slides[3]
    for shape in recomendaciones_slide.shapes:
        if shape.has_text_frame:
            texto = shape.text_frame.text
            texto = texto.replace("RECOMENDACIONES", datos['recomendaciones'])
            shape.text_frame.text = texto

    ppt_buffer = BytesIO()
    prs.save(ppt_buffer)
    ppt_buffer.seek(0)
    return ppt_buffer

# --- Acción después del envío del formulario ---
if enviar:
    campos_requeridos = [
        nombre_dispositivo, direccion_regional, fecha_ejecucion,
        responsable_dispositivo, descripcion_resultados, analisis_operativo, recomendaciones
    ]
    if not all(campos_requeridos):
        st.error("⚠️ Completa todos los campos antes de generar el informe.")
    else:
        st.success("✅ ¡Informe generado correctamente!")

        plantilla_url = "https://github.com/<TU_USUARIO>/<TU_REPO>/raw/main/plantilla_personalizada.pptx"
        plantilla_bytes = cargar_plantilla(plantilla_url)

        datos_formulario = {
            'nombre_dispositivo': nombre_dispositivo,
            'direccion_regional': direccion_regional,
            'fecha_ejecucion': fecha_ejecucion.strftime("%d/%m/%Y"),
            'responsable_dispositivo': responsable_dispositivo,
            'descripcion_resultados': descripcion_resultados,
            'analisis_operativo': analisis_operativo,
            'recomendaciones': recomendaciones
        }

        ppt_buffer = generar_pptx(datos_formulario, plantilla_bytes)

        nombre_archivo = f"Informe_{nombre_dispositivo.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d')}.pptx"
        
        st.download_button(
            label="📥 Descargar Informe PPTX",
            data=ppt_buffer,
            file_name=nombre_archivo,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
