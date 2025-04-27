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

    st.subheader("🔹 Checklist: Antecedentes como Referencia para el Taller")
    antecedentes = {}
    antecedentes["Errores en órdenes anteriores"] = st.selectbox("Identificación de errores", ["Sí", "No", "Parcial"])
    antecedentes["Acciones estratégicas línea de acción"] = st.selectbox("Abordaje de acciones estratégicas", ["Sí", "No", "Parcial"])
    antecedentes["Uso de informe territorial"] = st.selectbox("Utilización de insumos de informe territorial", ["Sí", "No", "Parcial"])
    antecedentes["Coherencia problemática-ambientación"] = st.selectbox("Coherencia problemática-ambientación", ["Sí", "No", "Parcial"])
    antecedentes["Aplicación fases operativas"] = st.selectbox("Aplicación de fases pre, operativa y post", ["Sí", "No", "Parcial"])
    antecedentes["Documentación balances e informes"] = st.selectbox("Documentación de balances e informes", ["Sí", "No", "Parcial"])

    st.subheader("🔹 Checklist: Evaluación de Insumos Mostrados en el Taller")
    insumos = {}
    insumos["Datos de Participación"] = st.selectbox("Uso de Datos de Participación", ["Sí", "No", "Parcial"])
    insumos["Análisis Estructural"] = st.selectbox("Uso de Análisis Estructural", ["Sí", "No", "Parcial"])
    insumos["Causas Socioculturales y Estructurales"] = st.selectbox("Uso de Causas Socioculturales y Estructurales", ["Sí", "No", "Parcial"])
    insumos["Percepción Ciudadana"] = st.selectbox("Uso de Percepción Ciudadana", ["Sí", "No", "Parcial"])
    insumos["Victimización Ciudadana"] = st.selectbox("Uso de Victimización Ciudadana", ["Sí", "No", "Parcial"])
    insumos["Problemáticas Priorizadas"] = st.selectbox("Uso de Problemáticas Priorizadas", ["Sí", "No", "Parcial"])

    st.subheader("🔹 Checklist: Evaluación de la Elaboración de la Orden de Ejecución")
    orden = {}
    orden["Portada"] = st.selectbox("Correcta Portada", ["Sí", "No", "Parcial"])
    orden["Título"] = st.selectbox("Correcto Título", ["Sí", "No", "Parcial"])
    orden["Código"] = st.selectbox("Correcto Código", ["Sí", "No", "Parcial"])
    orden["Fecha de Ejecución"] = st.selectbox("Correcta Fecha de Ejecución", ["Sí", "No", "Parcial"])
    orden["Vigencia de la Operación"] = st.selectbox("Correcta Vigencia de la Operación", ["Sí", "No", "Parcial"])

    st.subheader("🔹 Checklist: Evaluación de las Fases de la Orden de Ejecución")
    fases = {}
    fases["Ambientación"] = st.selectbox("Ambientación", ["Sí", "No", "Parcial"])
    fases["Finalidad"] = st.selectbox("Finalidad", ["Sí", "No", "Parcial"])
    fases["Fase Preoperativa"] = st.selectbox("Fase Preoperativa", ["Sí", "No", "Parcial"])
    fases["Fase Operativa"] = st.selectbox("Fase Operativa", ["Sí", "No", "Parcial"])
    fases["Fase Postoperativa"] = st.selectbox("Fase Postoperativa", ["Sí", "No", "Parcial"])

    st.subheader("🔹 Checklist: Seguimiento (Matrices, Actividades, Metas)")
    seguimiento = {}
    seguimiento["Actividades Estratégicas"] = st.selectbox("Revisión de Actividades Estratégicas", ["Sí", "No", "Parcial"])
    seguimiento["Indicadores"] = st.selectbox("Revisión de Indicadores", ["Sí", "No", "Parcial"])
    seguimiento["Meta 2025"] = st.selectbox("Revisión de Meta 2025", ["Sí", "No", "Parcial"])
    seguimiento["Meta Bianual"] = st.selectbox("Revisión de Meta Bianual", ["Sí", "No", "Parcial"])
    seguimiento["Actualización Informe Trimestral"] = st.selectbox("Actualización de Informe Trimestral", ["Sí", "No", "Parcial"])

    st.subheader("🔹 Conclusión Final")
    conclusion = st.text_area("Escribe una Conclusión Final")

    enviar = st.form_submit_button("📤 Generar Informe PDF")

# ---- FUNCIONES ----
class PDF(FPDF):
    def header(self):
        self.set_fill_color(0, 51, 102)  # Azul
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

    # Sección de Datos Generales
    pdf.ln(15)
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, 'Datos Generales', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0)
    for k, v in datos["datos_generales"].items():
        pdf.cell(0, 8, f"{k}: {v}", ln=True)

    # Otras secciones
    def add_checklist_section(title, checklist):
        pdf.ln(8)
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, title, ln=True)
        pdf.set_font('Arial', '', 12)
        pdf.set_text_color(0, 0, 0)
        for k, v in checklist.items():
            pdf.cell(0, 8, f"{k}: {v}", ln=True)

    add_checklist_section('Antecedentes como Referencia para el Taller', datos["antecedentes"])
    add_checklist_section('Evaluación de Insumos Mostrados', datos["insumos"])
    add_checklist_section('Evaluación de Orden de Ejecución', datos["orden"])
    add_checklist_section('Evaluación de las Fases de Orden', datos["fases"])
    add_checklist_section('Seguimiento de Matrices y Metas', datos["seguimiento"])

    # Conclusión
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, 'Conclusión Final', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, datos["conclusion"])

    # Guardar en memoria
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
                "Agentes Operacionales": agentes_operacionales,
                "Agente Preventivos": agente_preventivos,
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


