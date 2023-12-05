from django.contrib import admin

from .models.taxonomy.ncbi_taxonomy import Species
from .models.molecular_components.genetic_components.genes import Gene
from .models.molecular_components.genetic_components.genomes import Genome
from .models.biomass.biomass_composition import BiomassComposition
from .models.literature.literature import Literature
from .models.functional_annotation.annotation_method import GenomeAnnotationMethod
from .models.functional_annotation.cazyme import CAZyme, CAZymeProteinAssociation
from .models.functional_annotation.gene_ontology import GeneOntologyTerm, GOProteinAssociation
from .models.functional_annotation.interpro import InterPro, InterProProteinAssociation
from .models.functional_annotation.metabolic_map import MetabolicMap
from .models.functional_annotation.transcript import Transcript, TranscriptionalRegulatorFamily, TranscRegProteinAssociation


class LitAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        doi = request.POST['doi']
        obj = Literature.get_lit_info(doi)
        super().save_model(request, obj, form, change)


admin.site.register(Species)
admin.site.register(Gene)
admin.site.register(Genome)
admin.site.register(BiomassComposition)
admin.site.register(Literature, LitAdmin)
admin.site.register(GenomeAnnotationMethod)
admin.site.register(CAZyme, CAZymeProteinAssociation)
admin.site.register(GeneOntologyTerm, GOProteinAssociation)
admin.site.register(InterPro, InterProProteinAssociation)
admin.site.register(MetabolicMap)
admin.site.register(Transcript, TranscriptionalRegulatorFamily, TranscRegProteinAssociation)