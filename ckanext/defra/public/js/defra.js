$(document).ready(function () {
  /*
   * When the dataset page loads open the corresponding resource
   * to the id passed in the hash. If no resource id is passed
   * open the first resource
   */
  if ($('#resource-accordion').length > 0) {
    var qs = parseHash(window.location.hash);
    var el = qs.res ? $('#resource-' + qs.res) : $('#resource-accordion .panel-collapse').first();
    $(el).collapse('show');
    if (qs.res) {
      $('#resource-' + qs.res)
          .collapse('show')
          .parents('.mdf-resource').get(0).scrollIntoView()
    } else {
      $('#resource-accordion .panel-collapse').first().collapse('show');
    }
  }

  $('.location-typeahead').typeahead({
    displayText: function (item) {
      return item.district ? item.name + ', ' + item.district : item.name;
    },
    source: function (query, cb) {
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
    afterSelect: function (selectedItem) {
      clear_map_layers();
      if (selectedItem) {
        var bounds = [
          [selectedItem.Xmin, selectedItem.Ymax],
          [selectedItem.Xmax, selectedItem.Ymin]
        ];
        L.rectangle(bounds, {color: '#ef6f64', weight: 2, opacity: 1}).addTo(map);
        map.fitBounds(bounds);
        var bbox = [selectedItem.Ymin, selectedItem.Xmin, selectedItem.Ymax, selectedItem.Xmax];
        $('#ext_bbox,#ext_prev_extent').val(bbox.join(','));
        $('.search-form').submit();
      }
    }
  });

  /**
   * Dataset sort select
   */
  $('#dataset-sort').on('change', function () {
    $('#field-order-by').val($(this).val());
    $('#dataset-search-form').submit();
  });

  /**
   * Init tooltips
   */
  $('[data-toggle="tooltip"]').tooltip()
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
  map.eachLayer(function (layer) {
    if (count > 0) map.removeLayer(layer);
    count++;
  });
}


function parseHash(hash) {
  var qs = {};
  $(hash.replace('#', '').split('&')).each(function (i, q) {
    var parts = q.split('=');
    qs[parts[0]] = parts[1];
  });
  return qs;
}