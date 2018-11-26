
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

    $('.location-typeahead').typeahead({
        displayText: function(item) {
            return item.district ? item.name + ', ' + item.district : item.name;
        },
        source: function(query, cb) {
            if (query && query.length > 3) {
                $.ajax({
                    url: this.$element.data('locationServiceUrl') + '?q=' + query.split(',')[0],
                    dataType: 'json',
                    crossDomain: true,
                    success: function (resp) {
                        if (resp.Results.Place && resp.Results.Place.length > 0) {
                            return cb(resp.Results.Place)
                        }
                        return cb([]);
                    },
                    error: function () {
                        return cb([]);
                    }
                });
            }
            return cb([]);
        },
        afterSelect: function(selectedItem) {
            clear_map_layers();
            if (selectedItem) {
                var bounds = [
                    [selectedItem.Xmin, selectedItem.Ymax],
                    [selectedItem.Xmax, selectedItem.Ymin]
                ];
                L.rectangle(bounds, {color: '#ef6f64', weight: 2, opacity: 1}).addTo(map);
                map.fitBounds(bounds);
                var bbox = [selectedItem.Ymax, selectedItem.Xmin, selectedItem.Ymin, selectedItem.Xmax];
                $('#ext_bbox,#ext_prev_extent').val(bbox.join(','));
                $('.search-form').submit();
            }
        }
    });
});

var mapshow = $('#show-map')
mapshow.on('click', function () {
    var field = "#location-search"

    if (mapshow.is(':checked')) {
        fake_show(field)
    } else {
        fake_hide(field);
        // Clear the location form and map
        $('#ext_bbox,#ext_prev_extent,#location').val("");
        clear_map_layers();
    }
});

if (!mapshow.is(':checked')) {
    fake_hide("#location-search")
}

function fake_show(e) {
    $(e).css({
        position: 'relative',
        visibility: 'visible',
        display: 'block'
    });
    if (map) map.invalidateSize();
}

function fake_hide(e) {
    $(e).css({
        position: 'absolute',
        visibility: 'hidden',
        display: 'block'
    });
}

/*
 * Clear all but the base layer of the map
 */
function clear_map_layers() {
    var count = 0;
    map.eachLayer(function(layer){
        if (count > 0) map.removeLayer(layer);
        count++;
    });
}
