import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import statistics
import time
import os

# Configurações da página
st.set_page_config(page_title="Dashboard Roleta", layout="wide", initial_sidebar_state="expanded")
st.title("Painel de Análise - Roleta Betfair")

# ============================
# Funções auxiliares
# ============================
def ler_dados():
    try:
        df = pd.read_csv("resultados_roleta.csv")
        todos_numeros = []
        for linha in df['números']:
            nums = linha.split(', ')
            todos_numeros.extend([int(n) for n in nums if n.isdigit()])
        return todos_numeros, df
    except Exception:
        return [], pd.DataFrame()

def prever_proximo_markov(numeros):
    transicoes = {}
    for i in range(len(numeros)-1):
        atual = numeros[i]
        prox = numeros[i+1]
        if atual not in transicoes:
            transicoes[atual] = []
        transicoes[atual].append(prox)
    
    if numeros:
        ultimo = numeros[-1]
        if ultimo in transicoes:
            candidatos = Counter(transicoes[ultimo])
            return candidatos.most_common(3)
    return []

def linha_coluna(numero):
    if numero == 0:
        return "0", "0"
    linha = {1: "1ª", 2: "2ª", 3: "3ª"}[(numero - 1) % 3 + 1]
    if 1 <= numero <= 12:
        coluna = "1ª (1-12)"
    elif 13 <= numero <= 24:
        coluna = "2ª (13-24)"
    else:
        coluna = "3ª (25-36)"
    return linha, coluna

def salvar_previsoes(previsoes):
    nome_arquivo = "historico_previsoes.csv"
    with open(nome_arquivo, 'a') as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        linha = f"{timestamp}," + ",".join(str(p[0]) for p in previsoes) + "\n"
        f.write(linha)

# ============================
# Leitura de dados
# ============================
numeros, df = ler_dados()

if not numeros:
    st.warning("Nenhum dado encontrado ainda.")
    st.stop()

# ============================
# Estatísticas Básicas
# ============================
st.subheader("Estatísticas")
col1, col2 = st.columns(2)

with col1:
    st.metric("Total de Números", len(numeros))
    st.metric("Média", f"{statistics.mean(numeros):.2f}")
    st.metric("Mediana", statistics.median(numeros))
    st.metric("Moda", statistics.mode(numeros))
    st.metric("Desvio Padrão", f"{statistics.stdev(numeros):.2f}")

    pares = len([n for n in numeros if n % 2 == 0])
    impares = len([n for n in numeros if n % 2 != 0])
    st.write(f"Pares: **{pares}** | Ímpares: **{impares}**")

with col2:
    contador = Counter(numeros)
    fig, ax = plt.subplots()
    ax.bar(contador.keys(), contador.values(), color='orange')
    ax.set_xlabel("Número")
    ax.set_ylabel("Ocorrências")
    ax.set_title("Frequência dos Números")
    st.pyplot(fig)

# ============================
# Previsão com IA Markov
# ============================
st.subheader("Previsão de Próximos Números (IA - Markov)")

previsoes = prever_proximo_markov(numeros)
if previsoes:
    salvar_previsoes(previsoes)
    for num, freq in previsoes:
        linha, coluna = linha_coluna(num)
        st.write(f"**{num}** (linha {linha}, coluna {coluna}) - tendência: {freq}")
else:
    st.info("Ainda não há dados suficientes para prever.")

# ============================
# Linha e Coluna
# ============================
st.subheader("Distribuição por Linha e Coluna")

linhas = {"1ª": 0, "2ª": 0, "3ª": 0, "0": 0}
colunas = {"1ª (1-12)": 0, "2ª (13-24)": 0, "3ª (25-36)": 0, "0": 0}

for n in numeros:
    linha, coluna = linha_coluna(n)
    linhas[linha] += 1
    colunas[coluna] += 1

col3, col4 = st.columns(2)

with col3:
    st.write("**Frequência por Linha:**")
    st.bar_chart(pd.Series(linhas))

with col4:
    st.write("**Frequência por Coluna:**")
    st.bar_chart(pd.Series(colunas))

# ============================
# Histórico de previsões
# ============================
st.subheader("Histórico de Previsões")

if os.path.exists("historico_previsoes.csv"):
    df_hist = pd.read_csv("historico_previsoes.csv", header=None, names=["Timestamp", "N1", "N2", "N3"])
    st.dataframe(df_hist.tail(10), use_container_width=True)
else:
    st.info("Nenhuma previsão registrada ainda.")

# ============================
# Últimos registros
# ============================
st.subheader("Últimos Resultados Coletados")
st.dataframe(df.tail(10), use_container_width=True)
