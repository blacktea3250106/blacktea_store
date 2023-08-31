document.addEventListener("DOMContentLoaded", function() {
    const allCheckboxes = document.querySelectorAll('[data-cart-id="all-check"]');
    const productCheckboxes = document.querySelectorAll('.product-checkbox');
    const checkoutCheckbox = document.querySelector('[data-cart-id="checkout-check"]');
    const selectedItemsCount = document.querySelector('.selected-items-count');
    const totalAmount = document.querySelector('.total-amount');

    allCheckboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            productCheckboxes.forEach(function(productCheckbox) {
                productCheckbox.checked = checkbox.checked;
            });
            updateCheckoutStatus();
        });
    });

    productCheckboxes.forEach(function(productCheckbox) {
        productCheckbox.addEventListener('change', function() {
            let allChecked = true;
            productCheckboxes.forEach(function(checkbox) {
                if (!checkbox.checked) {
                    allChecked = false;
                }
            });
            allCheckboxes.forEach(function(checkbox) {
                checkbox.checked = allChecked;
            });
            updateCheckoutStatus();
        });
    });


    function updateCheckoutStatus() {
        let selectedCount = 0;
        let total = 0;


        productCheckboxes.forEach(function(productCheckbox, index) {
            if (productCheckbox.checked) {
                //----------怎麼抓到countElement的value
                const cartItemId = productCheckbox.getAttribute('data-cart-id');

                const countElement = document.getElementById(`volume_box-${cartItemId}`);
                selectedCount += parseInt(countElement.value);
                //---------------------
                const priceElement = document.querySelectorAll('.product-total')[index];
                const price = parseInt(priceElement.textContent.replace('NT$ ', '').replace(/,/g, '').trim()); // 假设价格格式为 $99.99
                total += price;
            }
        });

        selectedItemsCount.textContent = selectedCount;

        const formattedTotal = 'NT$ ' + total.toLocaleString();
        totalAmount.textContent = formattedTotal;
        checkoutCheckbox.checked = selectedCount > 0;
    }
});