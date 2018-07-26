

var mapshow = $('#show-map')
mapshow.on('click', function () {
    if (mapshow.is(':checked')) {
        fake_show("#location-search")
        //$('.leaflet-draw-draw-rectangle').get(0).click();
        //$('.cancel').get(0).click();
    } else {
        fake_hide("#location-search")

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