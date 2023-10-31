from haystack import indexes
from .models.taxonomy.ncbi_taxonomy import Species

class SpeciesIndex(indexes.SearchIndex, indexes.Indexable):

scientific_name = indexes.CharField(document=True, use_template=True)
common_name = indexes.CharField(model_attr=’name’)