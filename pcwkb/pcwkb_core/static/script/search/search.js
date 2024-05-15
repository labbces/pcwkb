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
                    $('#search-results').html('<p>Search result: <a href="' + response.results.url + '" target="_blank">' + response.results.label + '</a></p>');
                    // Update object data
                    updateObjectData(response);
                },
                error: function (xhr, status, error) {
                    // Handle error
                    console.error(xhr.responseText);
                }
            });
        }
    });

    function updateObjectData(response) {
        // Update the HTML with the objectData content
        var speciesHtml = `<p>Species: ${response.results.specie}</p>`;
        var geneHtml = `<p>Gene: ${response.results.genes}</p>`;
        
        $('#species-data').html(speciesHtml);
        $('#gene-data').html(geneHtml);
    }
});