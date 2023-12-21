from django import forms


class DataSubmissionForm(forms.Form):
    """ Class to submit 


    """
    title = forms.CharField(max_length=50)
    #input_file = forms.FileField()


class SpeciesSubmissionForm(forms.Form):
    """
    """
    taxid = forms.IntegerField(label="Plant TaxID")
    plant_image = forms.ImageField(label="Plant image")
    plant_image_source = forms.URLField(label="Image Source URL", required=True)
    description = forms.CharField(label="Plant description", max_length=200)