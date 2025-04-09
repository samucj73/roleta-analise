import streamlit as st
import pandas as pd
import os
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from lstm_model import treinar_e_prever

st.set_page_config(page_title="Painel Roleta Web", layout="wide")

st.title("Análise da Roleta (Painel Web)")

# Análise de dados
if os.path.exists("resultados_roleta.csv"):
    df = pd.read_csv("resultados_roleta.csv")
    df.dropna(inplace=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["números"] = df["números"].apply(lambda x: list(map(int, x.split(", "))))
    numeros_flat = [num for sublist in df["números"] for num in sublist]

    st.subheader("Estatísticas básicas")
    st.write(f"Total de registros: {len(df)}")
    st.write(f"Números coletados: {len(numeros_flat)}")

    col1, col2 = st.columns(2)
    with col1:
        st.write("Número mais frequente:")
        st.write(pd.Series(numeros_flat).mode().values)

    with col2:
        st.write("Frequência dos números:")
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.histplot(numeros_flat, bins=37, ax=ax, discrete=True)
        st.pyplot(fig)

    st.subheader("Previsão IA (LSTM)")
    with st.spinner("Treinando modelo e prevendo..."):
        previsoes = treinar_e_prever(numeros_flat)
        st.success("Previsão concluída!")
        st.write("Próximos números estimados:")
        st.write(", ".join(map(str, previsoes)))
else:
    st.warning("Arquivo 'resultados_roleta.csv' não encontrado. O bot deve ser executado localmente.")
