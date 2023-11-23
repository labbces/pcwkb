from django.db import models
from crossref.restful import Works

class Literature(models.Model):

    doi = models.CharField(max_length=50, unique=True, null=False)
    author_name = models.CharField(max_length=50, null=False, blank=True)
    title = models.CharField(max_length=100, null=False, blank=True)
    public_year = models.DateField(null=False, blank=True)
    # source = models.CharField(max_length=50, null=False, blank=True)

    def __str__(self):
        return self.doi

    def get_lit_info(self, doi):

        print(doi,"\n\n\n\n\n\n\n\n")

        # verify if DOI already exists in DB, if not, collect data
        literature = Literature.objects.get(doi=doi)
        
        if literature is None:

            works = Works()
            literature_info = works.doi(doi)
            
            if 'family' in literature_info['author'][0].keys():
                author_name = literature_info['author'][0]['family']
            else:
                author_name = literature_info['author'][0]['name']

            title = literature_info['title']

            if 'published-print' in literature_info.keys():
                print(literature_info['published-print']['date-parts'])
                public_year = literature_info['published-print']['date-parts'][0][0]
            elif 'published-online' in literature_info.keys():
                print(literature_info['published-online']['date-parts'])
                public_year = literature_info['published-online']['date-parts'][0][0]
            else:
                print(literature_info['issued']['date-parts'])
                public_year = literature_info['issued']['date-parts'][0][0]
            
            new_literature = Literature(doi=doi,
                                        author_name=author_name, 
                                        title=title,
                                        public_year=public_year)
        return new_literature



    