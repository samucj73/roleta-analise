import time

driver = opcoes.Chrome()
driver.get("https://casino.betfair.com/pt-br/c/roleta")

time.sleep(3)

while True:
    lista = []

    for x in range(8):
        elem = driver.find_elements(By.CLASS_NAME, 'number')
        elem2 = elem[x].text
        lista.append(elem2)

    print(lista)
    time.sleep(5)
