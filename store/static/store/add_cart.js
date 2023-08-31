document.addEventListener('DOMContentLoaded', function() {
    const colorButtons = document.querySelectorAll('.color-btn');
    const capacityButtons = document.querySelectorAll('.capacity-btn');
    const addToCartButton = document.getElementById('add-to-cart');
    const product_name = addToCartButton.getAttribute('data-product'); // Get product value from data-product attribute


    let selectedColor = null;
    let selectedCapacity = null;

    colorButtons.forEach(button => {
        button.addEventListener('click', () => {
            colorButtons.forEach(btn => btn.classList.remove('focused'));
            button.classList.add('focused');
            selectedColor = button.textContent;

        });
    });

    capacityButtons.forEach(button => {
        button.addEventListener('click', () => {
            capacityButtons.forEach(btn => btn.classList.remove('focused'));
            button.classList.add('focused');
            selectedCapacity = button.textContent;
        });
    });

    addToCartButton.addEventListener('click', () => {
        if (selectedColor && selectedCapacity) {
            const countElement = document.getElementById('volume_box');
            const count = parseInt(countElement.value);

            const data = {
                product_name: product_name,
                color: selectedColor,
                capacity: selectedCapacity,
                volume: count
            };

            fetch(`/add_cart`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    // 处理从后端返回的响应
                    console.log('已經數據發送到後端', data);

                    // 显示SweetAlert2成功提示
                    Swal.fire({
                        icon: 'success',
                        title: '已加入購物車！',
                        showConfirmButton: false,
                        timer: 1000,
                    });
                })
                .catch(error => {
                    Swal.fire({
                        icon: 'info',
                        title: '尚未登入會員',
                        html: '會員才能使用購物車哦！',
                        showCloseButton: true,
                        showCancelButton: false,
                        focusConfirm: false,
                        showCloseButton: false,
                    });
                    console.error('錯誤訊息', error);
                });
        } else {
            console.log('請選擇顏色和容量');
        }
    });
});