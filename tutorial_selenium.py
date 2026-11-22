from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    driver.get('https://es.finance.yahoo.com/')

    # 1. Cookies
    wait.until(EC.element_to_be_clickable((By.ID, 'didomi-notice-agree-button'))).click()

    # 2. Entrar en el ticker MU
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/quote/MU/"]'))).click()

    # 2.1 Elementos dinámicos (menú lateral)
    wait.until(EC.element_to_be_clickable((By.ID, '_yb_sidenav-btn'))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-rapid_p="13"]'))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-rapid_p="21"]'))).click()

    # 3. Buscar AAPL
    caja = wait.until(EC.element_to_be_clickable((By.ID, 'ybar-sbq')))
    caja.clear()
    caja.send_keys('AAPL', Keys.ENTER)

    # Leer el precio varias veces (se vuelve a buscar el elemento cada vez
    # porque Yahoo lo actualiza en vivo y la referencia puede quedar obsoleta)
    for i in range(10):
        elemento = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'fin-streamer[data-testid="qsp-price"]')
        ))
        print(f"Lectura {i + 1}: {elemento.get_attribute('data-value')}")
        sleep(1)

    # 4. Varios elementos a la vez
    etiquetas = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, 'span.label')
    ))
    valores = driver.find_elements(By.CSS_SELECTOR, 'span.value')

    for i, (etiqueta, valor) in enumerate(zip(etiquetas, valores)):
        print(f"{i}: {etiqueta.text}: {valor.text}")

finally:
    input("Pulsa Enter para cerrar...")
    driver.quit()