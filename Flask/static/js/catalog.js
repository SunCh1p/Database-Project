$(document).ready(function(){
    $(".product").hover(function(){
        if($(".arrow-btn").hasClass("rotate360")){
            $(".arrow-btn").removeClass("rotate360");
        }
        $(".arrow-btn").addClass("rotate180");
        $(".product").addClass("highlight");
        var productPosition = $(this).offset();
        var productWidth = $(this).outerWidth();
        var menuLeft = productPosition.left;
        var menuTop = productPosition.top + $(this).outerHeight();
        $(this).find('.product-details').css({
            'left': menuLeft,
            'top': menuTop
        }).slideDown(200);
    }, function(){
        if($(".arrow-btn").hasClass("rotate180")){
            $(".arrow-btn").removeClass("rotate180")
        }
        $(".arrow-btn").addClass("rotate360");
        $(".product").removeClass("highlight");
        $(this).find('.product-details').slideUp(200);
    });
});
