$(document).ready(function () {
  /*
   * When the dataset page loads open the corresponding resource
   * to the id passed in the hash. If no resource id is passed
   * open the first resource
   */
  if ($('#resource-accordion').length > 0) {
    var qs = parseQueryString(window.location.hash);
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
   * Clear location search input
   */
  $('.location-search .form-control-clear').click(function() {
    $('#ext_bbox,#ext_prev_extent,#location').val("");
    clear_map_layers();
    $('.search-form').submit();
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
  $('[data-toggle="tooltip"]').tooltip();

  /**
   * Handle location search form show/hide
   */
  $('#location-search-collapse').on('shown.bs.collapse', function () {
    if (map) {
      if (!$(this).hasClass('pre-opened')) {
        map.invalidateSize();
        map.setZoom(5);
      }
    }
  }).on('hidden.bs.collapse', function() {
    $('#ext_bbox,#ext_prev_extent,#location').val("");
    clear_map_layers();
  });

  /*
   This is the only way to detect IE11.
   Add a class to the html element so we can handle the lack of webfonts on Defra machines.
  */
  if (!!window.MSInputMethodContext && !!document.documentMode) {
    document.documentElement.classList.add('isie');
  }

  /**
   * Show/hide the facets panel
   */
  $('.filter-toggle').click(function(e) {
    e.preventDefault();
    $('aside.secondary, .filters-show').toggle();
    $('aside.secondary').toggleClass('col-sm-3');
    $('div.primary').toggleClass('col-md-12')
  });

  /**
   * Toggle custom filters
   */
  $('.defra-custom-filters input[type="checkbox"]').on('change', function(e) {
    var name = $(e.currentTarget).attr('name');
    var params = parseQueryString(window.location.search.substr(1));
    if (name in params) {
      delete params[name];
    }
    else {
      params[name] = 'True';
    }
    window.location.search = buildQueryString(params);
  });
});

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


function parseQueryString(queryString) {
  var qs = {};
  $(queryString.replace('#', '').split('&')).each(function (i, q) {
    var parts = q.split('=');
    if (parts.length > 1) {
      qs[parts[0]] = parts[1];
    }
  });
  return qs;
}

function buildQueryString(parts) {
  var qs = [];
  $.each(parts, function(key, val) {
    qs.push(key + '=' + val);
  });
  return qs.join('&')
}