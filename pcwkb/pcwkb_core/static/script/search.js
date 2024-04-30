$(document).ready(function() {
    $('#search-input').keyup(function() {
        var query = $(this).val().trim();
        if (query.length >= 0) { 
            $.ajax({
                url: '/pcwkb_core/autocomplete/',
                method: 'GET',
                data: { 'q': query },
                success: function(data) {
                    displayResults(data);
                }
            });
        } else {
            $('#search-results').empty();
        }
    });

    function displayResults(results) {
        var html = '';
        for (var i = 0; i < results.length; i++) {
            var label = results[i].label;
            var url = results[i].url;
            html += '<li><a href="' + url + '">' + label + '</a></li>';
        }
        $('#search-results').html(html);
    }
});