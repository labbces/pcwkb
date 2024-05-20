$(document).ready(function () {
    $('#search-form').submit(function (event) {
        event.preventDefault(); // Prevent default form submission

        var query = $('#search-input').val().trim();
        if (query.length > 0) {
            $('#search-results').html('<p>Loading...</p>'); // Loading indicator

            // Manually trigger AJAX request to search_pcwkb endpoint
            $.ajax({
                url: '/pcwkb_core/search_pcwkb/',
                method: 'GET',
                data: { 'q': query },
                success: function (response) {
                    // Clear previous data
                    $('#search-results').empty();
                    $('#species-data').empty();
                    $('#gene-data').empty();

                    let content = '';
                    if (response.results && response.results.length > 0) {
                        content = '<p>Search results:</p>';
                        response.results.forEach(function(result) {
                            content += '<p><a href="' + result.url_species + '" target="_blank">' + result.label + '</a></p>';
                            updateResponseDivs(result);
                        });
                    } else {
                        content = '<p>Search result: No results found.</p>';
                    }
                    $('#search-results').html(content);
                },
                error: function (xhr, status, error) {
                    $('#search-results').empty(); // Clear previous results
                    $('#search-results').html('<p>Search result: An error occurred. Please try again later.</p>');
                    console.error(`Error: ${error}`);
                }
            });
        }
    });

    function updateResponseDivs(result) {
        // Compile templates
        var speciesTemplate = _.template($('#species-card-template').html());
        var geneTemplate = _.template($('#gene-card-template').html());

        // Update the HTML with the objectData content
        var speciesHtml = speciesTemplate({ specie: '<a href="' + result.url_species + '" target="_blank">' + result.specie + '</a></p>' });
        
        var geneHtml = '';
        if (result.gene_name) {
            geneHtml = geneTemplate({ genes: '<a href="' + result.url_gene + '" target="_blank">' + result.gene_name + '</a></p>' });
        } else {
            geneHtml = geneTemplate({ genes: '<a href="' + result.url_species + '#pagination-links" target="_blank">' + result.genes_count + '</a></p>' });
        }

        $('#species-data').append(speciesHtml);
        $('#gene-data').append(geneHtml);
    }
});
