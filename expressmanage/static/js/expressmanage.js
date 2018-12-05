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

    // About page
    } else if(pathname.startsWith('/about')) {
        $(".opt-about").addClass("nav-expanded nav-active")
    
    // Customer options
    } else if(pathname.startsWith('/customers')) {
        $(".opt-customers").addClass("nav-expanded nav-active")

        if(pathname.indexOf('new') != -1) {
            $(".opt-customer-create").addClass("nav-active")
        } else {
            $(".opt-customer-list").addClass("nav-active")
        }
        
        // Product options
    } else if(pathname.startsWith('/products')) {
        $(".opt-products").addClass("nav-expanded nav-active")

        if(pathname.indexOf('new') != -1) {
            $(".opt-product-create").addClass("nav-active")
        } else {
            $(".opt-product-list").addClass("nav-active")
        }
    }


}