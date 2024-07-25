from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.functional_annotation.experimental.relationships.biomass_gene_experiment_assoc import BiomassGeneExperimentAssoc
from pcwkb_core.models.ontologies.experiment_related.eco import ECOTerm
from pcwkb_core.models.ontologies.plant_related.peco import PECOTerm
from pcwkb_core.models.ontologies.plant_related.po import PlantOntologyTerm
from pcwkb_core.models.ontologies.plant_related.to import TOTerm
from pcwkb_core.models.biomass.cellwall_component import CellWallComponent
from pcwkb_core.models.biomass.plant_component import PlantComponent
from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.literature.literature import Literature
from pcwkb_core.models.functional_annotation.experimental.experiment import Experiment
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ForeignKey, ManyToManyField, CharField, IntegerField, TextField, JSONField, ManyToOneRel
import pandas as pd

def validate_model_data(data, model_class):
    errors = {}
    warnings = {}

    # Get model fields
    model_fields = {field.name: field for field in model_class._meta.get_fields()}

    for field_name, field in model_fields.items():       
        
        field_value = data.get(field_name)
        print(field, field_name,field_value)
        if pd.isna(field_value):
            field_value = None

        # Skip ManyToOneRel fields (reverse relationships)
        if isinstance(field, ManyToOneRel):
            continue

        # Check if the field is allowed to be null or blank
        is_null = getattr(field, 'null', False)
        is_blank = getattr(field, 'blank', False)


        if (is_blank and field_value == '') or (is_null and field_value is None):
            continue  # Skip validation for this field if it's allowed to be blank or null

        # If field is not allowed to be null/blank and value is None, it's an error
        if field_value is None and not (is_blank or is_null):
            errors[field_name] = 'This field is required and cannot be null or blank.'

        # Add specific validation for field types here, if needed
        if isinstance(field, IntegerField):
            if field_value is not None and not isinstance(field_value, int):
                errors[field_name] = 'Invalid integer value. Field Value: {field_value}'
        elif isinstance(field, CharField):
            if field_value is not None and not isinstance(field_value, str):
                errors[field_name] = 'Invalid string value. Field Value: {field_value}'
        elif isinstance(field, TextField):
            if field_value is not None and not isinstance(field_value, str):
                errors[field_name] = 'Invalid text value. Field Value: {field_value}'
        elif isinstance(field, JSONField):
            if field_value is not None:
                import json
                try:
                    json.loads(field_value)  # Try to parse JSON
                except json.JSONDecodeError:
                    errors[field_name] = 'Invalid JSON value. Field Value: {field_value}'

        # ForeignKey fields
        if isinstance(field, ForeignKey):
            if field_value is not None:
                related_model = field.related_model
                if field_name == 'plant_cell_wall_component':
                    if not related_model.objects.filter(chebi__chebi_id=field_value).exists() or \
                        related_model.objects.filter(cellwallcomp_name=field_value).exists():
                        errors[field_name] = f'Invalid reference for {field_name}. Field Value: {field_value}' 
                elif field_name == 'gene':
                    if not related_model.objects.filter(gene_name=field_value).exists() or related_model.objects.filter(gene_id=field_value).exists():
                        warnings[field_name] = f'Considering "{field_value}" as a new gene in the database'
                elif field_name == 'plant_trait':
                    if not related_model.objects.filter(name=field_value).exists() or related_model.objects.filter(to__to_id=field_value).exists() or \
                        TOTerm.objects.filter(to_id=field_value):
                        errors[field_name] = f'Invalid reference for {field_name}. Field Value: {field_value}' 
                elif field_name == 'species':
                    if not related_model.objects.filter(scientific_name=field_value).exists():
                        errors[field_name] = f'Invalid reference for {field_name}. Field Value: {field_value}'
                elif field_name == 'experiment_species':
                    if not related_model.objects.filter(scientific_name=field_value).exists():
                        warnings[field_name] = f'Considering "{field_value}" a new species that does not have a corresponding record.'
                        errors[field_name] = f'Invalid reference for {field_name}. Field Value: {field_value}'
                elif field_name == 'literature':
                    if field_value.startswith('10'):
                        if not related_model.objects.filter(doi=field_value).exists():
                            warnings[field_name] = f'Considering "{field_value}" a new DOI that does not have a corresponding record.'
                    else:
                        errors[field_name] = f'Invalid DOI reference for {field_name}. DOI should start with "10". Field Value: {field_value}'
                else:
                    if not related_model.objects.filter(pk=field_value).exists():
                        errors[field_name] = f'Invalid reference for {field_name}.'

        # ManyToMany fields
        elif isinstance(field, ManyToManyField):
            if field_value is not None:
                field_value=field_value.split(", ")
                if not isinstance(field_value, list):
                    errors[field_name] = f'Invalid format for {field_name} field. Expected a list. \
                                            Your data should be like "ECO:0001050, ECO:0007045, Klason method"'
                else:
                    related_model = field.related_model
                    if field_name == 'plant_component':
                        for item in field_value:
                            if item.startswith('PO:'):
                                if not related_model.objects.filter(po__po_id=item).exists() and not PlantOntologyTerm.objects.filter(po_id=item):
                                    errors[field_name] = f'Invalid PO term reference in {item}. Field Value: {field_value}'
                            else:
                                if not related_model.objects.filter(name=item).exists():
                                     errors[field_name] = f'Invalid reference in {item}. Field Value: {field_value}'
                    elif field_name == 'experiment':
                        for item in field_value:
                            if item.startswith('ECO:'):
                                if not related_model.objects.filter(eco_term__eco_id=item).exists() and not ECOTerm.objects.filter(eco_id=item):
                                    errors[field_name] = f'Invalid ECO term reference in {item}. Field Value: {field_value}'
                            else:
                                if not related_model.objects.filter(experiment_name=item).exists():
                                    warnings[field_name] = f'Considering "{item}" a new experiment name that does not have a corresponding ECO term.'
                                    errors[field_name] = f'Invalid reference for {field_name}. Field Value: {item}'
                    else:
                        for item in field_value:
                            if not related_model.objects.filter(pk=item).exists():
                                errors[field_name] = f'Invalid reference in {item}. Field Value: {field_value}'

    return not bool(errors), errors, warnings

