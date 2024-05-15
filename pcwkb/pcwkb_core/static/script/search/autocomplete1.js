$(document).ready(function () {
    $('#search-input').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: '/pcwkb_core/autocomplete/',
                method: 'GET',
                data: { q: request.term },
                success: function (data) {
                    response($.map(data, function (item) {
                        return {
                            label: item.label,
                            value: item.label
                        };
                    }));
                }
            });
        },
        autoFocus: true,
        minLength: 1,
        select: function (event, ui) {
            $('#search-input').val(ui.item.label);
            return false; // Previne o comportamento padrão
        }
    });

    $('#search-input').on('autocompleteselect', function(event, ui) {
        // Opcional: Faça algo quando um item for selecionado
        console.log('Selected: ' + ui.item.value);
    });
});