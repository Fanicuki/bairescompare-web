from bs4 import BeautifulSoup
import requests

def disco_product_info(url):
    # Realizamos la solicitud a la página web
    resultado = requests.get(url)
    content = resultado.text

    # Parseamos el contenido HTML de la página con BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Buscamos el nombre del producto usando la clase correcta
    name_tag = soup.find('span', class_='vtex-store-components-3-x-productBrand')

    # Buscamos el precio del producto usando la clase correcta
    price_tag = soup.find('div', class_='priceContainer')

    # Extraemos y mostramos el texto dentro de esas clases
    if price_tag and name_tag:
        return {
            "name": name_tag.get_text(strip=True),
            "price": price_tag.get_text(strip=True)
        }
    else:
        return None

# URLs de los productos de Disco
urls = [
    "https://www.disco.com.ar/galletitas-oreo-rellenas-con-crema-sabor-original-118g-menos-sodio/p",
    "https://www.disco.com.ar/galletitas-traviata-x540g/p"
]

# Iteramos sobre las URLs y mostramos la información de cada producto
for url in urls:
    product_info = disco_product_info(url)
    if product_info:
        print(f"Producto: {product_info['name']} - Precio: {product_info['price']}")
    else:
        print(f"No se encontró información para la URL: {url}")
