
$(document).ready(function () {
    $('#search-form').submit(function (event) {
        event.preventDefault(); // Prevent default form submission

        var query = $('#search-input').val().trim();
        if (query.length > 0) {
            // Manually trigger AJAX request to search_pcwkb endpoint
            $.ajax({
                url: '/pcwkb_core/search_pcwkb/',
                method: 'GET',
                data: { 'q': query },
                success: function (response) {
                    // Clear previous results
                    $('#search-results').empty();
                    // Display species names
                    $('#search-results').append('<p>Last search result: <a href="' + response.results.url + '" target="_blank">' + response.results.label + '</a></p>');
                },
                error: function (xhr, status, error) {
                    // Handle error
                    console.error(xhr.responseText);
                }
            });
        }
    });
});

