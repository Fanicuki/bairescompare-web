from flask import Flask, request, jsonify, send_from_directory
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

app = Flask(__name__, static_folder='')

# Cache simple en memoria
cache = {}

def fetch_url(url):
    if url in cache:
        return cache[url]
    result = requests.get(url)
    cache[url] = result
    return result

def scrape_carrefour_product_info(query):
    products = []
    urls = [
        "https://www.carrefour.com.ar/pure-de-tomate-carrefour-classic-520-g/p",
        "https://www.carrefour.com.ar/lomitos-de-atun-carrefour-al-natural-170-g/p",
        "https://www.carrefour.com.ar/leche-entera-uat-carrefour-classic-tetra-1-lt-721388/p",
        "https://www.carrefour.com.ar/pan-de-mesa-bimbo-tipo-artesano-500-g-715676/p",
        "https://www.carrefour.com.ar/galletitas-crackers-la-providencia-303-g/p",
        "https://www.carrefour.com.ar/galletitas-pepitos-con-chips-de-chocolate-x3-119-g-715954/p",
        "https://www.carrefour.com.ar/arroz-largo-fino-crucero-00000-1-kg-719197/p",
        "https://www.carrefour.com.ar/harina-de-trigo-000-caserita-x-1-kg-7757/p",
        "https://www.carrefour.com.ar/harina-integral-pureza-1-kg/p",
        "https://www.carrefour.com.ar/fideos-monos-matarazzo-500-g/p",
        "https://www.carrefour.com.ar/papa-x-kg-9278/p",
        "https://www.carrefour.com.ar/batata-naranja-huella-natural-x-kg/p",
        "https://www.carrefour.com.ar/azucar-ledesma-molida-superior-bolsa-1-kg/p",
        "https://www.carrefour.com.ar/mermelada-bc-la-campagnola-frutilla-390-g/p",
        "https://www.carrefour.com.ar/lentejas-secas-remojadas-carrefour-340-g/p",
        "https://www.carrefour.com.ar/tomate-perita-arcor-400-g/p",
        "https://www.carrefour.com.ar/manzana-red-x-kg-432782/p",
        "https://www.carrefour.com.ar/tapa-de-asado-x-kg-57088/p",
        "https://www.carrefour.com.ar/fiambre-de-paleta-de-cerdo-centurion-706575/p",
        "https://www.carrefour.com.ar/huevos-blancos-carrefour-6-u/p",
        "https://www.carrefour.com.ar/leche-entera-larga-vida-la-serenisima-clasica-3-botella-1-l/p"
    ]

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
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
        "https://diaonline.supermercadosdia.com.ar/flautita-80-gr-278604/p",
        "https://diaonline.supermercadosdia.com.ar/galletitas-pepitos-con-chips-de-chocolate-357g-pack-x-3-ud-de-119-gr-271632/p",
        "https://diaonline.supermercadosdia.com.ar/galletitas-crackers-la-providencia-303-gr-299849/p",
        "https://diaonline.supermercadosdia.com.ar/arroz-largo-fino-ala-1kg-25417/p",
        "https://diaonline.supermercadosdia.com.ar/harina-leudante-fortificada-blancaflor-1-kg-300778/p",
        "https://diaonline.supermercadosdia.com.ar/almidon-de-maiz-maizena-500-gr-295455/p",
        "https://diaonline.supermercadosdia.com.ar/fideos-tallarin-n5-matarazzo-500-gr-42907/p",
        "https://diaonline.supermercadosdia.com.ar/papa-negra-x-1-kg-90094/p",
        "https://diaonline.supermercadosdia.com.ar/batata-x-1-kg-90062/p",
        "https://diaonline.supermercadosdia.com.ar/azucar-azucel-comun-tipo--a--500-gr-266204/p",
        "https://diaonline.supermercadosdia.com.ar/dulce-de-batata-emeth-500-gr-50789/p",
        "https://diaonline.supermercadosdia.com.ar/mermelada-de-frutilla-delicius-454-gr-287493/p",
        "https://diaonline.supermercadosdia.com.ar/dulce-de-leche-milkaut-400-gr-297589/p",
        "https://diaonline.supermercadosdia.com.ar/arvejas-secas-remojadas-dia-300-gr-279121/p",
        "https://diaonline.supermercadosdia.com.ar/lentejas-secas-remojadas-dia-300-gr-279126/p",
        "https://diaonline.supermercadosdia.com.ar/acelga-x-1-kg-90134/p",
        "https://diaonline.supermercadosdia.com.ar/cebolla-comercial-en-bolsa-malla-x-1-kg-90063/p",
        "https://diaonline.supermercadosdia.com.ar/lechuga-capuchina-x-1-kg-90079/p",
        "https://diaonline.supermercadosdia.com.ar/tomate-perita-pelado-dia-400-gr-34596/p",
        "https://diaonline.supermercadosdia.com.ar/tomate-perita-x-1-kg-90074/p",
        "https://diaonline.supermercadosdia.com.ar/zapallo-x-1-kg-94087/p",
        "https://diaonline.supermercadosdia.com.ar/zanahoria-x-1-kg-90122/p",
        "https://diaonline.supermercadosdia.com.ar/manzana-roja-comercial-en-bolsa-malla-x-1-kg-90111/p",
        "https://diaonline.supermercadosdia.com.ar/mandarina-x-1-kg-90119/p",
        "https://diaonline.supermercadosdia.com.ar/naranja-jugo-x-1-kg-90117/p",
        "https://diaonline.supermercadosdia.com.ar/banana-x-1-kg-90110/p",
        "https://diaonline.supermercadosdia.com.ar/pera-x-1-kg-90113/p",
        "https://diaonline.supermercadosdia.com.ar/tapa-de-asado-envasado-al-vacio-x-kg-279530/p",
        "https://diaonline.supermercadosdia.com.ar/hamburguesas-de-carne-clasicas-dia-x-12-uds-24138/p",
        "https://diaonline.supermercadosdia.com.ar/jamon-natural-fetas-finas-dia-120-gr-62654/p",
        "https://diaonline.supermercadosdia.com.ar/carne-picada-de-nalga-x-500-gr-225674/p",
        "https://diaonline.supermercadosdia.com.ar/tapa-de-nalga-envasado-al-vacio-x-kg-279531/p",
        "https://diaonline.supermercadosdia.com.ar/pollo-fresco-x-1-kg-90150/p",
        "https://diaonline.supermercadosdia.com.ar/filet-de-merluza-dia-500-gr-276010/p",
        "https://diaonline.supermercadosdia.com.ar/salame-feteado-lario-milan-150-gr-270906/p",
        "https://diaonline.supermercadosdia.com.ar/huevos-grandes-blancos-don-ramon-6-uds-54365/p",
        "https://diaonline.supermercadosdia.com.ar/leche-larga-vida-clasica-la-serenisma-200-ml-1695/p"
    ]

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
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
        start_time = time.time()
        carrefour_products = scrape_carrefour_product_info(query)
        dia_products = scrape_dia_product_info(query)
        all_products = carrefour_products + dia_products
        all_products.sort(key=lambda x: x['price'])
        
        # Añadir depuración aquí
        print(f"Query: {query}")
        print(f"Carrefour Products: {carrefour_products}")
        print(f"Día Products: {dia_products}")
        print(f"All Products: {all_products}")
        print(f"Tiempo total de búsqueda: {time.time() - start_time} segundos")

        return jsonify(all_products)
    except Exception as e:
        print(f"Error in search endpoint: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)