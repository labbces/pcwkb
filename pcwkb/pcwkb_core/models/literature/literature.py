import datetime
from django.db import models
from crossref.restful import Works #ver se pega o resumo

class Literature(models.Model):

    doi = models.CharField(max_length=50, unique=True, null=False)
    author_name = models.CharField(max_length=50, null=False, blank=True)
    title = models.TextField(null=False, blank=True)
    public_year = models.DateField(null=False, blank=True)
    reference_type = models.CharField(max_length=50, null=True, blank=True)
    journal = models.CharField(max_length=100, null=True, blank=True)
    abstract = models.TextField(null=True, blank=True)
    pmid = models.CharField(max_length=50, null=True, blank=True)


    # source = models.CharField(max_length=50, null=False, blank=True)

    def __str__(self):
        return self.doi

    def get_lit_info(doi):
        """ Gets literature information using only the DOI identifier whit crossref library.

        Verify if DOI already exists in DB, if not, collect data and store in the fields from Literature class.
        """
        try:
            literature = Literature.objects.get(doi=doi)      #Checks if the literature exists
            return literature
        except Literature.DoesNotExist:
            works = Works()
            literature_info = works.doi(doi)
            
            if 'family' in literature_info['author'][0].keys():
                author_name = literature_info['author'][0]['family']
            else:
                author_name = literature_info['author'][0]['name']

            title = literature_info['title'][0]

            if 'published-print' in literature_info.keys():
                public_year = str(literature_info['published-print']['date-parts'][0][0])+"-01-01"
                print(str(literature_info['published-print']['date-parts']))
            elif 'published-online' in literature_info.keys():
                public_year = str(literature_info['published-online']['date-parts'][0][0])+"-01-01"
                print(str(literature_info['published-online']['date-parts']))
            else:
                public_year = str(literature_info['issued']['date-parts'][0][0])+"-01-01"
                print(str(literature_info['issued']['date-parts']))
            
            new_literature = Literature.objects.create(doi=doi,                           #saves the new literature
                                                        author_name=author_name, 
                                                        title=title,
                                                        public_year=public_year)
            return new_literature



    