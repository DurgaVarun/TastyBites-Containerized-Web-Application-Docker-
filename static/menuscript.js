  const cart = {};
    let total = 0;
    function addToCart(dish, price) {
      if (cart[dish]) {
        cart[dish].quantity += 1;
        cart[dish].totalPrice += price;
      } else {
        cart[dish] = {
          quantity: 1,
          totalPrice: price
        };
      }
      total += price;
      updateCartDisplay();
    }
    function updateCartDisplay() {
      const cartItems = document.getElementById("cartItems");
      const totalCost = document.getElementById("totalCost");
      cartItems.innerHTML = "";
      for (let item in cart) {
        const li = document.createElement("li");
        li.textContent = `${item} x ${cart[item].quantity} - ₹${cart[item].totalPrice}`;
        cartItems.appendChild(li);
      }
      totalCost.textContent = total;
    }
    function placeOrder() {
      if (Object.keys(cart).length === 0) {
        alert("Your cart is empty. Please add some dishes!");
        return;
      }
      let orderSummary = "Your Order:\n";
      for (let item in cart) {
        orderSummary += `${item} x ${cart[item].quantity} = ₹${cart[item].totalPrice}\n`;
      }
      orderSummary += `\nTotal Amount: ₹${total}`;
      alert(orderSummary + "\n\nThank you for ordering at TastyBites!");
      for (let item in cart) delete cart[item];
      total = 0;
      updateCartDisplay();
    }