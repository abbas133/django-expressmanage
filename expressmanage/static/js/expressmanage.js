$(function() {
    // console.log( "document ready!" );
    init();
});


var init = function() {
    // console.log( "init ");
    activateNavItem();
}

var activateNavItem = function() {
    var url = window.location.pathname;
    var selectedElem = $('ul.nav a[href="'+ url +'"]')

    if(selectedElem.length == 0) {
        url = url.slice("0", url.indexOf("/", "1") + 1)
        selectedElem = $('ul.nav a[href="' + url + '"]')
    }

    $(selectedElem).closest("li").addClass('nav-expanded nav-active');
    $(selectedElem).closest(".nav-parent").addClass('nav-expanded nav-active');

}