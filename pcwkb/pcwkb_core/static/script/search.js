$(document).ready(function() {
    $('#search-input').keyup(function() {
        var query = $(this).val().trim();
        if (query.length >= 0) { 
            $.ajax({
                url: '/pcwkb_core/autocomplete/',
                method: 'GET',
                data: { 'q': query },
                success: function(data) {
                    displaySuggestions(data);
                }
            });
        } else {
            $('#search-suggestions').empty();
        }
    });

    function displaySuggestions(suggestions) {
        var html = '';
        for (var i = 0; i < suggestions.length; i++) {
            var label = suggestions[i].label;
            html += '<li class="suggestion">' + label + '</li>';
        }
        $('#search-suggestions').html(html);
    }

    $(document).on('click', '.suggestion', function() {
        var suggestion = $(this).text();
        $('#search-input').val(suggestion);
        $('#search-suggestions').empty();
    });

    // Submit form on button click
    $('#search-form').submit(function(event) {
        var query = $('#search-input').val().trim();
        if (query.length > 0) {
            window.location.href = '/pcwkb_core/search/?q=' + encodeURIComponent(query);
        }
        event.preventDefault();
    });
});