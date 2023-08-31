function add() {
    var count = document.getElementById("volume_box").value;
    count = parseInt(count) + 1;
    document.getElementById("volume_box").value = count;
    updateTotal();
}

function sub() {
    var count = document.getElementById("volume_box").value;
    if (count <= 1) {
        count = 1;
    } else {
        count = parseInt(count) - 1;
    }
    document.getElementById("volume_box").value = count;
    updateTotal();
}



function updateTotal() {
    // 取得商品單價
    const priceElement = document.querySelector(`.product-price-hide`);
    const price = parseInt(priceElement.textContent.trim());

    const countElement = document.getElementById('volume_box');
    var count = parseInt(countElement.value);


    if (count == 0 || isNaN(count)) {
        count = 1;
    }

    if (count > 9999) {
        count = 9999;
    }

    countElement.value = count;

    // 更新商品總價格
    const total = price * count;
    const formattedTotal = 'NT$ ' + total.toLocaleString();

    const formatPriceElement = document.querySelector(`.product-price-title`);
    formatPriceElement.textContent = formattedTotal;
}