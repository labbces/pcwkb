from django.shortcuts import render


from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.functional_annotation.experimental.relationships.gene_experiment_association import GeneExperimentAssociation

def gene_page(request, gene_id):
    
    gene = Gene.objects.get(id=gene_id)

    context = {'gene_id': gene_id,
               'gene_name': gene.gene_name,
               'description': gene.description}
    
    return render(request, 'gene/gene_page.html', context)