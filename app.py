import streamlit as st
from fpdf import FPDF
import datetime
from io import BytesIO

st.set_page_config(page_title="Generador de Informe de Acompañamiento", layout="centered")

st.title("🚔 Generador de Informe de Acompañamiento - Estrategia Sembremos Seguridad")

# ---- FORMULARIO ----
with st.form("formulario_informe"):
    st.subheader("🔹 Datos Generales")
    delegacion = st.text_input("Delegación Policial")
    fecha_realizacion = st.date_input("Fecha de Realización")
    facilitadores = st.text_input("Facilitadores")
    jefe = st.text_input("Jefe")
    subjefe = st.text_input("Subjefe")
    agentes_operacionales = st.text_input("Agente(s) Operacionales")
    agente_preventivos = st.text_input("Agente de Programas Policiales Preventivos")

    opciones = ["Sí", "No"]

    st.subheader("🔹 Antecedentes como Referencia para el Taller")
    antecedentes = {}
    antecedentes["Identificación de errores en la elaboración de órdenes de ejecución anteriores."] = st.selectbox(
        "Identificación de errores en la elaboración de órdenes de ejecución anteriores.", opciones, key="antecedente_1")
    antecedentes["Abordaje de acciones estratégicas vinculadas a la línea de acción o a causas socioculturales y estructurales."] = st.selectbox(
        "Abordaje de acciones estratégicas vinculadas a la línea de acción o a causas socioculturales y estructurales.", opciones, key="antecedente_2")
    antecedentes["Correcta utilización de los insumos del informe territorial (datos de participación, percepción, etc.)."] = st.selectbox(
        "Correcta utilización de los insumos del informe territorial (datos de participación, percepción, etc.).", opciones, key="antecedente_3")
    antecedentes["Coherencia entre la problemática priorizada y la redacción de la ambientación y finalidad."] = st.selectbox(
        "Coherencia entre la problemática priorizada y la redacción de la ambientación y finalidad.", opciones, key="antecedente_4")
    antecedentes["Aplicación adecuada de las fases preoperativa, operativa y postoperativa."] = st.selectbox(
        "Aplicación adecuada de las fases preoperativa, operativa y postoperativa.", opciones, key="antecedente_5")
    antecedentes["Documentación completa de balances operativos o informes de resultados."] = st.selectbox(
        "Documentación completa de balances operativos o informes de resultados.", opciones, key="antecedente_6")

    st.subheader("🔹 Evaluación de la Aplicación de Insumos Mostrados en el Taller")
    insumos = {}
    insumos["Datos de Participación"] = st.selectbox("Datos de Participación", opciones, key="insumo_1")
    insumos["Análisis Estructural"] = st.selectbox("Análisis Estructural", opciones, key="insumo_2")
    insumos["Causas Socioculturales y Estructurales"] = st.selectbox("Causas Socioculturales y Estructurales", opciones, key="insumo_3")
    insumos["Percepción Ciudadana"] = st.selectbox("Percepción Ciudadana", opciones, key="insumo_4")
    insumos["Victimización Ciudadana"] = st.selectbox("Victimización Ciudadana", opciones, key="insumo_5")
    insumos["Problemáticas Priorizadas"] = st.selectbox("Problemáticas Priorizadas", opciones, key="insumo_6")

    st.subheader("🔹 Evaluación de la Elaboración de la Orden de Ejecución durante el Taller")
    orden = {}
    orden["Portada"] = st.selectbox("Portada", opciones, key="orden_1")
    orden["Título"] = st.selectbox("Título", opciones, key="orden_2")
    orden["Código"] = st.selectbox("Código", opciones, key="orden_3")
    orden["Fecha de Ejecución"] = st.selectbox("Fecha de Ejecución", opciones, key="orden_4")
    orden["Vigencia de la Operación"] = st.selectbox("Vigencia de la Operación", opciones, key="orden_5")

    st.subheader("🔹 Evaluación de las Fases de la Orden de Ejecución")
    fases = {}
    fases["Ambientación"] = st.selectbox("Ambientación", opciones, key="fase_1")
    fases["Finalidad"] = st.selectbox("Finalidad", opciones, key="fase_2")
    fases["Fase Preoperativa"] = st.selectbox("Fase Preoperativa", opciones, key="fase_3")
    fases["Fase Operativa"] = st.selectbox("Fase Operativa", opciones, key="fase_4")
    fases["Fase Postoperativa"] = st.selectbox("Fase Postoperativa", opciones, key="fase_5")

    st.subheader("🔹 Seguimiento: Matrices, Actividades, Indicadores y Metas")
    seguimiento = {}
    seguimiento["Se revisó y ajustó las actividades estratégicas de líneas de acción."] = st.selectbox(
        "Se revisó y ajustó las actividades estratégicas de líneas de acción.", opciones, key="seguimiento_1")
    seguimiento["Se revisó y ajustó los indicadores de las líneas de acción."] = st.selectbox(
        "Se revisó y ajustó los indicadores de las líneas de acción.", opciones, key="seguimiento_2")
    seguimiento["Se revisó y actualizó la meta planteada para la ejecución del año 2025."] = st.selectbox(
        "Se revisó y actualizó la meta planteada para la ejecución del año 2025.", opciones, key="seguimiento_3")
    seguimiento["Se revisó y actualizó la meta bianual."] = st.selectbox(
        "Se revisó y actualizó la meta bianual.", opciones, key="seguimiento_4")
    seguimiento["Se actualizaron las metas en el Informe Trimestral de avance de líneas de acción."] = st.selectbox(
        "Se actualizaron las metas en el Informe Trimestral de avance de líneas de acción.", opciones, key="seguimiento_5")

    st.subheader("🔹 Conclusión Final")
    conclusion = st.text_area("Conclusión Final")

    enviar = st.form_submit_button("📤 Generar Informe PDF")
