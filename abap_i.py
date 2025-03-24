# -*- coding: utf-8 -*-
"""ABAP-F.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NBmNSNM5_4DQe-6oFaiK8zMQcqCVAMgh
"""

import streamlit as st
import pandas as pd

# Datos iniciales
if 'catalogo_cuentas' not in st.session_state:
    st.session_state['catalogo_cuentas'] = pd.DataFrame(columns=['Código', 'Nombre', 'Tipo'])

if 'polizas' not in st.session_state:
    st.session_state['polizas'] = pd.DataFrame(columns=['Folio', 'Fecha', 'Concepto', 'Cuenta', 'Debe', 'Haber'])

# Módulo de Cuentas
st.title("Catálogo de Cuentas")

# Formulario para agregar cuenta
with st.form("Alta de Cuenta"):
    codigo = st.text_input("Código")
    nombre = st.text_input("Nombre")
    tipo = st.selectbox("Tipo", ["Activo", "Pasivo", "Capital", "Ingresos", "Gastos"])
    submit_cuenta = st.form_submit_button("Agregar Cuenta")

    if submit_cuenta:
        nueva_cuenta = pd.DataFrame([[codigo, nombre, tipo]], columns=['Código', 'Nombre', 'Tipo'])
        st.session_state['catalogo_cuentas'] = pd.concat([st.session_state['catalogo_cuentas'], nueva_cuenta], ignore_index=True)
        st.success("Cuenta agregada correctamente")

st.write("### Cuentas Registradas")
st.dataframe(st.session_state['catalogo_cuentas'])

# Módulo de Pólizas
st.title("Módulo de Pólizas")

# Formulario para agregar póliza
with st.form("Alta de Póliza"):
    folio = st.text_input("Folio")
    fecha = st.date_input("Fecha")
    concepto = st.text_input("Concepto")
    cuenta = st.selectbox("Cuenta", st.session_state['catalogo_cuentas']['Código'].tolist() if not st.session_state['catalogo_cuentas'].empty else ["No hay cuentas registradas"])
    debe = st.number_input("Debe", min_value=0.0, format="%.2f")
    haber = st.number_input("Haber", min_value=0.0, format="%.2f")
    submit = st.form_submit_button("Agregar Póliza")

    if submit:
        if cuenta != "No hay cuentas registradas":
            nueva_poliza = pd.DataFrame([[folio, fecha, concepto, cuenta, debe, haber]],
                                        columns=['Folio', 'Fecha', 'Concepto', 'Cuenta', 'Debe', 'Haber'])
            st.session_state['polizas'] = pd.concat([st.session_state['polizas'], nueva_poliza], ignore_index=True)
            st.success("Póliza registrada correctamente")
        else:
            st.warning("No se puede registrar una póliza sin cuentas disponibles.")

# Mostrar pólizas registradas
st.write("### Pólizas Registradas")
st.dataframe(st.session_state['polizas'])

# Eliminar póliza específica
folio_eliminar = st.text_input("Ingrese el folio de la póliza a eliminar")
if st.button("Eliminar Póliza"):
    if folio_eliminar in st.session_state['polizas']['Folio'].values:
        st.session_state['polizas'] = st.session_state['polizas'][st.session_state['polizas']['Folio'] != folio_eliminar]
        st.success(f"Póliza con folio {folio_eliminar} eliminada correctamente.")
    else:
        st.warning("Folio no encontrado en las pólizas registradas.")