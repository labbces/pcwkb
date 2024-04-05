from django.db import models

class OrthogroupMethods(models.Model):
    tool = models.CharField('Tool used to search for orthogroups', max_length=50)
    version = models.CharField('Tool version', max_length=50)
    run = models.CharField('Run number (if it is the only one type 1)',max_length=50)
    personal_identifier = models.CharField('Personal researcher identifier to easy find the method you insert (optional)', max_length=10, null=True, blank=True)
    description = models.CharField('Description about the process', max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.tool}.v{self.version}.{self.run}_{self.personal_identifier}"

class Orthogroup(models.Model):
    orthogroup_id = models.CharField(max_length=50)
    og_method = models.ForeignKey(OrthogroupMethods, on_delete=models.CASCADE)
    tree = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.orthogroup_id}.{self.og_method}"
    
    
