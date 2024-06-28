import requests
from bs4 import BeautifulSoup

def scrape_carrefour_product_info(query):
    # Aquí va tu código para hacer scraping en Carrefour
    # Este es un ejemplo simple
    products = []
    urls = [
        "https://www.carrefour.com.ar/pure-de-tomate-carrefour-classic-520-g/p",
        "https://www.carrefour.com.ar/lomitos-de-atun-carrefour-al-natural-170-g/p"
    ]
    for url in urls:
        result = requests.get(url)
        soup = BeautifulSoup(result.text, 'html.parser')
        name_tag = soup.find('span', class_='vtex-store-components-3-x-productBrand vtex-store-components-3-x-productBrand--quickview')
        price_tag = soup.find('span', class_='valtech-carrefourar-product-price-0-x-currencyContainer')
        if name_tag and price_tag:
            name = name_tag.get_text(strip=True).lower()
            if query in name:
                price = price_tag.get_text(strip=True).replace('$', '')
                products.append({"name": name, "price": price, "store": "Carrefour"})
    return products
