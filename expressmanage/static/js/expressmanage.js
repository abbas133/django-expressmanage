$(document).ready(function() {
    // console.log( "document ready!" );
    init();
})

var init = function() {
    // console.log( "init ");
    activateNavItem();

    // initialize dynamic add more and remove option for formsets
    initFormsetOptions();
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

var initFormsetOptions = function() {
    $('.formset_row.container-type').formset({
        addText: 'Add More',
        deleteText: 'Remove',
        prefix: 'rateslab_set',
    });

    $('.formset_row.inward-order').formset({
        addText: 'Add More',
        deleteText: 'Remove',
        prefix: 'inoli_set',
    });
}