from django import forms


class DataSubmissionForm(forms.Form):
    """ Class were the data submitted by users can be stored for further evalluation

    The fields receive only the title of the said submission and a sheet file (.xlsx or .xml) were all the informations about the gene will be received.
    """
    title = forms.CharField(max_length=50)
    #input_file = forms.FileField()


class SpeciesSubmissionForm(forms.Form):
    """ Class were a new species submitted by users can be stored

    The fields from TaxID and plant image are optional, since not necessarily this information will be avaliable. However, the plant name, description and source are required, since they are essential for curation purposes.
    """
    taxid = forms.IntegerField(label="Plant TaxID")
    plant_name: forms.CharField(label="Plant's scientific name", required=True)
    plant_image = forms.ImageField(label="Plant image")
    plant_image_source = forms.URLField(label="Image Source URL")
    description = forms.CharField(label="Plant description", max_length=200, required=True)