def get_or_create_gene(gene_data):
    try:
        # Try to retrieve the gene by gene_id
        gene = Gene.objects.get(gene_id=gene_data.get('gene_id'))
    except Gene.DoesNotExist:
        try:
            # If not found by gene_id, try to retrieve by gene_name
            gene = Gene.objects.get(gene_name=gene_data.get('gene_name'))
        except Gene.DoesNotExist:
            # If not found by either, create a new gene
            species = Species.objects.get(scientific_name=gene_data.get('gene_species'))
            gene = Gene.objects.create(
                gene_id=gene_data.get('gene_id'),
                gene_name=gene_data.get('gene_name'),
                description=gene_data.get('gene_description'),
                species=species,
                species_variety=gene_data.get('species_variety')
            )
    return gene


def get_or_create_experiment(exp_data):
    literature = Literature.objects.get(doi=exp_data.get('literature'))
    experiment, created = Experiment.objects.get_or_create(
        experiment_name=exp_data.get('experiment_name'),
        defaults={
            'experiment_category': exp_data.get('experiment_category'),
            'description': exp_data.get('description'),
            'peco_term': PECOTerm.objects.get(peco_id=exp_data.get('peco_term')),
            'eco_term': ECOTerm.objects.get(eco_id=exp_data.get('eco_term')),
            'literature': literature,
        }
    )
    return experiment

def get_or_create_species(species_data):
    species, created = Species.objects.get_or_create(
        scientific_name=species_data.get('scientific_name'),
        defaults={
            'species_code': species_data.get('species_code'),
            'taxid': species_data.get('taxid'),
            'common_name': species_data.get('common_name'),
            'family': species_data.get('family'),
            'clade': species_data.get('clade'),
            'photosystem': species_data.get('photosystem'),
        }
    )
    return species

@transaction.atomic
def create_biomass_gene_experiment_assoc(data):
    for record in data['Biomass_gene_association_data']:
        species = get_or_create_species({'scientific_name': record.get('species')})
        gene = get_or_create_gene(record)
        experiment = get_or_create_experiment({'experiment_name': record.get('experiment'), 'literature': record.get('literature')})

        BiomassGeneExperimentAssoc.objects.create(
            experiment_species=species,
            gene=gene,
            gene_expression=record.get('gene_expression'),
            effect_on_plant_cell_wall_component=record.get('effect_on_plant_cell_wall_component'),
            literature=Literature.objects.get(doi=record.get('literature')),
            experiment=experiment,
        )
    return
