console.log("add_item_to_card.js");

const submitBtn = document.getElementById("add-item-to-cart-submit");
const addItemForm = document.getElementById("add-item-to-cart-form");

submitBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    console.log("submit");
    const formData = new FormData(addItemForm);
    console.log(formData);

    const response = await fetch("/shop/add-item-to-cart", {
        method: "POST",
        body: formData,
      });
      //console.log(await response.json());
      //const responseData = await response.json();
      //console.log(responseData);
      window.location.reload();
      //alert("Item added to cart!");

});