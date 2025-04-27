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
    antecedentes["Identificación de errores en la elaboración de órdenes de ejecución anteriores."] = st.selectbox("", opciones)
    antecedentes["Abordaje de acciones estratégicas vinculadas a la línea de acción o a causas socioculturales y estructurales."] = st.selectbox("", opciones)
    antecedentes["Correcta utilización de los insumos del informe territorial (datos de participación, percepción, etc.)."] = st.selectbox("", opciones)
    antecedentes["Coherencia entre la problemática priorizada y la redacción de la ambientación y finalidad."] = st.selectbox("", opciones)
    antecedentes["Aplicación adecuada de las fases preoperativa, operativa y postoperativa."] = st.selectbox("", opciones)
    antecedentes["Documentación completa de balances operativos o informes de resultados."] = st.selectbox("", opciones)

    st.subheader("🔹 Evaluación de la Aplicación de Insumos Mostrados en el Taller")
    insumos = {}
    insumos["Datos de Participación"] = st.selectbox("Datos de Participación", opciones)
    insumos["Análisis Estructural"] = st.selectbox("Análisis Estructural", opciones)
    insumos["Causas Socioculturales y Estructurales"] = st.selectbox("Causas Socioculturales y Estructurales", opciones)
    insumos["Percepción Ciudadana"] = st.selectbox("Percepción Ciudadana", opciones)
    insumos["Victimización Ciudadana"] = st.selectbox("Victimización Ciudadana", opciones)
    insumos["Problemáticas Priorizadas"] = st.selectbox("Problemáticas Priorizadas", opciones)

    st.subheader("🔹 Evaluación de la Elaboración de la Orden de Ejecución durante el Taller")
    orden = {}
    orden["Portada"] = st.selectbox("Portada", opciones)
    orden["Título"] = st.selectbox("Título", opciones)
    orden["Código"] = st.selectbox("Código", opciones)
    orden["Fecha de Ejecución"] = st.selectbox("Fecha de Ejecución", opciones)
    orden["Vigencia de la Operación"] = st.selectbox("Vigencia de la Operación", opciones)

    st.subheader("🔹 Evaluación de las Fases de la Orden de Ejecución")
    fases = {}
    fases["Ambientación"] = st.selectbox("Ambientación", opciones)
    fases["Finalidad"] = st.selectbox("Finalidad", opciones)
    fases["Fase Preoperativa"] = st.selectbox("Fase Preoperativa", opciones)
    fases["Fase Operativa"] = st.selectbox("Fase Operativa", opciones)
    fases["Fase Postoperativa"] = st.selectbox("Fase Postoperativa", opciones)

    st.subheader("🔹 Seguimiento: Matrices, Actividades, Indicadores y Metas")
    seguimiento = {}
    seguimiento["Se revisó y ajustó las actividades estratégicas de líneas de acción."] = st.selectbox("", opciones)
    seguimiento["Se revisó y ajustó los indicadores de las líneas de acción."] = st.selectbox("", opciones)
    seguimiento["Se revisó y actualizó la meta planteada para la ejecución del año 2025."] = st.selectbox("", opciones)
    seguimiento["Se revisó y actualizó la meta bianual."] = st.selectbox("", opciones)
    seguimiento["Se actualizaron las metas en el Informe Trimestral de avance de líneas de acción."] = st.selectbox("", opciones)

    st.subheader("🔹 Conclusión Final")
    conclusion = st.text_area("Conclusión Final")

    enviar = st.form_submit_button("📤 Generar Informe PDF")

# ---- FUNCIONES ----
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

    pdf.ln(15)
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, 'Datos Generales', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0)
    for k, v in datos["datos_generales"].items():
        pdf.cell(0, 8, f"{k}: {v}", ln=True)

    # ---- Agregamos textos institucionales ----
    def add_section(title, content):
        pdf.ln(8)
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, title, ln=True)
        pdf.set_font('Arial', '', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 8, content)

    objetivo = ("El objetivo principal del acompañamiento fue fortalecer las competencias operativas y preventivas del personal policial "
                "en la elaboración de órdenes de ejecución, basadas en el análisis de informe territorial, percepción ciudadana, causas "
                "socioculturales y estructurales, así como en las problemáticas priorizadas, fomentando también la correcta documentación "
                "de balances operativos e informes de gestión, en el marco de la Estrategia Integral Sembremos Seguridad.")
    add_section("Objetivo del Acompañamiento", objetivo)

    antecedentes_intro = "Durante la revisión de las órdenes de ejecución previas, se identificaron los siguientes hallazgos:"
    add_section("Antecedentes como Referencia para el Taller", antecedentes_intro)

    for k, v in datos["antecedentes"].items():
        pdf.cell(0, 8, f"{k} - Cumple: {v}", ln=True)

    resultados_esperados = ("Resultados Esperados:\n"
                            "- Revisar las órdenes de ejecución previas para identificar áreas de mejora.\n"
                            "- Fortalecer la capacidad del personal policial para redactar órdenes de ejecución claras, basadas en insumos estratégicos.\n"
                            "- Actualizar actividades estratégicas, indicadores y metas, asegurando su alineación con las problemáticas priorizadas.")
    add_section("Implementación del Taller", resultados_esperados)

    add_section("Evaluación de la Aplicación de Insumos Mostrados en el Taller", "")
    for k, v in datos["insumos"].items():
        pdf.cell(0, 8, f"{k} - Cumple: {v}", ln=True)

    add_section("Evaluación de la Elaboración de la Orden de Ejecución durante el Taller", "")
    for k, v in datos["orden"].items():
        pdf.cell(0, 8, f"{k} - Cumple: {v}", ln=True)

    add_section("Evaluación de las Fases de la Orden de Ejecución", "")
    for k, v in datos["fases"].items():
        pdf.cell(0, 8, f"{k} - Cumple: {v}", ln=True)

    add_section("Seguimiento: Matrices, Actividades, Indicadores y Metas", "")
    for k, v in datos["seguimiento"].items():
        pdf.cell(0, 8, f"{k} - Cumple: {v}", ln=True)

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
