var NEWS = {};
var SELECTED = null;

function handle_trends(trends) {
    $('#trends').empty();
    $('#news').empty();

    NEWS = {};

    var has_selected = 0;
    for (var i in trends) {
        var trend = trends[i];
        var obj = $(trend['trend']);
        /*
        if (obj.text() == SELECTED.text()) {
            SELECTED = obj;
            obj.addClass('selected');
            has_selected = 1;
        }
        */
        $('#trends').append(obj);
        NEWS[trend['url']] = trend['news'];
    }

    if (!has_selected) {
        SELECTED = null;
    }

    $('#trends li a').mouseenter(function() {
        $('#news').html(NEWS[this.href]);
    });

    $('#updated').text(new Date().toString());

    setTimeout(load_trends, 10 * 1000);
}

function load_trends() {
    $.getJSON('/get', {}, handle_trends);
}

$(document).ready(load_trends);
