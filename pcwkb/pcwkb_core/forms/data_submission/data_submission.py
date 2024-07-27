from django import forms
import pandas as pd

from pcwkb_core.models.functional_annotation.experimental.experiment import Experiment
from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.literature.literature import Literature
from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.functional_annotation.experimental.relationships.biomass_gene_experiment_assoc import BiomassGeneExperimentAssoc
from pcwkb_core.utils.data_submission import validate_model_data

class DataSubmissionForm(forms.Form):
    title = forms.CharField(max_length=50)
    input_file = forms.FileField()
    type_of_data = forms.ChoiceField(
        choices=[
            ('species_data', 'Species Data'),
            ('experiment_data', 'Experiment Data'),
            ('biomass_gene_association_data', 'Biomass Gene Association Data')
        ],        required=True,
        widget=forms.RadioSelect
    )

    def clean(self):
        cleaned_data = super().clean()
        type_of_data = cleaned_data.get('type_of_data')
        uploaded_file = cleaned_data.get('input_file')

        if not uploaded_file:
            raise forms.ValidationError("Input file is required.")
        
        # Ensure `type_of_data` is present and valid
        if not type_of_data:
            raise forms.ValidationError("Type of data is required.")

        # Validation logic specific to type_of_data
        if type_of_data not in ['species_data', 'experiment_data', 'biomass_gene_association_data']:
            raise forms.ValidationError(f"Invalid type of data: {type_of_data}")
        
        #Validate data sheet:
        # Check if the sheet has non-empty rows based on the type_of_data
        df_dict = pd.read_excel(uploaded_file, sheet_name=None)
        for sheet in df_dict:
            if type_of_data == sheet and df_dict[sheet].empty:
                print("empty")
                print(f"The sheet {sheet} is empty or only contains empty rows. Please ensure that it has non-empty data.")
                raise forms.ValidationError(f"The sheet {sheet} is empty or only contains empty rows. Please ensure that it has non-empty data.")
            if type_of_data != sheet and not df_dict[sheet].empty and (sheet == 'species_data' or sheet == 'experiment_data' or sheet == 'biomass_gene_association_data'):
                raise forms.ValidationError(f"The sheet {sheet} is not empty. Please select Biomass Gene Association Data if you have all the sheets filled. \
                                            (Now it is not available to send experiment data and species data at the same time)")

        return cleaned_data


    def clean_input_file(self):
        """
        Checks if the uploaded file has the correct extension and data
        """
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
        row_limit=50

        # Check if at least one required sheet has non-empty data
        non_empty_sheets = [sheet for sheet in required_sheets if not df_dict.get(sheet, pd.DataFrame()).empty]
        if not non_empty_sheets:
            raise forms.ValidationError("All required sheets are empty. Please ensure that at least one sheet contains data.")

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
                
                # Check if the sheet exceeds the row limit
                if len(df_dict[sheet]) > row_limit:
                    raise forms.ValidationError(f"The sheet {sheet} exceeds the row limit of {row_limit} rows. Please reduce the number of rows.")
                
               
        return uploaded_file


    def process_file(self):
        """
        Process the uploaded file and returns a dict
        """

        uploaded_file = self.cleaned_data['input_file']
        data = {}
        
        df_dict = pd.read_excel(uploaded_file, sheet_name=['biomass_gene_association_data', 'experiment_data', 'species_data'])
        for sheet, df in df_dict.items():
            data[sheet] = df.to_dict(orient='records')

        return data
    
    @staticmethod
    def process_warnings_or_errors(data_dict):
        """
        Process the dictionary to aggregate values into lists and filter out empty lists.
        """
        aggregated_data = {}
        
        for key in data_dict:
            aggregated_data[key] = {}
            for sub_key, values in data_dict[key].items():
                if isinstance(values, list):
                    aggregated_data[key][sub_key] = list(set(values))
                else:
                    aggregated_data[key][sub_key] = values
        
        # Remove keys with empty lists
        filtered_data = {key: value for key, value in aggregated_data.items() if value}
        
        return filtered_data

    def validate_data(self, data):
        """
        Validate data and categorize errors and warnings into separate dictionaries.
        """
        errors = {
            'species_data': {},
            'experiment_data': {},
            'gene_data': {},
            'biomass_gene_association_data': {}
        }
        warnings = {
            'species_data': {},
            'experiment_data': {},
            'gene_data': {},
            'biomass_gene_association_data': {}
        }

        # Extract specific data for validation
        gene_data = data.get('biomass_gene_association_data', [])
        species_data = data.get('species_data', [])
        experiment_data = data.get('experiment_data', [])

        def add_errors_and_warnings(validation_results, error_dict, warning_dict):
            for key, value in validation_results[0].items():
                if key not in error_dict:
                    error_dict[key] = []
                error_dict[key].append(value)
            for key, value in validation_results[1].items():
                if key not in warning_dict:
                    warning_dict[key] = []
                warning_dict[key].append(value)

        # Validate data based on selected choice
        validation_choice = self.cleaned_data.get('type_of_data')

        if validation_choice in ['species_data', 'biomass_gene_association_data']:
            # Validate species_data
            for record in species_data:
                is_valid, field_errors, field_warnings = validate_model_data(record, Species)
                add_errors_and_warnings((field_errors, field_warnings), errors['species_data'], warnings['species_data'])

        if validation_choice in ['experiment_data', 'biomass_gene_association_data']:
            # Validate experiment_data
            for record in experiment_data:
                is_valid, field_errors, field_warnings = validate_model_data(record, Experiment)
                add_errors_and_warnings((field_errors, field_warnings), errors['experiment_data'], warnings['experiment_data'])

        if validation_choice in ['biomass_gene_association_data']:
            # Validate Gene data
            for record in gene_data:
                gene_data_for_validation = {
                    'gene_name': record.get('gene_name'),
                    'gene_id': record.get('gene_id'),
                    'description': record.get('gene_description'),
                    'species': record.get('gene_species'),
                }
                is_valid, field_errors, field_warnings = validate_model_data(gene_data_for_validation, Gene)
                add_errors_and_warnings((field_errors, field_warnings), errors['gene_data'], warnings['gene_data'])

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
                add_errors_and_warnings((field_errors, field_warnings), errors['biomass_gene_association_data'], warnings['biomass_gene_association_data'])

        # Deduplicate errors and warnings
        errors = DataSubmissionForm.process_warnings_or_errors(errors)
        warnings = DataSubmissionForm.process_warnings_or_errors(warnings)

        # Check and remove errors if related data exists
        if errors and errors['biomass_gene_association_data']:
            for field_name in ['experiment_species', 'gene', 'experiment']:
                if field_name in errors['biomass_gene_association_data']:
                    field_errors = errors['biomass_gene_association_data'].get(field_name, [])
                    if field_errors:
                        # Extract the list of errors for the field
                        field_errors_list = field_errors

                        # Extract the list of valid values from related data
                        if field_name == 'experiment_species':
                            valid_values = [record.get('scientific_name') for record in species_data if record.get('scientific_name')] + \
                                        [record.get('common_name') for record in species_data if record.get('common_name')] + \
                                        [record.get('species_code') for record in species_data if record.get('species_code')]
                        elif field_name == 'gene':
                            valid_values = [record.get('gene_name') for record in gene_data if record.get('gene_name')] + \
                                        [record.get('gene_id') for record in gene_data if record.get('gene_id')]
                        elif field_name == 'experiment':
                            valid_values = [record.get('experiment_name') for record in experiment_data if record.get('experiment_name')]
                        else:
                            valid_values = []
                        

                        # Filter out errors that are valid based on the related data
                        new_field_errors = [error for error in field_errors_list if error.split(': ')[-1].strip().strip('"') not in valid_values]

                        # Update the error dictionary with the filtered errors
                        errors['biomass_gene_association_data'][field_name] = new_field_errors
            
            # Collect keys to be removed
            keys_to_remove = [key for key in errors if all(not errors[key][sub_key] for sub_key in errors[key])]
            sub_keys_to_remove = [sub_key for key in errors for sub_key in errors[key] if not errors[key][sub_key]]

            # Remove collected keys
            for key in keys_to_remove:
                del errors[key]
            for sub_key in sub_keys_to_remove:
                for key in errors:
                    del errors[key][sub_key]
        
        print(errors, warnings, validation_choice)

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