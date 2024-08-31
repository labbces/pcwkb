from django.db import models

from pcwkb_core.models.literature.literature import Literature


class AnnotationMethod(models.Model):
    """ This class store the information about annotation methods.
    The methods annotation include the name of the referred method
    and its version, since thats an important information for 
    compatibility. This class also requires a related literature to
    verify the method used.
    """
    software = models.CharField('Software name', max_length=20)
    software_version = models.CharField('Software version', max_length=10)
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE,
                                   null=True, blank=True) #software literature
    
    def __str__(self):
        return f"{self.software}_{self.software_version}_{self.literature.doi}"
    