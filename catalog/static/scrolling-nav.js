//jQuery to collapse the navbar on scroll
$(window).scroll(function() {

    if ($(window).scrollTop() > 50)
    {
        $(".navbar-fixed-top").addClass("top-nav-collapse");
        $(".blog_logo").animate({
            // left: "150px",
            opacity: "0.2"
        });
    } else if ($(window).scrollTop() <= 40) {
        $(".navbar-fixed-top").removeClass("top-nav-collapse");
        $(".blog_logo").animate({
            // left: "0px",
            opacity: "1.0"
        });

    }



});

//jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});
