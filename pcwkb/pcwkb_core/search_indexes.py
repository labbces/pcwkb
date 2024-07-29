from haystack import indexes
from .models.taxonomy.ncbi_taxonomy import Species
from .models.molecular_components.genetic.genes import Gene
from .models.biomass.cellwall_component import CellWallComponent

class SpeciesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    scientific_name = indexes.CharField(model_attr='scientific_name')
    common_name = indexes.CharField(model_attr='common_name', null=True)
    family = indexes.CharField(model_attr='family')
    clade = indexes.CharField(model_attr='clade')
    photosystem = indexes.CharField(model_attr='photosystem', null=True)

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
    gene_id = indexes.CharField(model_attr='gene_id', null=True)
    gene_name = indexes.CharField(model_attr='gene_name', null=True)
    gene_description = indexes.CharField(model_attr='description', null=True)
    species = indexes.CharField(model_attr='species__scientific_name')

    # Autocomplete
    gene_name_auto = indexes.EdgeNgramField(model_attr='gene_name')
    gene_description_auto = indexes.EdgeNgramField(model_attr='description', null=True)

    def get_model(self):
        return Gene

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    
class CellWallComponentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    cellwallcomp_name = indexes.CharField(model_attr='cellwallcomp_name', null=True)
    cellwallcomp_description = indexes.CharField(model_attr='description', null=True)

    # Autocomplete
    cellwallcomp_name_auto = indexes.EdgeNgramField(model_attr='cellwallcomp_name')
    cellwallcomp_description_auto = indexes.EdgeNgramField(model_attr='description', null=True)

    def get_model(self):
        return CellWallComponent

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

