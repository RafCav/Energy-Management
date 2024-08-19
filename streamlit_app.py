import streamlit as st
from datetime import datetime
import pandas as pd
import pytz
import matplotlib.pyplot as plt


def get_data():
    sheet_id = '14ZRdMa16p6LR9BKdDGXYXYGYOqe5auFOKEUS1J4U40Y'
    gid = '640773164'

    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}")

    df['date'] = pd.to_datetime(df['date'])
    df['value_per_kwh'] = df['value_per_kwh'].str.replace(',', '.').astype(float)
    df['value'] = df['value'].str.replace(',', '.').astype(float)

    return df


st.title('Projeção da Conta de Energia')

with st.form(key='projection_form'):
    kwh_current = st.number_input('Digite o kWh consumido:', format='%d', step=1)
    submit_button = st.form_submit_button(label='Enviar')

    if submit_button:
        df = get_data()

        # Date Variables
        today = datetime.now(pytz.timezone('America/Sao_Paulo')).date()  # Just today :p
        date_next_billing = (df['date'].max()).date()  # Next billing date
        date_last_billing = df['date'].iloc[len(df) - 2].date()  # Last billing date
        days_next_billing = (date_next_billing - date_last_billing).days  # Days between today and next billing date
        days_last_billing = (today - date_last_billing).days  # Days between last billing date and today

        # Math Variables
        avg_value_per_kwh = df['value_per_kwh'].mean()  # Average billing cost per kWh
        last_kwh = df['kWh'].max()  # Last kWh registered
        kwh_consumed = int(kwh_current) - last_kwh  # Difference between last and current kWh

        # Projection Variables
        kwh_projection = (days_next_billing * kwh_consumed) / days_last_billing
        value_projection = kwh_projection * avg_value_per_kwh

        # Fill the black space with the projection
        df['value'] = df['value'].fillna(value_projection)

        st.write(f'Valor da Conta Projetado: R$ {round(value_projection, 2)}')
        st.write(f'Consumo Projetado: {kwh_projection} kWh')

        # DataFrame cut
        df_copied = df.tail(6)

        # Plot
        fig, ax = plt.subplots()
        ax.bar(df_copied['date'], df_copied['value'], width=15)
        ax.set_xlabel('Mês')
        ax.set_ylabel('R$')
        ax.set_title('Valor das Contas por Data')
        st.pyplot(fig)
