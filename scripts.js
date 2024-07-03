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

    // Show the loading spinner
    spinner.style.display = 'block';

    try {
        const response = await fetch(`http://127.0.0.1:5000/search?query=${query}`);
        
        if (!response.ok) {
            console.error('Error fetching data:', response.statusText);
            return;
        }

        const products = await response.json();
        
        // Debugging received products
        console.log("Received products:", products);

        products.forEach(product => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = product.url;  
            a.target = '_blank'; 
            
            const formattedName = product.name.replace(/\b\w/g, char => char.toUpperCase());

            const img = document.createElement('img');
            img.src = product.image;
            img.alt = formattedName;
            img.style.width = '150px';
            img.style.height = '150px';
            a.textContent = `${formattedName} - $${product.price.toFixed(2)} - ${product.store}`;
            
            li.appendChild(img);
            li.appendChild(document.createTextNode(' '));
            li.appendChild(a);
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
