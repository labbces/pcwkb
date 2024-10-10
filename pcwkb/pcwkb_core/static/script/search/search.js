$(document).ready(function () {

    $('#species_results').hide();
    $('#genes_results').hide();
    $('#cellwallcomp_results').hide();

    // Função para atualizar a URL
    function updateURL(query, model, speciesId) {
        const newURL = `${window.location.protocol}//${window.location.host}/search_engine/?q=${encodeURIComponent(query)}&model=${model}&species_id=${speciesId}`;
        window.history.pushState({ path: newURL }, '', newURL);
    }

    $('#model-select').change(function () {
        var selectedModel = $(this).val();
        if (selectedModel === 'genes' || selectedModel === 'cellwallcomp') {
            $('#species-select').show();
        } else {
            $('#species-select').hide();
        }
    });

    $('#search-form').submit(function (event) {
        event.preventDefault();

        var query = $('#search-input').val().trim();
        var model = $('#model-select').val();
        var speciesId = $('#species-select').val();

        if (query.length > 0) {
            $('#search-results').html('<p>Loading...</p>');
            $('#species-data').empty();
            $('#gene-data').empty();
            $('#cellwallcomp-data').empty();
            
            $('#species_results').hide();
            $('#genes_results').hide();
            $('#cellwallcomp_results').hide();

            // Atualiza a URL no navegador
            updateURL(query, model, speciesId);

            $.ajax({
                url: '/search_pcwkb/',
                method: 'GET',
                data: { 'q': query, 'model': model, 'species_id': speciesId },
                success: function (response) {
                    $('#search-results').empty();


                    let content = "";
                    if (response.results && response.results.length > 0) {
                        content = '<p>Search results for <strong>' + query + '</strong>:</p>';
                        response.results.forEach(function(result) {
                            updateResponseDivs(result);
                        });
                    } else {
                        content = '<p>Search result: No results found.</p>';
                    }
                    $('#search-results').html(content);
                },
                error: function (xhr, status, error) {
                    $('#search-results').empty();
                    $('#search-results').html('<p>Search result: An error occurred. Please try again later.</p>');
                    console.error(`Error: ${error}`);
                }
            });
        }
    });

    function updateResponseDivs(result) {
        var speciesTemplate = _.template($('#species-card-template').html());
        var geneTemplate = _.template($('#gene-card-template').html());
        var cellwallcompTemplate = _.template($('#cellwallcomp-card-template').html());

        var speciesHtml = '';
        var geneHtml = '';
        var cwcompHtml = '';

        if (result.cellwallcompquery) {
            cwcompHtml = cellwallcompTemplate({
                cellwallcomp: '<p><a href="' + result.url_cellwallcomp + '" target="_blank">' + result.cellwallcomp + '</a></p>'
            });
        
            
            if (result.species && result.species.length > 0) {
                result.species.forEach(function(species) {
                    speciesHtml += speciesTemplate({ species: '<a href="#">' + species + '</a>' });
                });
            } else {
                speciesHtml = speciesTemplate({ species: '<p>No species associated</p>' });
            }
        
            
            if (result.genes && result.genes.length > 0) {
                result.genes.forEach(function(gene) {
                    geneHtml += geneTemplate({ genes: '<p><a href="#">' + gene + '</a></p>' });
                });
            } else {
                geneHtml = geneTemplate({ genes: '<p>No genes associated</p>' });
            }
        } else {

            var speciesHtml = speciesTemplate({ species: '<a href="' + result.url_species + '" target="_blank">' + result.species + '</a>'});
            
            if (result.gene) {
                geneHtml = geneTemplate({ genes: '<p><a href="' + result.url_gene + '" target="_blank">' + result.gene + '</a></p>' });
            } else if (result.genes_count && result.genes_count !== 0) {
                geneHtml = geneTemplate({ genes: '<p><a href="' + result.url_species + '#pagination-links" target="_blank">' + result.genes_count + '</a></p>' });
            } else {
                geneHtml = geneTemplate({ genes: '<p>No Genes</p>' });
            }
            
            if (result.cellwallcomp && result.cellwallcomp.length > 0) {
                result.cellwallcomp.forEach(function(cellwallcomp) {
                    cwcompHtml += cellwallcompTemplate({ 
                        cellwallcomp: '<p><a href="/cellwallcomponent_page/' + cellwallcomp + '" target="_blank">' + cellwallcomp + '</a></p>' 
                    });
                });
            } else {
                cwcompHtml = cellwallcompTemplate({cellwallcomp: '<p>No Cell Wall Components</p>'});
            }
        }

        $('#species-data').append(speciesHtml);
        $('#gene-data').append(geneHtml);
        $('#cellwallcomp-data').append(cwcompHtml);

        $('#species_results').show();
        $('#genes_results').show();
        $('#cellwallcomp_results').show();
    }

    // Função para lidar com o carregamento inicial da página com parâmetros na URL
    function handleInitialLoad() {
        const urlParams = new URLSearchParams(window.location.search);
        const query = urlParams.get('q');
        const model = urlParams.get('model');
        const speciesId = urlParams.get('species_id');

        if (query) {
            $('#search-input').val(query);
        }
        if (model) {
            $('#model-select').val(model).change();
        }
        if (speciesId && (model === 'genes' || model === 'cellwallcomp')) {
            $('#species-select').val(speciesId).show();
        }

        if (query) {
            $('#search-form').submit();
        }
    }

    // Chama a função para carregar os dados iniciais da URL
    handleInitialLoad();
});
