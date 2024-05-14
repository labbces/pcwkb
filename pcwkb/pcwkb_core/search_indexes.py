from haystack import indexes
from .models.taxonomy.ncbi_taxonomy import Species
from .models.molecular_components.genetic.genes import Gene

class SpeciesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    species_code = indexes.CharField(model_attr='species_code')
    scientific_name = indexes.CharField(model_attr='scientific_name')
    common_name = indexes.CharField(model_attr='common_name', null=True)
    family = indexes.CharField(model_attr='family')
    clade = indexes.CharField(model_attr='clade')
    photosystem = indexes.CharField(model_attr='photosystem')

    # Autocomplete
    scientific_name_auto = indexes.EdgeNgramField(model_attr='scientific_name')
    common_name_auto = indexes.EdgeNgramField(model_attr='common_name', null=True)
    #species_code_auto = indexes.EdgeNgramField(model_attr='species_code')

    def get_model(self):
        return Species

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    
class GeneIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    gene_name = indexes.CharField(model_attr='gene_name')
    gene_description = indexes.CharField(model_attr='description', null=True)

    # Autocomplete
    gene_name_auto = indexes.EdgeNgramField(model_attr='gene_name')
    gene_description_auto = indexes.EdgeNgramField(model_attr='description', null=True)

    def get_model(self):
        return Gene

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

