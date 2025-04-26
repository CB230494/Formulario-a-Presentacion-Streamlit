import streamlit as st
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
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

# ---- FUNCIONES ----
@st.cache_resource
def cargar_plantilla(url):
    respuesta = requests.get(url)
    return BytesIO(respuesta.content)

def crear_diapositiva_con_estilo(prs, titulo_texto, contenido_texto):
    slide_layout = prs.slide_layouts[6]  # Layout vacío
    slide = prs.slides.add_slide(slide_layout)

    # Fondo azul claro
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(230, 240, 255)

    # Agregar título
    left = Inches(0.5)
    top = Inches(0.5)
    width = Inches(8)
    height = Inches(1)
    title_box = slide.shapes.add_textbox(left, top, width, height)
    tf = title_box.text_frame
    p = tf.add_paragraph()
    p.text = titulo_texto
    p.font.bold = True
    p.font.size = Pt(36)
    p.font.name = 'Arial'
    p.font.color.rgb = RGBColor(0, 51, 102)  # Azul oscuro

    # Agregar contenido
    left = Inches(0.5)
    top = Inches(1.8)
    width = Inches(8)
    height = Inches(4.5)
    body_box = slide.shapes.add_textbox(left, top, width, height)
    tf = body_box.text_frame
    p = tf.add_paragraph()
    p.text = contenido_texto
    p.font.size = Pt(24)
    p.font.name = 'Calibri'
    p.font.color.rgb = RGBColor(0, 0, 0)  # Negro
    tf.word_wrap = True

def mover_diapositiva(prs, index_origen, index_destino):
    xml_slides = prs.slides._sldIdLst
    slides = list(xml_slides)
    xml_slides.insert(index_destino, slides.pop(index_origen))

def generar_pptx(datos, plantilla_bytes):
    prs = Presentation(plantilla_bytes)

    # Guardar la portada (slide 0) y la página institucional (slide 1)
    portada = prs.slides[0]
    institucional = prs.slides[1]

    # Eliminar todo excepto la portada para insertar contenido
    for i in range(len(prs.slides) - 1, 0, -1):
        r_id = prs.slides._sldIdLst[i].rId
        prs.part.drop_rel(r_id)
        del prs.slides._sldIdLst[i]

    # Insertar las nuevas diapositivas generadas
    crear_diapositiva_con_estilo(prs, "Información General", 
        f"Nombre del Dispositivo: {datos['nombre_dispositivo']}\n"
        f"Responsable: {datos['nombre_responsable']}\n"
        f"Cargo del Responsable: {datos['cargo_responsable']}\n"
        f"Fecha de Ejecución: {datos['fecha_ejecucion']}"
    )

    crear_diapositiva_con_estilo(prs, "Resultados Obtenidos", datos['descripcion_resultados'])
    crear_diapositiva_con_estilo(prs, "Análisis Operativo", datos['analisis_operativo'])
    crear_diapositiva_con_estilo(prs, "Recomendaciones", datos['recomendaciones'])

    # Volver a agregar la página institucional al final
    slide_layout = prs.slide_layouts[6]  # Layout vacío
    new_slide = prs.slides.add_slide(slide_layout)
    for shape in institucional.shapes:
        el = shape.element
        new_slide.shapes._spTree.insert_element_before(el, 'p:extLst')

    # Ajustar el fondo de la última página (opcional)

    ppt_buffer = BytesIO()
    prs.save(ppt_buffer)
    ppt_buffer.seek(0)
    return ppt_buffer

# ---- ACCIÓN TRAS ENVIAR ----
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


