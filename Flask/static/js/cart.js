

$(document).ready(function(){
    // Array to store cart items
    var cartItems = [];

    // Function to update the cart total
    function updateCartTotal() {
        var totalAmount = 0;
        // Calculate total amount by summing up prices of all items in the cart
        cartItems.forEach(function(item) {
            totalAmount += item.price * item.quantity;
        });
        // Update the total amount displayed on the page
        $("#cart-total-amount").text("$" + totalAmount.toFixed(2));
    }

    // Function to render cart items
    function renderCartItems() {
        $(".cart-items").empty(); // Clear existing cart items
        cartItems.forEach(function(item) {
            var itemHTML = '<div class="cart-item">';
            itemHTML += '<p><strong>Product Name:</strong> ' + item.name + '</p>';
            itemHTML += '<p><strong>Price:</strong> $' + item.price.toFixed(2) + '</p>';
            itemHTML += '<p><strong>Quantity:</strong> ' + item.quantity + '</p>';
            itemHTML += '</div>';
            $(".cart-items").append(itemHTML);
        });
    }

    // Event listener for add to cart button
    $(".add-to-cart-btn").click(function() {
        var productId = $(this).data("product-id");
        // Assuming you have a way to retrieve product details based on productId
        var product = getProductDetails(productId);
        if (product) {
            // Check if the product is already in the cart
            var existingItem = cartItems.find(function(item) {
                return item.id === productId;
            });
            if (existingItem) {
                // If the product is already in the cart, increase its quantity
                existingItem.quantity++;
            } else {
                // If the product is not in the cart, add it
                cartItems.push({
                    id: productId,
                    name: product.name,
                    price: product.price,
                    quantity: 1
                });
            }
            // Render cart items and update cart total
            renderCartItems();
            updateCartTotal();
        }
    });

    // Event listener for checkout button
    $("#checkout-btn").click(function() {
        // Perform checkout action (e.g., redirect to checkout page)
        // Here you can add your own logic for what happens when the user clicks the checkout button
        alert("Checkout functionality is not implemented yet!");
    });

    // This function is just a placeholder. You should replace it with your own function to retrieve product details from your backend or wherever they are stored.
    function getProductDetails(productId) {
        // Example of how you might retrieve product details from a list of products
        return Products.find(function(product) {
            return product.id === productId;
        });
    }
});
