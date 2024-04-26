from django import forms
from openpyxl import load_workbook
from pcwkb_core.models.molecular_components.relationships.biomass_experiemnte_assoc import Experimentalevidenceplanttrait
import xml.etree.ElementTree as ET


class DataSubmissionForm(forms.Form):
    """ Class were the data submitted by users can be stored for further evalluation

    The fields receive only the title of the said submission and a sheet file (.xlsx or .xml) were all the informations about the gene will be received.
    """
    title = forms.CharField(max_length=50)
    input_file = forms.FileField()

    def clean_file(self):
        uploaded_file = self.cleaned_data['input_file']

        # Check if the file has the extension .xlsx
        if not uploaded_file.name.endswith(('.xlsx', '.xls')):
            raise forms.ValidationError('The file must have the extension .xlsx or .xls.')

        # Check if the .xlsx file is valid
        if uploaded_file.name.endswith('.xlsx'):
            try:
                load_workbook(uploaded_file)
            except Exception as e:
                raise forms.ValidationError('Error loading the .xlsx file: {}'.format(str(e)))

        # Check if the file has the extension .xml
        if not uploaded_file.name.endswith('.xml'):
            raise forms.ValidationError('The file must have the extension .xml.')

        # Check if the .xml file is valid
        if uploaded_file.name.endswith('.xml'):
            try:
                ET.parse(uploaded_file)
            except ET.ParseError as e:
                raise forms.ValidationError('Error parsing the .xml file: {}'.format(str(e)))


        return uploaded_file


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
        model = Experimentalevidenceplanttrait
        fields = '__all__'