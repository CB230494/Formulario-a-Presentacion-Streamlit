import streamlit as st
from pptx import Presentation
import requests
from io import BytesIO
import datetime

st.set_page_config(page_title="Informe Policial Automático", layout="centered")

st.title("🚔 Generador de Informe de Dispositivo Policial")

# ---- FORMULARIO ----
with st.form("formulario_informe"):
    st.subheader("🔹 Datos del Informe")
    nombre_dispositivo = st.text_input("Nombre del Dispositivo")
    nombre_responsable = st.text_input("Nombre del Responsable")
    cargo_responsable = st.text_input("Cargo del Responsable")
    direccion_regional = st.selectbox("Dirección Regional", [
        "Cartago", "San José", "Alajuela", "Heredia", "Guanacaste", "Puntarenas", "Limón"
    ])
    delegacion_policial = st.text_input("Delegación Policial")
    fecha_ejecucion = st.date_input("Fecha de ejecución")
    
    st.subheader("🔹 Contenido del Informe")
    descripcion_resultados = st.text_area("Breve descripción de resultados obtenidos")
    analisis_operativo = st.text_area("Análisis o balance operativo")
    recomendaciones = st.text_area("Recomendaciones o sugerencias")

    enviar = st.form_submit_button("📤 Generar Informe PPTX")

# ---- Cargar plantilla personalizada desde GitHub ----
@st.cache_resource
def cargar_plantilla(url):
    respuesta = requests.get(url)
    return BytesIO(respuesta.content)

# ---- Generar presentación basada en plantilla ----
def generar_pptx(datos, plantilla_bytes):
    prs = Presentation(plantilla_bytes)

    # Portada - Slide 1 (solo Delegación y Dirección Regional)
    portada = prs.slides[0]
    for shape in portada.shapes:
        if shape.has_text_frame:
            texto = shape.text_frame.text
            texto = texto.replace("DELEGACION_POLICIAL", datos['delegacion_policial'])
            texto = texto.replace("DIRECCION_REGIONAL", datos['direccion_regional'])
            shape.text_frame.text = texto

    # Segunda diapositiva - Datos del dispositivo
    slide_dispositivo = prs.slides.add_slide(prs.slide_layouts[1])
    titulo = slide_dispositivo.shapes.title
    contenido = slide_dispositivo.placeholders[1]

    titulo.text = "Información General del Dispositivo"
    contenido.text = (
        f"Nombre del Dispositivo: {datos['nombre_dispositivo']}\n"
        f"Responsable: {datos['nombre_responsable']}\n"
        f"Cargo del Responsable: {datos['cargo_responsable']}\n"
        f"Fecha de Ejecución: {datos['fecha_ejecucion']}"
    )

    # Tercera diapositiva - Resultados
    slide_resultados = prs.slides.add_slide(prs.slide_layouts[1])
    titulo = slide_resultados.shapes.title
    contenido = slide_resultados.placeholders[1]

    titulo.text = "Resultados Obtenidos"
    contenido.text = datos['descripcion_resultados']

    # Cuarta diapositiva - Análisis operativo
    slide_analisis = prs.slides.add_slide(prs.slide_layouts[1])
    titulo = slide_analisis.shapes.title
    contenido = slide_analisis.placeholders[1]

    titulo.text = "Análisis Operativo"
    contenido.text = datos['analisis_operativo']

    # Quinta diapositiva - Recomendaciones
    slide_recomendaciones = prs.slides.add_slide(prs.slide_layouts[1])
    titulo = slide_recomendaciones.shapes.title
    contenido = slide_recomendaciones.placeholders[1]

    titulo.text = "Recomendaciones"
    contenido.text = datos['recomendaciones']

    # Guardar presentación en memoria
    ppt_buffer = BytesIO()
    prs.save(ppt_buffer)
    ppt_buffer.seek(0)
    return ppt_buffer

# ---- Lógica después de enviar el formulario ----
if enviar:
    campos = [
        nombre_dispositivo, nombre_responsable, cargo_responsable,
        direccion_regional, delegacion_policial, fecha_ejecucion,
        descripcion_resultados, analisis_operativo, recomendaciones
    ]
    if not all(campos):
        st.error("⚠️ Completa todos los campos para generar el informe.")
    else:
        st.success("✅ Informe generado correctamente.")

        # URL correcta de tu plantilla en GitHub
        plantilla_url = "https://github.com/CB230494/Formulario-a-Presentacion-Streamlit/raw/refs/heads/main/plantilla_personalizada.pptx"
        plantilla_bytes = cargar_plantilla(plantilla_url)

        datos = {
            'nombre_dispositivo': nombre_dispositivo,
            'nombre_responsable': nombre_responsable,
            'cargo_responsable': cargo_responsable,
            'direccion_regional': f"Dirección Regional {direccion_regional}",
            'delegacion_policial': delegacion_policial,
            'fecha_ejecucion': fecha_ejecucion.strftime("%d/%m/%Y"),
            'descripcion_resultados': descripcion_resultados,
            'analisis_operativo': analisis_operativo,
            'recomendaciones': recomendaciones
        }

        ppt_buffer = generar_pptx(datos, plantilla_bytes)

        nombre_archivo = f"Informe_{nombre_dispositivo.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d')}.pptx"

        st.download_button(
            label="📥 Descargar Informe PPTX",
            data=ppt_buffer,
            file_name=nombre_archivo,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )

