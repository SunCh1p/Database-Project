$(".user").hover(function(){
    if($(".arrow-btn").hasClass("rotate360")){
        $(".arrow-btn").removeClass("rotate360");
    }
    $(".arrow-btn").addClass("rotate180");
    $(".profile-pic, .arrow-btn, .user").addClass("highlight");
    var userPosition = $(this).offset();
    var userWidth = $(this).outerWidth();
    var menuLeft = userPosition.left;
    var menuTop = userPosition.top + $(this).outerHeight();
    $(this).find('.drop-down').css({
        'left': menuLeft,
        'top': menuTop
    }).slideDown(200);
}, function(){
    if($(".arrow-btn").hasClass("rotate180")){
        $(".arrow-btn").removeClass("rotate180")
    }
    $(".arrow-btn").addClass("rotate360");
    $(".profile-pic, .arrow-btn, .user").removeClass("highlight");
    $(this).find('.drop-down').slideUp(200);
});

