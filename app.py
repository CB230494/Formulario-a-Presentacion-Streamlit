import streamlit as st
from fpdf import FPDF
import datetime
from io import BytesIO

st.set_page_config(page_title="Generador de Informe de Acompañamiento", layout="centered")
st.title("🚔 Estrategia Sembremos Seguridad-Informe de Acompañamiento Taller 2025 ")

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
    antecedentes = {
        "Identificación de errores en la elaboración de órdenes de ejecución anteriores.": st.selectbox("Identificación de errores en la elaboración de órdenes de ejecución anteriores.", opciones, key="antecedente1"),
        "Abordaje de acciones estratégicas vinculadas a la línea de acción o a causas socioculturales y estructurales.": st.selectbox("Abordaje de acciones estratégicas vinculadas a la línea de acción o a causas socioculturales y estructurales.", opciones, key="antecedente2"),
        "Correcta utilización de los insumos del informe territorial (datos de participación, percepción, etc.).": st.selectbox("Correcta utilización de los insumos del informe territorial.", opciones, key="antecedente3"),
        "Coherencia entre la problemática priorizada y la redacción de la ambientación y finalidad.": st.selectbox("Coherencia entre problemática y ambientación.", opciones, key="antecedente4"),
        "Aplicación adecuada de las fases preoperativa, operativa y postoperativa.": st.selectbox("Aplicación adecuada de las fases operativas.", opciones, key="antecedente5"),
        "Documentación completa de balances operativos o informes de resultados.": st.selectbox("Documentación completa de balances operativos.", opciones, key="antecedente6")
    }

    st.subheader("🔹 Evaluación de la Aplicación de Insumos Mostrados en el Taller")
    insumos = {
        "Datos de Participación": st.selectbox("Datos de Participación", opciones, key="insumo1"),
        "Análisis Estructural": st.selectbox("Análisis Estructural", opciones, key="insumo2"),
        "Causas Socioculturales y Estructurales": st.selectbox("Causas Socioculturales y Estructurales", opciones, key="insumo3"),
        "Percepción Ciudadana": st.selectbox("Percepción Ciudadana", opciones, key="insumo4"),
        "Victimización Ciudadana": st.selectbox("Victimización Ciudadana", opciones, key="insumo5"),
        "Problemáticas Priorizadas": st.selectbox("Problemáticas Priorizadas", opciones, key="insumo6")
    }

    st.subheader("🔹 Evaluación de la Elaboración de la Orden de Ejecución durante el Taller")
    orden = {
        "Portada": st.selectbox("Portada", opciones, key="orden1"),
        "Título": st.selectbox("Título", opciones, key="orden2"),
        "Código": st.selectbox("Código", opciones, key="orden3"),
        "Fecha de Ejecución": st.selectbox("Fecha de Ejecución", opciones, key="orden4"),
        "Vigencia de la Operación": st.selectbox("Vigencia de la Operación", opciones, key="orden5")
    }

    st.subheader("🔹 Evaluación de las Fases de la Orden de Ejecución")
    fases = {
        "Ambientación": st.selectbox("Ambientación", opciones, key="fase1"),
        "Finalidad": st.selectbox("Finalidad", opciones, key="fase2"),
        "Fase Preoperativa": st.selectbox("Fase Preoperativa", opciones, key="fase3"),
        "Fase Operativa": st.selectbox("Fase Operativa", opciones, key="fase4"),
        "Fase Postoperativa": st.selectbox("Fase Postoperativa", opciones, key="fase5")
    }

    st.subheader("🔹 Seguimiento: Matrices, Actividades, Indicadores y Metas")
    seguimiento = {
        "Se revisó y ajustó las actividades estratégicas de líneas de acción.": st.selectbox("Actividades estratégicas ajustadas", opciones, key="seguimiento1"),
        "Se revisó y ajustó los indicadores de las líneas de acción.": st.selectbox("Indicadores ajustados", opciones, key="seguimiento2"),
        "Se revisó y actualizó la meta planteada para la ejecución del año 2025.": st.selectbox("Meta 2025 actualizada", opciones, key="seguimiento3"),
        "Se revisó y actualizó la meta bianual.": st.selectbox("Meta bianual actualizada", opciones, key="seguimiento4"),
        "Se actualizaron las metas en el Informe Trimestral de avance de líneas de acción.": st.selectbox("Informe trimestral actualizado", opciones, key="seguimiento5")
    }

    st.subheader("🔹 Conclusión Final")
    conclusion = st.text_area("Conclusión Final")

    enviar = st.form_submit_button("📤 Generar Informe PDF")
# ---- FUNCIÓN PARA CREAR EL PDF CORREGIDO ----
class PDF(FPDF):
    def header(self):
        

        # Colocar el logo centrado dentro del cuadro
        self.image('logo.png', 9, 6, 22)  # Un poquito más pequeño que el cuadro

        # Espacio debajo del logo
        self.set_y(10)
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 102, 0)  # Verde oscuro

        # Título en dos líneas
        self.cell(0, 5, 'Estrategia Sembremos Seguridad', ln=True, align='C')
        self.cell(0, 8, 'Generador de Informe de Acompañamiento 2025', ln=True, align='C')

        # Línea verde inferior
        self.set_draw_color(0, 102, 0)
        self.set_line_width(0.8)
        self.line(35, 25, 200, 25)


    def footer(self):
        self.set_y(-20)
        self.set_font('Arial', 'I', 10)
        self.set_text_color(0, 102, 0)
        self.cell(0, 10, 'Modelo Preventivo de Gestión Policial - Estrategia Sembremos Seguridad', align='C')






