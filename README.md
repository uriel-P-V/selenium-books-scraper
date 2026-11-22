# Scraper de libros con Selenium

Proyecto de aprendizaje de Selenium usando [books.toscrape.com](https://books.toscrape.com),
un sitio creado específicamente para practicar scraping.

## Qué hace
- Lee título, precio, valoración y stock de los libros.
- Recorre la paginación de todo el catálogo (1000 libros).
- Navega por las 50 categorías y cuenta los libros de cada una.

## Requisitos
- Python 3.8+
- Google Chrome instalado

## Instalación
    pip install -r requirements.txt

## Uso
    python scraper_libros.py

## Conceptos practicados
- Localizadores (CSS, LINK_TEXT)
- Esperas explícitas (`WebDriverWait`)
- Búsqueda dentro de elementos
- Paginación
- Manejo de elementos obsoletos (stale)

## Hoja de ruta
- [x] Fase 1: extraer libros de una página
- [x] Fase 2: paginación
- [x] Fase 3: categorías
- [ ] Fase 4: páginas de detalle
- [ ] Fase 5: exportar a CSV y modo headless
- [ ] Fase 6: refactor y manejo de errores
- [ ] Fase 7: elementos dinámicos (quotes.toscrape.com)