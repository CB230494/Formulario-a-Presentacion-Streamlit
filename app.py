import streamlit as st
from fpdf import FPDF
import datetime
from io import BytesIO

st.set_page_config(page_title="Generador de Informe en PDF", layout="centered")

st.title("🚔 Generador de Informe de Dispositivo Policial en PDF")

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

    enviar = st.form_submit_button("📤 Generar Informe PDF")

# ---- FUNCIONES ----
class PDF(FPDF):
    def header(self):
        # Línea azul en la parte superior
        self.set_fill_color(0, 51, 102)  # Azul institucional
        self.rect(0, 0, 210, 15, 'F')
        self.set_y(5)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(255, 255, 255)  # Blanco
        self.cell(0, 10, 'Informe de Dispositivo Policial', ln=True, align='C')

    def footer(self):
        self.set_y(-20)
        self.set_font('Arial', 'I', 10)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, 'Dirección de Programas Policiales Preventivos - Sembremos Seguridad', align='C')

def generar_pdf(datos):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Espaciado después del encabezado
    pdf.ln(10)

    # Información general
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, 'Información General', ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.ln(2)
    pdf.multi_cell(0, 8, 
        f"Delegación Policial: {datos['delegacion_policial']}\n"
        f"Dirección Regional: {datos['direccion_regional']}\n"
        f"Nombre del Dispositivo: {datos['nombre_dispositivo']}\n"
        f"Responsable: {datos['nombre_responsable']}\n"
        f"Cargo del Responsable: {datos['cargo_responsable']}\n"
        f"Fecha de Ejecución: {datos['fecha_ejecucion']}"
    )

    pdf.ln(8)

    # Resultados
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, 'Resultados Obtenidos', ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.ln(2)
    pdf.multi_cell(0, 8, datos['descripcion_resultados'])

    pdf.ln(8)

    # Análisis Operativo
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, 'Análisis Operativo', ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.ln(2)
    pdf.multi_cell(0, 8, datos['analisis_operativo'])

    pdf.ln(8)

    # Recomendaciones
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, 'Recomendaciones', ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.ln(2)
    pdf.multi_cell(0, 8, datos['recomendaciones'])

    # Guardar en memoria
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    return buffer

# ---- DESPUÉS DE ENVIAR FORMULARIO ----
if enviar:
    campos = [
        nombre_dispositivo, nombre_responsable, cargo_responsable,
        direccion_regional, delegacion_policial, fecha_ejecucion,
        descripcion_resultados, analisis_operativo, recomendaciones
    ]
    if not all(campos):
        st.error("⚠️ Completa todos los campos para generar el informe.")
    else:
        st.success("✅ Informe PDF generado correctamente.")

        datos = {
            'nombre_dispositivo': nombre_dispositivo,
            'nombre_responsable': nombre_responsable,
            'cargo_responsable': cargo_responsable,
            'direccion_regional': direccion_regional,
            'delegacion_policial': delegacion_policial,
            'fecha_ejecucion': fecha_ejecucion.strftime("%d/%m/%Y"),
            'descripcion_resultados': descripcion_resultados,
            'analisis_operativo': analisis_operativo,
            'recomendaciones': recomendaciones
        }

        pdf_buffer = generar_pdf(datos)

        nombre_archivo = f"Informe_{nombre_dispositivo.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d')}.pdf"

        st.download_button(
            label="📥 Descargar Informe en PDF",
            data=pdf_buffer,
            file_name=nombre_archivo,
            mime="application/pdf"
        )

