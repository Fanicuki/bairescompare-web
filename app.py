from flask import Flask, request, jsonify, send_from_directory
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import time
from flask_cors import CORS

app = Flask(__name__, static_folder='')
CORS(app)  # Enable CORS for all routes

# Cache simple en memoria
cache = {}

def fetch_url(url):
    if url in cache:
        return cache[url]
    result = requests.get(url)
    cache[url] = result
    return result

def load_urls():
    with open('urls.json') as f:
        return json.load(f)

urls = load_urls()

def scrape_carrefour_product_info(query):
    products = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls['carrefour']}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                soup = BeautifulSoup(result.text, 'html.parser')
                name_tag = soup.find('span', class_='vtex-store-components-3-x-productBrand vtex-store-components-3-x-productBrand--quickview')
                price_tag = soup.find('span', class_='valtech-carrefourar-product-price-0-x-currencyContainer')
                image_tag = soup.find('img', class_='vtex-store-components-3-x-productImageTag vtex-store-components-3-x-productImageTag--product-view-images-selector vtex-store-components-3-x-productImageTag--main vtex-store-components-3-x-productImageTag--product-view-images-selector--main')
                
                if name_tag and price_tag and image_tag:
                    name = name_tag.get_text(strip=True).lower() if name_tag else 'Producto sin nombre'
                    price = price_tag.get_text(strip=True).replace('$', '').replace('.', '').replace(',', '.')
                    image_url = image_tag['src'] if image_tag else 'URL de imagen no disponible'
                    if query in name:
                        try:
                            price = float(price)
                        except ValueError:
                            price = 0.0  # Si no se puede convertir a float, asignar 0.0
                        products.append({"name": name, "price": price, "store": "Carrefour", "url": url, "image": image_url})
            except Exception as e:
                print(f"Error scraping Carrefour URL {url}: {e}")
    return products

def scrape_dia_product_info(query):
    products = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls['dia']}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                soup = BeautifulSoup(result.text, 'html.parser')
                name_tag = soup.find('span', class_='vtex-store-components-3-x-productBrand vtex-store-components-3-x-productBrand--productNamePdp')
                price_tag = soup.find('span', class_='vtex-product-price-1-x-sellingPriceValue')
                image_tag = soup.find('img', class_='vtex-store-components-3-x-productImageTag vtex-store-components-3-x-productImageTag--main')
                
                if name_tag and price_tag and image_tag:
                    name = name_tag.get_text(strip=True).lower() if name_tag else 'Producto sin nombre'
                    price = price_tag.get_text(strip=True).replace('$', '').replace('.', '').replace(',', '.')
                    image_url = image_tag['src'] if image_tag else 'URL de imagen no disponible'
                    if query in name:
                        try:
                            price = float(price)
                        except ValueError:
                            price = 0.0  # Si no se puede convertir a float, asignar 0.0
                        products.append({"name": name, "price": price, "store": "Día", "url": url, "image": image_url})
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
        start_time = time.time()
        carrefour_products = scrape_carrefour_product_info(query)
        dia_products = scrape_dia_product_info(query)
        all_products = carrefour_products + dia_products
        all_products.sort(key=lambda x: x['price'])
        
        # Debugging
        print(f"Query: {query}")
        print(f"Carrefour Products: {carrefour_products}")
        print(f"Día Products: {dia_products}")
        print(f"All Products: {all_products}")
        print(f"Total search time: {time.time() - start_time} seconds")

        return jsonify(all_products)
    except Exception as e:
        print(f"Error in search endpoint: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
