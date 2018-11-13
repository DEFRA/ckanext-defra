
$(document).ready(function(){
    $('#additional-expando').on('click', function(){
        var chev = $(this).find('.chevron').get(0)
        $(chev).toggleClass("fa-chevron-right fa-chevron-down")

        $('#additional-info').toggle();
    });

    $('.resource-expand').on('click', function(){
        var toggle = $(this).siblings('.resource-expando').get(0)

        var chev = $(this).find('.chevron').get(0)
        $(chev).toggleClass("fa-chevron-right fa-chevron-down")
        $(toggle).toggle()
    });

    $('.resource-expand').each(function(idx, val){
        var toggle = $(this).siblings('.resource-expando').get(0)
        $(toggle).css('display', 'none')
    })

    if( $('.expando-report').length > 0 ) {
        $('.expando-report').on('click', function(){
            var chev = $(this).siblings('ul').get(0)
            $(chev).toggle();
        });

    }
});

var mapshow = $('#show-map')
mapshow.on('click', function () {
    var field = "#location-search"

    if (mapshow.is(':checked')) {
        fake_show(field)
    } else {
        fake_hide(field)

        /*
            Clear the values in the spatial search, although we really
            want to reset the map itself (but it is hidden away in a CKAN
            sandbox)
        */
        $('#ext_bbox').val("");
        $('#ext_prev_extent').val("");
    }
})

if (!mapshow.is(':checked')) {
    fake_hide("#location-search")
}

function fake_show(e) {
    $(e).css({
        position: 'relative',
        visibility: 'visible',
        display: 'block'
    });
}

function fake_hide(e) {
    $(e).css({
        position: 'absolute',
        visibility: 'hidden',
        display: 'block'
    });
}