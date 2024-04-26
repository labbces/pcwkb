from django.contrib import admin

from .models.taxonomy.ncbi_taxonomy import Species
from .models.molecular_components.genetic.genes import Gene
from .models.molecular_components.genetic.genomes import Genome
from .models.molecular_components.genetic.transcripts import Transcript
from .models.molecular_components.genetic.proteins import Protein
from .models.molecular_components.genetic.cds import CDS
from .models.molecular_components.relationships.orthogroups import Orthogroup, OrthogroupMethods
from .models.molecular_components.relationships.protein_orthogroup import ProteinOrthogroup
from .models.molecular_components.relationships.pcw_genetics_association import BiomassComposition
from .models.literature.literature import Literature
from .models.functional_annotation.computational.annotation_method import GenomeAnnotationMethod
from .models.functional_annotation.computational.cazyme import CAZyme, CAZymeProteinAssociation
from .models.functional_annotation.computational.gene_ontology import GeneOntologyTerm, GOProteinAssociation
from .models.functional_annotation.computational.interpro import InterPro, InterProProteinAssociation
from .models.functional_annotation.computational.kegg import MetabolicMap
from .models.functional_annotation.computational.transcriptional_regulation import TranscriptionalRegulatorFamily
from .models.functional_annotation.experimental.relationships.gene_experiment_association import GeneExperimentAssociation
from .models.functional_annotation.experimental.experiment import Experiment
from .models.molecular_components.pcw.biomass_composition import CellWallComponent
from .models.ontologies.experiment_related.eco import ECOTerm
from .models.ontologies.molecular_related.chebi import ChEBI
from .models.ontologies.plant_related.peco import PECOTerm
from .models.ontologies.plant_related.to import TOTerm
from .models.ontologies.plant_related.po import PlantOntologyTerm, PlantComponent, PlantComponentDevStage
from .models.temporary_data.data_submission import TemporaryData
from .models.temporary_data.species_submission import SpeciesTemporaryData
from .models.molecular_components.relationships.biomass_experiemnte_assoc import Experimentalevidenceplanttrait

class SpeciesAdmin(admin.ModelAdmin):
    """
    Class for adding species on Admin 
    """  
    def save_model(self, request, obj, form, change):
        """
        Function that saves the information obtained by insert_species_ncbi_taxid function 
        """  
        taxid = request.POST['taxid']
        obj = Species.insert_species_ncbi_taxid(taxid)
        super().save_model(request, obj, form, change)



class LitAdmin(admin.ModelAdmin):
    """
    Class for adding literature on Admin 
    """  
    def save_model(self, request, obj, form, change):
        """
        Function that saves the information obtained by get_lit_info function 
        """  
        doi = request.POST['doi']
        obj = Literature.get_lit_info(doi)
        super().save_model(request, obj, form, change)


admin.site.register(Species, SpeciesAdmin)
admin.site.register(Gene)
admin.site.register(Genome)
admin.site.register(Transcript)
admin.site.register(CDS)
admin.site.register(Protein)
admin.site.register(ProteinOrthogroup)
admin.site.register(OrthogroupMethods)
admin.site.register(Orthogroup)
admin.site.register(BiomassComposition)
admin.site.register(Literature, LitAdmin)
admin.site.register(GenomeAnnotationMethod)
admin.site.register(CAZyme)
admin.site.register(GeneOntologyTerm)
admin.site.register(GOProteinAssociation)
admin.site.register(InterPro)
admin.site.register(InterProProteinAssociation)
admin.site.register(MetabolicMap)
admin.site.register(TranscriptionalRegulatorFamily)
admin.site.register(PlantOntologyTerm)