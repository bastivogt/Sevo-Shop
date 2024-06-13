
const update_cart = document.querySelectorAll(".update-cart");
const shopping_cart_badge = document.getElementById("shopping-cart-badge");

shopping_cart_badge.textContent = "8";


function update_shoppping_cart() {
    
}


for(let item of update_cart) {
    item.addEventListener("click", (e) => {
        console.log(item.dataset.productId);
    })
}