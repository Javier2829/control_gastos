import json
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st



def get_firebase():
    if not firebase_admin._apps:
        try:
            firebase_secrets= dict(st.secrets['connections_firebase'])
            cred=credentials.Certificate(firebase_secrets)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f'Error al inicializar Firebase{e}')
            st.stop()
    return firestore.client()

# Obtener datos desde Firebase
def cargar_transacciones():
    db = get_firebase()
    transacciones_ref = db.collection('transacciones')
    docs = transacciones_ref.stream()

    data = []
    for doc in docs:
        transaccion = doc.to_dict()
        transaccion['id'] = doc.id  # opcional: incluir ID
        data.append(transaccion)

    df = pd.DataFrame(data)

    # Conversión segura de fecha si existe la columna
    if 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

    return df