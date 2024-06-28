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
        // Mostrar la ventana emergente
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
            li.textContent = `${product.name} - $${product.price.toFixed(2)} - ${product.store}`;
            productList.appendChild(li);
        });
    } catch (error) {
        console.error('Error:', error);
    } finally {
        // Ocultar la rueda de carga
        spinner.style.display = 'none';
    }
}

function closeModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'none';
}
