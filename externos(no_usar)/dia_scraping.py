from bs4 import BeautifulSoup
import requests

def scrape_product_info(url):
    # Realizamos la solicitud a la página web
    resultado = requests.get(url)
    content = resultado.text

    # Parseamos el contenido HTML de la página con BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Buscamos el precio del producto usando la clase correcta
    price_tag = soup.find('span', class_='vtex-product-price-1-x-sellingPriceValue')

    # Buscamos el nombre del producto usando la clase correcta
    name_tag = soup.find('span', class_='vtex-store-components-3-x-productBrand vtex-store-components-3-x-productBrand--productNamePdp')

    # Extraemos y mostramos el texto dentro de esas clases
    if price_tag and name_tag:
        return {
            "name": name_tag.get_text(strip=True),
            "price": price_tag.get_text(strip=True)
        }
    else:
        return None

# URLs de los productos
urls = [
    "https://diaonline.supermercadosdia.com.ar/arroz-largo-fino-ala-1kg-25417/p",
    "https://diaonline.supermercadosdia.com.ar/arvejas-secas-remojadas-dia-300-gr-279121/p",
    "https://diaonline.supermercadosdia.com.ar/tomate-perita-cubeteado-dia-con-agregado-de-pure-de-tomate-400-gr-119003/p",
    "https://diaonline.supermercadosdia.com.ar/mayonesa-de-ajo-hellmans-250-gr-291831/p",
    "https://diaonline.supermercadosdia.com.ar/almidon-de-maiz-maizena-500-gr-295455/p",
    "https://diaonline.supermercadosdia.com.ar/mostaza-savora-500-gr-278069/p",
    "https://diaonline.supermercadosdia.com.ar/mayonesa-sabor-ahumado-hellmans-250-gr-291832/p"
]

# Iteramos sobre las URLs y mostramos la información de cada producto
for url in urls:
    product_info = scrape_product_info(url)
    if product_info:
        print(f"Producto: {product_info['name']} - Precio: {product_info['price']}")
    else:
        print(f"No se encontró información para la URL: {url}")
