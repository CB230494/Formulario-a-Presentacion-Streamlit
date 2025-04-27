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
        "¿Identificación de errores en la elaboración de órdenes de ejecución anteriores?", opciones, key="antecedente_1")
    antecedentes["Abordaje de acciones estratégicas vinculadas a la línea de acción o a causas socioculturales y estructurales."] = st.selectbox(
        "¿Abordaje de acciones estratégicas vinculadas a la línea de acción o a causas socioculturales y estructurales?", opciones, key="antecedente_2")
    antecedentes["Correcta utilización de los insumos del informe territorial (datos de participación, percepción, etc.)."] = st.selectbox(
        "¿Correcta utilización de los insumos del informe territorial (datos de participación, percepción, etc.)?", opciones, key="antecedente_3")
    antecedentes["Coherencia entre la problemática priorizada y la redacción de la ambientación y finalidad."] = st.selectbox(
        "¿Coherencia entre la problemática priorizada y la redacción de la ambientación y finalidad?", opciones, key="antecedente_4")
    antecedentes["Aplicación adecuada de las fases preoperativa, operativa y postoperativa."] = st.selectbox(
        "¿Aplicación adecuada de las fases preoperativa, operativa y postoperativa?", opciones, key="antecedente_5")
    antecedentes["Documentación completa de balances operativos o informes de resultados."] = st.selectbox(
        "¿Documentación completa de balances operativos o informes de resultados?", opciones, key="antecedente_6")

    st.subheader("🔹 Evaluación de la Aplicación de Insumos Mostrados en el Taller")
    insumos = {}
    insumos["Datos de Participación"] = st.selectbox("¿Se utilizaron correctamente los Datos de Participación?", opciones, key="insumo_1")
    insumos["Análisis Estructural"] = st.selectbox("¿Se utilizó el Análisis Estructural?", opciones, key="insumo_2")
    insumos["Causas Socioculturales y Estructurales"] = st.selectbox("¿Se analizaron las Causas Socioculturales y Estructurales?", opciones, key="insumo_3")
    insumos["Percepción Ciudadana"] = st.selectbox("¿Se consideró la Percepción Ciudadana?", opciones, key="insumo_4")
    insumos["Victimización Ciudadana"] = st.selectbox("¿Se consideró la Victimización Ciudadana?", opciones, key="insumo_5")
    insumos["Problemáticas Priorizadas"] = st.selectbox("¿Se abordaron las Problemáticas Priorizadas?", opciones, key="insumo_6")

    st.subheader("🔹 Evaluación de la Elaboración de la Orden de Ejecución durante el Taller")
    orden = {}
    orden["Portada"] = st.selectbox("¿Se completó correctamente la Portada?", opciones, key="orden_1")
    orden["Título"] = st.selectbox("¿Se redactó correctamente el Título?", opciones, key="orden_2")
    orden["Código"] = st.selectbox("¿Se colocó correctamente el Código?", opciones, key="orden_3")
    orden["Fecha de Ejecución"] = st.selectbox("¿Se registró correctamente la Fecha de Ejecución?", opciones, key="orden_4")
    orden["Vigencia de la Operación"] = st.selectbox("¿Se indicó correctamente la Vigencia de la Operación?", opciones, key="orden_5")

    st.subheader("🔹 Evaluación de las Fases de la Orden de Ejecución")
    fases = {}
    fases["Ambientación"] = st.selectbox("¿La Ambientación menciona la problemática priorizada o las causas socioculturales?", opciones, key="fase_1")
    fases["Finalidad"] = st.selectbox("¿La Finalidad define claramente qué, quién y dónde?", opciones, key="fase_2")
    fases["Fase Preoperativa"] = st.selectbox("¿La Fase Preoperativa describe procedimientos previos?", opciones, key="fase_3")
    fases["Fase Operativa"] = st.selectbox("¿La Fase Operativa describe acciones concretas?", opciones, key="fase_4")
    fases["Fase Postoperativa"] = st.selectbox("¿La Fase Postoperativa describe procedimientos posteriores?", opciones, key="fase_5")

    st.subheader("🔹 Seguimiento: Matrices, Actividades, Indicadores y Metas")
    seguimiento = {}
    seguimiento["Se revisó y ajustó las actividades estratégicas de líneas de acción."] = st.selectbox(
        "¿Se revisó y ajustó las actividades estratégicas de líneas de acción?", opciones, key="seguimiento_1")
    seguimiento["Se revisó y ajustó los indicadores de las líneas de acción."] = st.selectbox(
        "¿Se revisaron y ajustaron los indicadores de las líneas de acción?", opciones, key="seguimiento_2")
    seguimiento["Se revisó y actualizó la meta planteada para la ejecución del año 2025."] = st.selectbox(
        "¿Se revisó y actualizó la meta para el año 2025?", opciones, key="seguimiento_3")
    seguimiento["Se revisó y actualizó la meta bianual."] = st.selectbox(
        "¿Se revisó y actualizó la meta bianual?", opciones, key="seguimiento_4")
    seguimiento["Se actualizaron las metas en el Informe Trimestral de avance de líneas de acción."] = st.selectbox(
        "¿Se actualizaron las metas en el Informe Trimestral de avance?", opciones, key="seguimiento_5")

    st.subheader("🔹 Conclusión Final")
    conclusion = st.text_area("Conclusión Final")

    enviar = st.form_submit_button("📤 Generar Informe PDF")


