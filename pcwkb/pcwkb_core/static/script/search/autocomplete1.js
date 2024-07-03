$(document).ready(function () {
    // jQuery: Initialize autocomplete widget on the input field with ID
    $('#search-input').autocomplete({
        // jQuery UI: Configure the autocomplete widget
        source: function (request, response) {
            // jQuery AJAX:  Make an AJAX request to autocomplete
            //(according to the view this autocomplete depends on the "*_auto" indexes in the search_view and search_indexes)
            $.ajax({
                url: '/pcwkb_core/autocomplete/',
                method: 'GET',
                data: { q: request.term }, // Pass search term as data
                success: function (data) {
                    // Map the returned data to the format expected by jQuery UI
                    response($.map(data, function (item) {
                        return {
                            label: item.label
                        };
                    }));
                }
            });
        },
        autoFocus: true, // Automatically focus on the first item
        minLength: 1,    // Minimum characters before triggering the autocomplete
        select: function (event, ui) {
            $('#search-input').val(ui.item.label); // jQuery: Set the selected value in the input field
            return false; // Prevent default behavior
        }
    });

    // jQuery: Handle autocompleteselect event (now it is just showing in the console)
    $('#search-input').on('autocompleteselect', function(event, ui) {
        console.log('Selected: ' + ui.item.value);
    });
});
