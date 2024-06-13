from django import forms
import xml.etree.ElementTree as ET
import pandas as pd
import json
from pcwkb_core.models.functional_annotation.experimental.relationships.biomass_gene_experiment_assoc import BiomassGeneExperimentAssoc

class DataSubmissionForm(forms.Form):
    title = forms.CharField(max_length=50)
    input_file = forms.FileField()

    def clean_input_file(self): #this is called when use forms.is_valid()
        uploaded_file = self.cleaned_data['input_file']
        
        # Check if the file has the correct extension
        if not uploaded_file.name.endswith(('.xlsx', '.xls', '.xml')):
            raise forms.ValidationError('The file must have the extension .xlsx, .xls, or .xml.')
        
        # Check if the .xlsx or .xls file is valid
        if uploaded_file.name.endswith(('.xlsx', '.xls')):
            try:
                df = pd.read_excel(uploaded_file)
            except Exception as e:
                raise forms.ValidationError('Error loading the .xlsx file: {}'.format(str(e)))
            
            fields = ['species', 'po', 'chebi', 'experiment', 'literature', 'gene', 'to', 'gene_expression', 'effect_on_plant_cell_wall_component']

            missing_fields=[]

            for field in fields:
                if field not in df.columns:
                    missing_fields.append(field)

            if not missing_fields:
                print("All required columns are present.")
            else:
                 raise forms.ValidationError(f"Missing columns")
        
        # Check if the .xml file is valid
        if uploaded_file.name.endswith('.xml'):
            try:
                ET.parse(uploaded_file)
            except ET.ParseError as e:
                raise forms.ValidationError('Error parsing the .xml file: {}'.format(str(e)))
        
        return uploaded_file

    def process_file(self): #this is called when use forms.process_file
        uploaded_file = self.cleaned_data['input_file']
        data = {}

        if uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
            data = df.to_dict(orient='records')
      
        elif uploaded_file.name.endswith('.xml'):
            tree = ET.parse(uploaded_file)
            root = tree.getroot()

            for child in root:
                row_data = {elem.tag: elem.text for elem in child}
                data[len(data) + 1] = row_data
        
        return json.dumps(data)


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
        fields = ['experiment_species', 'po', 'chebi', 'experiment', 'literature', 'gene', 'to', 'effect_on_plant_cell_wall_component']
        labels = {
            'to': 'Trait Ontology',
            'po': 'Plant Ontology',
            'chebi': 'Chemical Component (Cell Wall Component)',
        }