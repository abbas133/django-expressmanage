$(function() {
    // console.log( "document ready!" );
    init();
});


var init = function() {
    // console.log( "init ");
    hightlightCurrentSelection();
}


var hightlightCurrentSelection = function() {
    var pathname = window.location.pathname;
    console.log( "pathname : " + pathname);

    // Home page
    if(pathname == '' || pathname == '/') {
        $(".opt-home").addClass("nav-expanded nav-active")

    } else if(pathname.startsWith('/about')) {
        $(".opt-about").addClass("nav-expanded nav-active")
    }
}