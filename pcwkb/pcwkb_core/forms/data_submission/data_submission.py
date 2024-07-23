from django import forms
import pandas as pd
import json

from pcwkb_core.models.functional_annotation.experimental.experiment import Experiment
from pcwkb_core.models.literature.literature import Literature
from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.functional_annotation.experimental.relationships.biomass_gene_experiment_assoc import BiomassGeneExperimentAssoc
from pcwkb_core.utils.data_submission import validate_model_data

class DataSubmissionForm(forms.Form):
    title = forms.CharField(max_length=50)
    input_file = forms.FileField()

    def clean_input_file(self): #this is called when use forms.is_valid()
        uploaded_file = self.cleaned_data['input_file']
        
        # Check if the file has the correct extension
        if not uploaded_file.name.endswith(('.xlsx', '.xls')):
            raise forms.ValidationError('The file must have the extension .xlsx, .xls')
        
        # Check if the .xlsx or .xls file is valid
        try:
            df_dict = pd.read_excel(uploaded_file, sheet_name=None)
        except Exception as e:
            raise forms.ValidationError(f'Error loading the .xlsx file: {str(e)}')

        # Define required sheets and columns
        required_sheets = ['biomass_gene_association_data', 'experiment_data', 'species_data']
        required_columns = {
            'biomass_gene_association_data': ['experiment_species', 'gene_name', 'gene_id', 'gene_description', 'gene_species', 'gene_genetic_condition', 'effect_on_plant_cell_wall_component', 'plant_cell_wall_component', 'literature', 'plant_trait', 'experiment', 'plant_component'],
            'experiment_data': ['experiment_name', 'experiment_category', 'description', 'peco_term', 'eco_term', 'literature'],
            'species_data': ['species_code', 'taxid', 'scientific_name', 'common_name', 'family', 'clade', 'photosystem']
        }

        # Check if all required sheets are present
        for sheet in required_sheets:
            if sheet not in df_dict:
                raise forms.ValidationError(f"Missing sheet: {sheet}")

        # Check if all required columns are present in each sheet
        for sheet, columns in required_columns.items():
            if sheet in df_dict:
                missing_columns = [col for col in columns if col not in df_dict[sheet].columns]
                if missing_columns:
                    raise forms.ValidationError(f"Missing columns in {sheet}: {', '.join(missing_columns)}")
        
        return uploaded_file

    def process_file(self): #this is called when use forms.process_file
        uploaded_file = self.cleaned_data['input_file']
        data = {}
        
        df_dict = pd.read_excel(uploaded_file, sheet_name=['biomass_gene_association_data', 'experiment_data', 'species_data'])
        for sheet, df in df_dict.items():
            data[sheet] = df.to_dict(orient='records')

        return data
    

    def validate_data(self, data):
        errors = {}
        warnings = {
        'species_data': [],
        'experiment_data': [],
        'gene_data': [],
        'biomass_gene_association_data': []
        }

        # Extract specific data for validation
        gene_data = data.get('biomass_gene_association_data', [])
        species_data = data.get('species_data', [])
        experiment_data = data.get('experiment_data', [])

        # Validate species_data
        for record in species_data:
            is_valid, field_errors, field_warnings = validate_model_data(record, Species)
            if not is_valid:
                errors['species_data'] = field_errors
            warnings['species_data'].extend(field_warnings.values())

        # Validate experiment_data
        for record in experiment_data:
            is_valid, field_errors, field_warnings = validate_model_data(record, Experiment)
            if not is_valid:
                errors['experiment_data'] = field_errors
            warnings['experiment_data'].extend(field_warnings.values())

        # Validate Gene data
        for record in gene_data:
            gene_data_for_validation = {
                'gene_name': record.get('gene_name'),
                'gene_id': record.get('gene_id'),
                'description': record.get('gene_description'),
                'species': record.get('gene_species'),
            }
            is_valid, field_errors, field_warnings = validate_model_data(gene_data_for_validation, Gene)
            if not is_valid:
                errors['gene_data'] = field_errors
            warnings['gene_data'].extend(field_warnings.values())

        # Validate BiomassGeneExperimentAssoc data
        for record in gene_data:
            assoc_data_for_validation = {
                'experiment_species': record.get('experiment_species'),
                'gene': record.get('gene_name') or record.get('gene_id'),
                'gene_expression': record.get('gene_genetic_condition'),
                'effect_on_plant_cell_wall_component': record.get('effect_on_plant_cell_wall_component'),
                'plant_cell_wall_component': record.get('plant_cell_wall_component'),
                'literature': record.get('literature'),
                'plant_component': record.get('plant_component'),
                'plant_trait': record.get('plant_trait'),
                'experiment': record.get('experiment'),
            }
            is_valid, field_errors, field_warnings = validate_model_data(assoc_data_for_validation, BiomassGeneExperimentAssoc)
            if not is_valid:
                errors['biomass_gene_association_data'] = field_errors
            warnings['biomass_gene_association_data'].extend(field_warnings.values())
        
        print(warnings)

        for key in warnings:
            warnings[key] = list(set(warnings[key]))
        
        filtered_warnings = {}
        for key, value in warnings.items():
            if value:
                filtered_warnings[key] = value

        warnings = filtered_warnings

        return errors, warnings


class SpeciesSubmissionForm(forms.Form):
    """ Class were a new species submitted by users can be stored

    The fields from TaxID and plant image are optional, since not necessarily this information will be avaliable. However, the plant name, description and source are required, since they are essential for curation purposes.
    """
    taxid = forms.IntegerField(label="Plant TaxID")
    plant_name = forms.CharField(label="Plant's scientific name", required=True)
    plant_image = forms.ImageField(label="Plant image")
    plant_image_source = forms.URLField(label="Image Source URL")
    description = forms.CharField(label="Plant description", max_length=200, required=True)

class ExperimentForm(forms.ModelForm):
    class Meta:
        model = BiomassGeneExperimentAssoc
        fields = "__all__"