# ---- FUNCIÓN PARA CREAR EL PDF ----
class PDF(FPDF):
    def header(self):
        self.set_fill_color(0, 51, 102)
        self.rect(0, 0, 210, 15, 'F')
        self.set_y(5)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, 'Informe de Acompañamiento - Sembremos Seguridad', ln=True, align='C')

    def footer(self):
        self.set_y(-20)
        self.set_font('Arial', 'I', 10)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, 'Dirección de Programas Policiales Preventivos - Estrategia Sembremos Seguridad', align='C')

def generar_pdf(datos):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ---- Función para agregar sección de texto ----
    def add_section(title, content):
        pdf.ln(8)
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, title, ln=True)
        pdf.set_font('Arial', '', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 8, content)

    # ---- Función para agregar tablas de checklist ----
    def add_table_section(title, checklist_dict):
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, title, ln=True)

        pdf.ln(4)
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(0, 0, 0)

        # Encabezado tabla
        pdf.cell(140, 8, 'Aspecto Evaluado', border=1, align='C')
        pdf.cell(40, 8, 'Cumple', border=1, align='C')
        pdf.ln()

        pdf.set_font('Arial', '', 11)
        for aspecto, resultado in checklist_dict.items():
            pdf.cell(140, 8, aspecto, border=1)
            pdf.cell(40, 8, resultado, border=1, align='C')
            pdf.ln()

    # ---- Contenido ----
    pdf.ln(10)
    add_section("Datos Generales", "")
    for k, v in datos["datos_generales"].items():
        pdf.multi_cell(0, 8, f"{k}: {v}")

    add_section("Objetivo del Acompañamiento",
                "El objetivo principal del acompañamiento fue fortalecer las competencias operativas y preventivas del personal policial "
                "en la elaboración de órdenes de ejecución, basadas en el análisis de informe territorial, percepción ciudadana, causas "
                "socioculturales y estructurales, así como en las problemáticas priorizadas, fomentando también la correcta documentación "
                "de balances operativos e informes de gestión, en el marco de la Estrategia Integral Sembremos Seguridad.")

    add_section("Antecedentes como Referencia para el Taller",
                "Durante la revisión de las órdenes de ejecución previas, se identificaron los siguientes hallazgos:")

    add_table_section("Antecedentes como Referencia para el Taller", datos["antecedentes"])

    add_section("Implementación del Taller",
                "Resultados Esperados:\n"
                "- Revisar las órdenes de ejecución previas para identificar áreas de mejora.\n"
                "- Fortalecer la capacidad del personal policial para redactar órdenes de ejecución claras, basadas en insumos estratégicos.\n"
                "- Actualizar actividades estratégicas, indicadores y metas, asegurando su alineación con las problemáticas priorizadas.")

    add_table_section("Evaluación de la Aplicación de Insumos Mostrados en el Taller", datos["insumos"])

    add_table_section("Evaluación de la Elaboración de la Orden de Ejecución durante el Taller", datos["orden"])

    add_table_section("Evaluación de las Fases de la Orden de Ejecución", datos["fases"])

    add_table_section("Seguimiento: Matrices, Actividades, Indicadores y Metas", datos["seguimiento"])

    pdf.ln(10)
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, 'Conclusión Final', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, datos["conclusion"])

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer
# ---- DESPUÉS DE ENVIAR FORMULARIO ----
if enviar:
    if not delegacion or not fecha_realizacion or not facilitadores or not jefe:
        st.error("⚠️ Completa todos los campos para generar el informe.")
    else:
        datos = {
            "datos_generales": {
                "Delegación Policial": delegacion,
                "Fecha de Realización": fecha_realizacion.strftime("%d/%m/%Y"),
                "Facilitadores": facilitadores,
                "Jefe": jefe,
                "Subjefe": subjefe,
                "Agente(s) Operacionales": agentes_operacionales,
                "Agente de Programas Policiales Preventivos": agente_preventivos,
            },
            "antecedentes": antecedentes,
            "insumos": insumos,
            "orden": orden,
            "fases": fases,
            "seguimiento": seguimiento,
            "conclusion": conclusion
        }

        pdf_buffer = generar_pdf(datos)

        nombre_archivo = f"Informe_Acompanamiento_{delegacion.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d')}.pdf"

        st.download_button(
            label="📥 Descargar Informe en PDF",
            data=pdf_buffer,
            file_name=nombre_archivo,
            mime="application/pdf"
        )

