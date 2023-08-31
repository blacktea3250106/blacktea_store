document.addEventListener('DOMContentLoaded', () => {
    const quantityButtons = document.querySelectorAll('.quantity-btn');

    quantityButtons.forEach(button => {
        button.addEventListener('click', () => {
            const cartItemId = button.getAttribute('data-cart-id');
            const countElement = document.getElementById(`volume_box-${cartItemId}`);
            let newCount = parseInt(countElement.value);

            if (button.value === '+') {
                newCount += 1;
            } else if (button.value === '-' && newCount > 1) {
                newCount -= 1;
            }

            countElement.value = newCount;
            updateTotal(cartItemId);
        });
    });
});

function updateTotal(cartItemId) {
    // 取得商品單價
    const priceElement = document.querySelector(`.cart-product[data-cart-id="${cartItemId}"] .product-price`);
    const price = parseInt(priceElement.textContent.replace('NT$', '').replace(',', '').trim());

    const countElement = document.getElementById(`volume_box-${cartItemId}`);
    var count = parseInt(countElement.value);

    if (count == 0 || isNaN(count)) {
        count = 1;
    }

    if (count > 9999) {
        count = 9999;
    }

    console.log("count:", count)
    countElement.value = count;

    // 更新商品總價格
    const totalElement = document.querySelector(`.cart-product[data-cart-id="${cartItemId}"] .product-total`);
    const total = price * count;
    const formattedTotal = 'NT$ ' + total.toLocaleString();
    totalElement.textContent = formattedTotal;
    updateTotalCheckTotal();
    updateSelectQuantity();
    updateCartItemQuantity(cartItemId, count);
}

function updateTotalCheckTotal() {
    // 取得結帳span
    const totalAmount = document.querySelector('.total-amount');
    const productCheckboxes = document.querySelectorAll('.product-checkbox');
    let checkoutTotal = 0

    productCheckboxes.forEach(function(productCheckbox, index) {
        if (productCheckbox.checked) {
            const priceElement = document.querySelectorAll('.product-total')[index];
            const totalprice = parseInt(priceElement.textContent.replace('NT$ ', '').replace(/,/g, '').trim());
            checkoutTotal += totalprice;
        }
    });

    const formattedCheckoutTotal = 'NT$ ' + checkoutTotal.toLocaleString();
    totalAmount.textContent = formattedCheckoutTotal;

}

function updateSelectQuantity() {
    let selectedCount = 0;
    const productCheckboxes = document.querySelectorAll('.product-checkbox');
    const selectedItemsCount = document.querySelector('.selected-items-count');
    const checkoutCheckbox = document.querySelector('[data-cart-id="checkout-check"]');




    productCheckboxes.forEach(function(productCheckbox) {
        if (productCheckbox.checked) {
            const cartItemId = productCheckbox.getAttribute('data-cart-id');

            const countElement = document.getElementById(`volume_box-${cartItemId}`);
            selectedCount += parseInt(countElement.value);
        }
    });

    selectedItemsCount.textContent = selectedCount;

    checkoutCheckbox.checked = selectedCount > 0;
}

function updateCartItemQuantity(cartItemId, new_volume) {
    const data = {
        cart_item_id: cartItemId,
        volume: new_volume
    };

    fetch(`/update_volume`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
}

// 取得 CSRF Token 的函數
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}