def generar_pdf(datos):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    tablas_contador = 0  # Controlar manualmente cuántas tablas llevamos

    def add_section(title, content):
        pdf.ln(8)
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(0, 102, 0)
        pdf.cell(0, 10, title, ln=True)
        pdf.ln(2)
        pdf.set_font('Arial', '', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 8, content)

    def add_table(title, checklist, extra_text=None, salto_pagina=True):
        nonlocal_tablas = 0  # Esta variable va solo dentro del método para local control

        if tablas_contador % 2 == 0 and tablas_contador != 0 and salto_pagina:
            pdf.add_page()

        pdf.ln(8)
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(0, 102, 0)
        pdf.cell(0, 10, title, ln=True)
        pdf.ln(4)

        if extra_text:
            pdf.set_font('Arial', '', 12)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 8, extra_text)
            pdf.ln(2)

        col_widths = [140, 40]

        pdf.set_font('Arial', 'B', 12)
        pdf.cell(col_widths[0], 8, "Aspecto Evaluado", border=1, align='C')
        pdf.cell(col_widths[1], 8, "Cumple", border=1, align='C')
        pdf.ln()

        pdf.set_font('Arial', '', 11)
        pdf.set_text_color(0, 0, 0)

        for aspecto, cumple in checklist.items():
            num_lines = 1
            text_width = pdf.get_string_width(aspecto)
            if text_width > col_widths[0]:
                num_lines = int(text_width / col_widths[0]) + 1
            altura_fila = 8 * num_lines

            if pdf.get_y() + altura_fila > 270:
                pdf.add_page()
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(col_widths[0], 8, "Aspecto Evaluado", border=1, align='C')
                pdf.cell(col_widths[1], 8, "Cumple", border=1, align='C')
                pdf.ln()
                pdf.set_font('Arial', '', 11)

            x_start = pdf.get_x()
            y_start = pdf.get_y()
            pdf.multi_cell(col_widths[0], 8, aspecto, border=1)

            y_end = pdf.get_y()

            pdf.set_xy(x_start + col_widths[0], y_start)
            pdf.cell(col_widths[1], altura_fila, cumple, border=1, align='C')

            pdf.set_y(y_end)

    # ---- Página 1: Títulos y textos ----
    add_section("Datos Generales", "\n".join([f"{k}: {v}" for k, v in datos["datos_generales"].items()]))

    add_section("Objetivo del Acompañamiento",
            "El objetivo principal del acompañamiento fue fortalecer las competencias operativas y preventivas del personal policial en la elaboración de órdenes de ejecución, a partir del análisis del informe territorial, la percepción ciudadana, las causas socioculturales y estructurales, así como de las problemáticas priorizadas. "
            "Asimismo, se brindó orientación en la identificación y utilización de los elementos esenciales contenidos en el informe territorial, con el propósito de mejorar la planificación de las intervenciones policiales. "
            "Todo esto se desarrolló fomentando la correcta documentación de balances operativos e informes de gestión, en el marco de la Estrategia Integral Sembremos Seguridad.")





    pdf.add_page()

    # ---- Página 2 y 3: Tablas ----
    add_table(
        "Antecedentes como Referencia para el Taller",
        datos["antecedentes"],
        extra_text="Durante la revisión de las órdenes de ejecución previas, se identificaron los siguientes hallazgos:"
    )
    tablas_contador += 1

    add_table("Evaluación de la Aplicación de Insumos Mostrados en el Taller",
    datos["insumos"],
    extra_text="Se evaluó el uso adecuado de los insumos clave del taller, identificando fortalezas y áreas de mejora en la elaboración de órdenes de ejecución basadas en el diagnóstico territorial.")
    tablas_contador += 1


    add_table("Evaluación de la Elaboración de la Orden de Ejecución durante el Taller", datos["orden"])
    tablas_contador += 1

    add_table("Evaluación de las Fases de la Orden de Ejecución", datos["fases"])
    tablas_contador += 1

    # ---- NUEVA PÁGINA para el cuadro 5 + Conclusión
    pdf.add_page()

    add_table("Seguimiento: Matrices, Actividades, Indicadores y Metas", datos["seguimiento"], salto_pagina=False)
    tablas_contador += 1

    pdf.ln(10)
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 102, 0)
    pdf.cell(0, 10, 'Conclusión Final', ln=True)
    pdf.ln(4)
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, datos["conclusion"])

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer





# ---- BOTÓN PARA GENERAR Y DESCARGAR PDF ----
if enviar:
    if not delegacion or not fecha_realizacion or not facilitadores or not jefe:
        st.error("⚠️ Completa todos los campos principales para generar el informe.")
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



