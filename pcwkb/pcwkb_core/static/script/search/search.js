$(document).ready(function () {
    // jQuery: Handle model selection change event
    $('#model-select').change(function () {
        console.log("Script is running");
        var selectedModel = $(this).val(); // Get the selected model value
        if (selectedModel === 'genes' ||  selectedModel === 'cellwallcomp') {// Enable or disable species selector if genes or cellwallcomp is selected
            $('#species-select').show(); 
        } else {
            $('#species-select').hide();
        }
    });

    // jQuery: Handle form submission event
    $('#search-form').submit(function (event) {
        event.preventDefault(); // Prevent default form submission

        var query = $('#search-input').val().trim(); // Getting input values the search input value
        var model = $('#model-select').val(); 
        var speciesId = $('#species-select').val();

        if (query.length > 0) {
            $('#search-results').html('<p>Loading...</p>'); // Show loading indicator

            // jQuery AJAX: Make an AJAX request to search_pcwkb
            $.ajax({
                url: '/pcwkb_core/search_pcwkb/', // URL for search
                method: 'GET', // HTTP method
                data: { 'q': query, 'model': model, 'species_id': speciesId }, // Pass query, model, and species_id as parameters
                success: function (response) {
                    // Clear previous data
                    $('#search-results').empty();
                    $('#species-data').empty();
                    $('#gene-data').empty();

                    // Handle search results
                    let content = '';
                    if (response.results && response.results.length > 0) {
                        content = '<p>Search results for <strong>' + query + '</strong>:</p>';
                        // Iterate through results and display links
                        lastspecieshtml = "";
                        response.results.forEach(function(result) {
                            updateResponseDivs(result); // Update response divs
                        });
                    } else {
                        content = '<p>Search result: No results found.</p>';
                    }
                    $('#search-results').html(content); // jQuery: Display results in DOM
                },
                error: function (xhr, status, error) {
                    $('#search-results').empty(); // Clear previous results
                    $('#search-results').html('<p>Search result: An error occurred. Please try again later.</p>');
                    console.error(`Error: ${error}`);
                }
            });
        }
    });

    // Function to update response divs with template data
    function updateResponseDivs(result) {
        // Underscore.js: Compile templates
        var speciesTemplate = _.template($('#species-card-template').html());
        var geneTemplate = _.template($('#gene-card-template').html());
        var cellwallcompTemplate = _.template($('#cellwallcomp-card-template').html());

        // Update HTML with objectData content
        var speciesHtml = speciesTemplate({ species: '<a href="' + result.url_species + '" target="_blank">' + result.species + '</a>'});
        
        var geneHtml = '';
        if (result.gene) {
            geneHtml = geneTemplate({ genes: '<a href="' + result.url_gene + '" target="_blank">' + result.gene + '</a></p>' });
        }
        else if (result.genes_count) {
            geneHtml = geneTemplate({ genes: '<a href="' + result.url_species + '#pagination-links" target="_blank">' + result.genes_count + '</a></p>' });
        }
        else {
            geneHtml = geneTemplate({ genes: '<a href="' + result.genes + '#pagination-links" target="_blank">' + result.genes + '</a></p>' })
        }

        var cwcompHtml = cellwallcompTemplate({ cellwallcomp: '<a href="' + result.url_cellwallcomp + '" target="_blank">' + result.cellwallcomp + '</a>'});

        // jQuery: Update HTML with objectData content
        console.log(lastspecieshtml)
        if (lastspecieshtml != speciesHtml){
            lastspecieshtml = speciesHtml;
            console.log(lastspecieshtml, speciesHtml);
            $('#species-data').append(speciesHtml);
        }
        $('#gene-data').append(geneHtml);
        $('#cellwallcomp-data').append(cwcompHtml);
    }
});
