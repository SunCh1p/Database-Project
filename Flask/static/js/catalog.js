$(document).ready(function() {
    // Function to add item to cart
    $(".add-to-cart-button").click(function() {
        var productId = $(this).data("product-id");

        // Make AJAX request to add item to cart
        $.ajax({
            url: '/api/add-to-cart',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ product_id: productId, quantity: 1 }), // Assuming quantity is always 1 for simplicity
            success: function(response) {
                // Handle success (e.g., show message to user)
                alert("Item added to cart successfully!");
            },
            error: function(xhr, status, error) {
                // Handle error
                console.error("Error adding item to cart:", error);
            }
        });
    });

    // Function to buy item
    $(".buy-now-button").click(function() {
        var productId = $(this).data("product-id");

        // Make AJAX request to buy item
        $.ajax({
            url: '/api/buy-now',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ product_id: productId, quantity: 1 }), // Assuming quantity is always 1 for simplicity
            success: function(response) {
                // Handle success (e.g., redirect to cart page)
                window.location.href = '/cart';
            },
            error: function(xhr, status, error) {
                // Handle error
                console.error("Error buying item:", error);
            }
        });
    });

    // Mouse enter event handler
    $(".user").mouseenter(function() {
        var userElement = $(this);
        var arrowBtn = $(".arrow-btn", userElement);
        var profilePic = $(".profile-pic", userElement);

        if (arrowBtn.hasClass("rotate360")) {
            arrowBtn.removeClass("rotate360");
        }
        arrowBtn.addClass("rotate180");
        profilePic.addClass("highlight");
        userElement.addClass("highlight");

        var userPosition = userElement.offset();
        var userWidth = userElement.outerWidth();
        var menuLeft = userPosition.left;
        var menuTop = userPosition.top + userElement.outerHeight();

        var dropDownMenu = $(".drop-down", userElement);
        dropDownMenu.css({
            left: menuLeft + "px",
            top: menuTop + "px",
            display: "block"
        });
    });

    // Mouse leave event handler
    $(".user").mouseleave(function() {
        var userElement = $(this);
        var arrowBtn = $(".arrow-btn", userElement);
        var profilePic = $(".profile-pic", userElement);

        if (arrowBtn.hasClass("rotate180")) {
            arrowBtn.removeClass("rotate180");
        }
        arrowBtn.addClass("rotate360");
        profilePic.removeClass("highlight");
        userElement.removeClass("highlight");

        var dropDownMenu = $(".drop-down", userElement);
        dropDownMenu.css("display", "none");
    });
});
