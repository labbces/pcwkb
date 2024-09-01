from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse

from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.molecular_components.genetic.proteins import Protein
from pcwkb_core.models.molecular_components.relationships.protein_orthogroup import ProteinOrthogroup
from pcwkb_core.models.functional_annotation.experimental.relationships.gene_experiment_association import GeneExperimentAssociation
from pcwkb_core.models.functional_annotation.experimental.relationships.biomass_gene_experiment_assoc import BiomassGeneExperimentAssoc
from pcwkb_core.models.functional_annotation.experimental.relationships.gene_interation_experiment_assoc import GeneInterationExperimentAssociation
from pcwkb_core.models.functional_annotation.computational.cazyme import CAZymeProteinAssociation
from pcwkb_core.models.functional_annotation.computational.interpro import ProteinInterproAssociation, ProteinInterproSourceInfo
from pcwkb_core.models.functional_annotation.computational.transcriptional_regulation import GeneTFAssociation

def paginated_gene_list(request, species_id):
    page_number = request.GET.get('page', 1)
    data_list = Gene.objects.filter(species_id=species_id)
    paginator = Paginator(data_list, 15)

    try:
        data = paginator.page(page_number)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    serialized_data = list(data.object_list.values())

    return JsonResponse({
        'data': serialized_data,
        'page': data.number,
        'num_pages': paginator.num_pages
    })


def paginated_gene_biomass_list(request, species_id):
    species_gene = Gene.objects.filter(species_id=species_id)
    page_number = request.GET.get('page', 1)
    data_list = BiomassGeneExperimentAssoc.objects.filter(gene__in=species_gene)
    paginator = Paginator(data_list, 15)

    try:
        data = paginator.page(page_number)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    # Use a set to track unique combinations
    seen = set()
    unique_associations = []
    
    for assoc in data.object_list:
        key = (
            assoc.gene.gene_name,
            assoc.gene.gene_id,
            assoc.plant_cell_wall_component.cellwallcomp_name if assoc.plant_cell_wall_component else None
        )
        if key not in seen:
            seen.add(key)
            unique_associations.append({
                'gene_id': assoc.gene.gene_id,
                'gene_name': assoc.gene.gene_name,
                'chebi': assoc.plant_cell_wall_component.cellwallcomp_name if assoc.plant_cell_wall_component else None,
                'experiment_count':BiomassGeneExperimentAssoc.objects.filter(gene=assoc.gene).count()
            })

    return JsonResponse({
        'data': unique_associations,
        'page': data.number,
        'num_pages': paginator.num_pages
    })

def paginated_gene_interaction_list(request, species_id):
    # Filter genes by species
    species_gene = Gene.objects.filter(species_id=species_id)
    
    # Get the page number from the request
    page_number = request.GET.get('page', 1)
    
    # Filter GeneInterationExperimentAssociation by genes within the species
    data_list = GeneInterationExperimentAssociation.objects.filter(gene_target__in=species_gene)
    
    # Paginate the data list
    paginator = Paginator(data_list, 15)
    
    try:
        data = paginator.page(page_number)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    
    # Use a set to track unique combinations
    seen = set()
    unique_associations = []
    
    for assoc in data.object_list:
        # Create a unique key based on putative_gene_regulator, gene_target, and experiment_species
        key = (
            assoc.putative_gene_regulator.gene_name,
            assoc.gene_target.gene_name,
            assoc.experiment_species
        )
        
        if key not in seen:
            seen.add(key)
            unique_associations.append({
                'putative_gene_regulator': assoc.putative_gene_regulator.gene_name,
                'gene_target': assoc.gene_target.gene_name,
                'experiment_species': assoc.experiment_species,
                'effect_on_target': assoc.effect_on_target,
                'experiment_count': assoc.experiment.count(),
            })
    
    # Return the data as a JSON response
    return JsonResponse({
        'data': unique_associations,
        'page': data.number,
        'num_pages': paginator.num_pages
    })


def gene_page(request, gene_name):
    gene = Gene.objects.get(gene_name=gene_name)
    proteins = {}

    proteins_objects = Protein.objects.filter(gene=gene)
    for obj in proteins_objects:
        protein = str(obj.protein_name)
        proteins[protein] = {
            'sequence': obj.sequence,
            'description': obj.description,
            'orthogroup': ProteinOrthogroup.objects.get(protein=obj).orthogroup if ProteinOrthogroup.objects.filter(protein=obj).exists() else None
        }
        
    tf_annotations = GeneTFAssociation.objects.filter(gene=gene)
    cazyme_annotations = CAZymeProteinAssociation.objects.filter(protein__gene=gene)

    print(cazyme_annotations, tf_annotations)

    assoc_objects = BiomassGeneExperimentAssoc.objects.filter(gene=gene)
    associations = list(assoc_objects) if assoc_objects.exists() else None

    context = {
        'gene_id': gene.gene_id,
        'gene_name': gene.gene_name,
        'description': gene.description,
        'original_db_info': gene.original_db_info,
        'proteins': proteins,
        'species': gene.species,
        'assoc_list': associations,
        'tf_annotations': tf_annotations,
        'cazyme_annotations': cazyme_annotations,
    }

    return render(request, 'gene/gene_page.html', context)
