# Painel de Análise da Roleta - Betfair

Este projeto coleta, analisa e prevê números da roleta usando Python, IA leve e Streamlit.

## Funcionalidades
- Leitura automática do arquivo `resultados_roleta.csv`
- Análises estatísticas (frequência, média, moda, etc.)
- Previsão com modelo de transição de estados (Markov)
- Análise por linha e coluna da roleta
- Histórico das previsões feitas
- Pronto para rodar via GitHub e Streamlit Cloud

## Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run dashboard_roleta.py
