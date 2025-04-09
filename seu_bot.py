import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurações do navegador headless
opcoes = Options()
# opcoes.add_argument("--headless")  # Ative para rodar em segundo plano
opcoes.add_argument("--disable-gpu")
opcoes.add_argument("--log-level=3")  # Menos logs do Chrome

driver = webdriver.Chrome(options=opcoes)
driver.get("https://casino.betfair.com/pt-br/c/roleta")

# Espera os números aparecerem
WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'number'))
)

# Arquivo CSV para armazenar os dados
arquivo_csv = "resultados_roleta.csv"

# Cria o arquivo e cabeçalho, se necessário
try:
    with open(arquivo_csv, 'x', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'números'])
except FileExistsError:
    pass

ultimo_resultado = []

print("Bot iniciado. Coletando números da roleta...")

while True:
    try:
        elementos = driver.find_elements(By.CLASS_NAME, 'number')
        lista = []

        for elem in elementos[:8]:  # Pega apenas os últimos 8
            texto = elem.text.strip()
            if texto.isdigit():
                lista.append(texto)

        if lista and lista != ultimo_resultado:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Números: {lista}")

            with open(arquivo_csv, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, ', '.join(lista)])

            ultimo_resultado = lista

        time.sleep(5)

    except Exception as e:
        print(f"[ERRO] {time.strftime('%H:%M:%S')} - {e}")
        time.sleep(10)
        continue
