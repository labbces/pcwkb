from haystack import indexes
from .models.taxonomy.ncbi_taxonomy import Species

class SpeciesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    scientific_name = indexes.CharField(model_attr='scientific_name')
    common_name = indexes.CharField(model_attr='common_name')

    def get_model(self):
        return Species

