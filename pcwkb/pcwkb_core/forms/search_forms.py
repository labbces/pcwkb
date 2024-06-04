from haystack.forms import ModelSearchForm

class CustomSearchForm(ModelSearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['q'].widget.attrs.update({'id': 'search-input',
                                              'class': 'form-control flex-grow-1 me-2',
                                              'placeholder': 'Search...',
                                              'aria-label': 'Search'})
        self.fields['models'].widget.attrs.update({'class': 'form-check'})