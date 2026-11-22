from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL_BASE = "https://books.toscrape.com/"
ESTRELLAS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def leer_libros_de_pagina(wait):
    libros = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.product_pod"))
    )
    resultado = []
    for libro in libros:
        clase = libro.find_element(By.CSS_SELECTOR, "p.star-rating").get_attribute("class")
        resultado.append({
            "titulo": libro.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title"),
            "precio": float(libro.find_element(By.CSS_SELECTOR, "p.price_color").text.replace("£", "")),
            "estrellas": ESTRELLAS[clase.replace("star-rating", "").strip()],
            "stock": libro.find_element(By.CSS_SELECTOR, "p.availability").text.strip(),
        })
    return resultado


def entrar_en_categoria(driver, wait, nombre):
    enlace = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, nombre)))
    enlace.click()
    titulo = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.page-header h1")))
    print(f"Categoría abierta: {titulo.text}")


def leer_todas_las_paginas(driver, wait):
    acumulado = []
    while True:
        acumulado.extend(leer_libros_de_pagina(wait))
        siguiente = driver.find_elements(By.CSS_SELECTOR, "li.next a")
        if not siguiente:
            break
        siguiente[0].click()
    return acumulado


def obtener_nombres_categorias(driver, wait):
    enlaces = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.side_categories ul li ul li a")
        )
    )
    return [el.text.strip() for el in enlaces if el.text.strip()]


driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

conteo_por_categoria = {}

try:
    driver.get(URL_BASE)
    entrar_en_categoria(driver, wait, "Mystery")
    libros_mystery = leer_libros_de_pagina(wait)

    print("\n--- Libros en Mystery (página actual) ---")
    for libro in libros_mystery:
        print(f"- {libro['titulo']} | £{libro['precio']} | {libro['estrellas']}★ | {libro['stock']}")

    driver.get(URL_BASE)
    entrar_en_categoria(driver, wait, "Fiction")
    libros_fiction = leer_todas_las_paginas(driver, wait)
    print(f"\nTotal de libros en Fiction (todas las páginas): {len(libros_fiction)}")

    driver.get(URL_BASE)
    categorias = obtener_nombres_categorias(driver, wait)

    for nombre_cat in categorias:
        driver.get(URL_BASE)
        entrar_en_categoria(driver, wait, nombre_cat)
        libros_cat = leer_todas_las_paginas(driver, wait)
        conteo_por_categoria[nombre_cat] = len(libros_cat)

finally:
    driver.quit()

print("\n--- Cantidad de libros por categoría ---")
for categoria, cantidad in conteo_por_categoria.items():
    print(f"{categoria}: {cantidad}")

print(f"\nTotal de categorías recorridas: {len(conteo_por_categoria)}")
print(f"Suma total de libros: {sum(conteo_por_categoria.values())}")