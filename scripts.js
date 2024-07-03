document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('modal');
    modal.style.display = 'none';
});

async function searchProduct() {
    const query = document.getElementById('search-input').value.toLowerCase();
    const productList = document.getElementById('product-list');
    const spinner = document.getElementById('loading-spinner');
    const modal = document.getElementById('modal');
    productList.innerHTML = '';

    if (!query) {
        modal.style.display = 'flex';
        return;
    }

    // Mostrar la rueda de carga
    spinner.style.display = 'block';

    try {
        const response = await fetch(`http://127.0.0.1:5000/search?query=${query}`);
        
        if (!response.ok) {
            console.error('Error fetching data:', response.statusText);
            return;
        }

        const products = await response.json();
        
        // Añadir depuración aquí
        console.log("Productos recibidos:", products);

        products.forEach(product => {
            const li = document.createElement('li');
            
            // Imagen del producto
            const img = document.createElement('img');
            img.src = product.image;
            img.alt = product.name.replace(/\b\w/g, char => char.toUpperCase());
            img.style.width = '150px';
            img.style.height = '150px';
            li.appendChild(img);
            
            // Espacio entre imagen del producto y el texto
            li.appendChild(document.createTextNode(' '));
            
            // Link al producto
            const a = document.createElement('a');
            a.href = product.url;
            a.target = '_blank';
            a.textContent = `${product.name.replace(/\b\w/g, char => char.toUpperCase())} - $${product.price.toFixed(2)} - ${product.store}`;
            li.appendChild(a);
            
            // Espacio entre el texto y el logo del supermercado
            li.appendChild(document.createTextNode(' '));

            // Imagen del logo del supermercado
            const storeLogo = document.createElement('img');
            if (product.store === 'Carrefour') {
                storeLogo.src = 'carrefour_logo.png';
            } else if (product.store === 'Día') {
                storeLogo.src = 'dia_logo.png';
            }
            storeLogo.alt = `${product.store} Logo`;
            storeLogo.style.width = '20%';
            storeLogo.style.height = '20%';
            li.appendChild(storeLogo);

            productList.appendChild(li);
        });
    } catch (error) {
        console.error('Error:', error);
    } finally {
        spinner.style.display = 'none';
    }
}

function closeModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'none';
}
