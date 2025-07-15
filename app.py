import datetime
import plotly.express as px
import streamlit as st
import pandas as pd
import os


def main():
    # crear archivo csv
    # CSV_FILE = 'finanzas personales'
    # if os.path.exists(CSV_FILE):
    #     st.session_state.datos = pd.read_csv(CSV_FILE, parse_dates='fecha')
    # else:
    #     st.session_state.datos = pd.DataFrame(columns=['tipo', 'fecha', 'monto', 'categoria', 'descripcion'])
    # crear memoria de datos
    if 'datos' not in st.session_state:
        st.session_state.datos = pd.DataFrame(columns=['tipo', 'fecha', 'monto', 'categoria', 'descripcion'])
    st.header(":material/currency_exchange: Control de ingresos y gastos personales")
    # opciones del menu
    opMenu = ['Home', 'Registrar transacción', 'Ver historial', 'Resumen']
    # opciones de la categoria
    catRegistro = ['Sueldo', 'Boleta honorario', 'Otros Ingresos', 'Combustible', 'Supermercado', 'Deporte', 'Viajes',
                   'Crédito Consumo', 'Crédito Hipotecário', 'Linea de Crédito', 'Tarjeta', 'Luz', 'Agua', 'internet',
                   'Telefonía', 'Televisión']

    # menú del siderbar
    menu = st.sidebar.selectbox('Menu', opMenu)
    # ------------------------------------registro -------------------------------------------
    if menu == 'Registrar transacción':
        st.subheader('Registro de transacción')
        with (st.form(key='registro', clear_on_submit=True)):
            tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"], index=None, placeholder='Selecione una opción')

            fecha = st.date_input(label='Fecha', value="today", max_value='today')
            monto = st.number_input('Monto', min_value=0, value=0, step=1)
            categoria = st.selectbox('Categoria', catRegistro, index=None, placeholder='Elija una categoria')
            descripcion = st.text_area('Descripción u observación', placeholder='Detalle de la transacción')
            registrar = st.form_submit_button('Registrar', icon=':material/save:', type="primary")
            # guardar= st.button('Guardar', type='primary')

            if registrar:
                nuevaTransaccion = pd.DataFrame([{
                    "tipo": tipo,
                    "fecha": fecha,
                    "monto": monto,
                    "categoria": categoria,
                    "descripcion": descripcion
                }])
                st.session_state.datos = pd.concat([st.session_state.datos, nuevaTransaccion], ignore_index=True)

            # st.session_state.datos.to_csv(CSV_FILE, index=False)
            # st.info('datos guardados')

    # ----------------------------------historial-----------------------------------
    elif menu == 'Ver historial':
        st.subheader(":material/history: Historial de Transacciones")
        df = st.session_state.datos

        #     Filtros de los datos
        tipo_filtro = st.multiselect('Filtrar por tipo', ['Gasto', 'Ingreso'], default=["Ingreso", "Gasto"])
        fecha_inicio = st.date_input('Desde', datetime.date(2025, 1, 1))

        fecha_final = st.date_input('Hasta ', datetime.date.today())
        # convertir fechas a timestamp
        fecha_inicio = pd.Timestamp(fecha_inicio)
        fecha_final = pd.Timestamp(fecha_final)
        # asegura que la columna sea de tipo datetime
        df['fecha'] = pd.to_datetime(df['fecha'])
        # crea el dataframe filtrado
        df_filtrado = df[
            (df['tipo'].isin(tipo_filtro)) &
            (df['fecha'] >= fecha_inicio) &
            (df['fecha'] <= fecha_final)
            ]

        st.dataframe(df_filtrado)
        if not df_filtrado.empty:
            csv = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label='Descargar',
                data=csv,
                file_name='finanzas personales.csv',
                mime='text/csv')


    elif menu == 'Resumen':
        st.subheader(':material/analytics: Resumen financiero ')
        df = st.session_state.datos

        if df.empty:
            st.info('No hay datos para mostrar')
        else:
            ingresos = df[df['tipo'] == 'Ingreso']['monto'].sum()

        gastos = df[df['tipo'] == 'Gasto']['monto'].sum()
        balance = ingresos - gastos
        # tabla comparativa de gastos e ingresos
        col1, col2, col3 = st.columns(3)
        col1.metric('Total de ingresos', f'${ingresos}')
        col2.metric('Total de gastos ', f'${gastos}')
        col3.metric('Balance', f'${balance}')




        # graficos

        # Gráfico por categoría
        grafico_df = df.groupby(["categoria", "tipo"])["monto"].sum().reset_index()
        fig = px.bar(grafico_df, x="categoria", y="monto", color="tipo", barmode="group")
        st.plotly_chart(fig)


if __name__ == '__main__':
    main()
