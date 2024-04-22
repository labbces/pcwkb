from haystack import indexes
from .models.taxonomy.ncbi_taxonomy import Species

class SpeciesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    species_code = indexes.CharField(model_attr='species_code')
    scientific_name = indexes.CharField(model_attr='scientific_name')
    common_name = indexes.CharField(model_attr='common_name', null=True)
    family = indexes.CharField(model_attr='family')
    clade = indexes.CharField(model_attr='clade')
    photosystem = indexes.CharField(model_attr='photosystem')

    # Autocomplete
    content_auto = indexes.EdgeNgramField(model_attr='scientific_name')
    content_auto2 = indexes.EdgeNgramField(model_attr='common_name', null=True)

    def get_model(self):
        return Species

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
