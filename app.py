from flask import Flask, request, jsonify, send_from_directory
from bs4 import BeautifulSoup
import requests

app = Flask(__name__, static_folder='')

def scrape_carrefour_product_info(query):
    products = []
    urls = [
        "https://www.carrefour.com.ar/pure-de-tomate-carrefour-classic-520-g/p",
        "https://www.carrefour.com.ar/lomitos-de-atun-carrefour-al-natural-170-g/p",
        "https://www.carrefour.com.ar/leche-entera-uat-carrefour-classic-tetra-1-lt-721388/p"
    ]
    for url in urls:
        try:
            result = requests.get(url)
            soup = BeautifulSoup(result.text, 'html.parser')
            name_tag = soup.find('span', class_='vtex-store-components-3-x-productBrand vtex-store-components-3-x-productBrand--quickview')
            price_tag = soup.find('span', class_='valtech-carrefourar-product-price-0-x-currencyContainer')
            image_tag = soup.find('img', class_='vtex-store-components-3-x-productImageTag vtex-store-components-3-x-productImageTag--product-view-images-selector vtex-store-components-3-x-productImageTag--main vtex-store-components-3-x-productImageTag--product-view-images-selector--main')
            if name_tag and price_tag and image_tag:
                name = name_tag.get_text(strip=True).lower()
                price = price_tag.get_text(strip=True).replace('$', '').replace(',', '.')
                image_url = image_tag['src']
                if query in name:
                    products.append({"name": name, "price": float(price), "store": "Carrefour", "url": url, "image": image_url})
        except Exception as e:
            print(f"Error scraping Carrefour URL {url}: {e}")
    return products

def scrape_dia_product_info(query):
    products = []
    urls = [
        "https://diaonline.supermercadosdia.com.ar/arroz-largo-fino-ala-1kg-25417/p",
        "https://diaonline.supermercadosdia.com.ar/arvejas-secas-remojadas-dia-300-gr-279121/p",
        "https://diaonline.supermercadosdia.com.ar/tomate-perita-cubeteado-dia-con-agregado-de-pure-de-tomate-400-gr-119003/p",
        "https://diaonline.supermercadosdia.com.ar/mayonesa-de-ajo-hellmans-250-gr-291831/p",
        "https://diaonline.supermercadosdia.com.ar/almidon-de-maiz-maizena-500-gr-295455/p",
        "https://diaonline.supermercadosdia.com.ar/mostaza-savora-500-gr-278069/p",
        "https://diaonline.supermercadosdia.com.ar/mayonesa-sabor-ahumado-hellmans-250-gr-291832/p",
        "https://diaonline.supermercadosdia.com.ar/leche-larga-vida-clasica-la-serenisma-200-ml-1695/p"
    ]
    for url in urls:
        try:
            result = requests.get(url)
            soup = BeautifulSoup(result.text, 'html.parser')
            name_tag = soup.find('span', class_='vtex-store-components-3-x-productBrand vtex-store-components-3-x-productBrand--productNamePdp')
            price_tag = soup.find('span', class_='vtex-product-price-1-x-sellingPriceValue')
            image_tag = soup.find('img', class_='vtex-store-components-3-x-productImageTag vtex-store-components-3-x-productImageTag--main')
            if name_tag and price_tag and image_tag:
                name = name_tag.get_text(strip=True).lower()
                price = price_tag.get_text(strip=True).replace('$', '').replace(',', '.')
                image_url = image_tag['src']
                if query in name:
                    products.append({"name": name, "price": float(price), "store": "Día", "url": url, "image": image_url})
        except Exception as e:
            print(f"Error scraping Día URL {url}: {e}")
    return products

@app.route('/')
def home():
    return send_from_directory('', 'index.html')

@app.route('/search')
def search():
    query = request.args.get('query').lower()
    try:
        carrefour_products = scrape_carrefour_product_info(query)
        dia_products = scrape_dia_product_info(query)
        all_products = carrefour_products + dia_products
        all_products.sort(key=lambda x: x['price'])
        
        # Añadir depuración aquí
        print(f"Query: {query}")
        print(f"Carrefour Products: {carrefour_products}")
        print(f"Día Products: {dia_products}")
        print(f"All Products: {all_products}")

        return jsonify(all_products)
    except Exception as e:
        print(f"Error in search endpoint: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
