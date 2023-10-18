from django.db import models
from Bio import Entrez


class Species(models.Model):
    species_code = models.CharField(max_length=10)
    scientific_name = models.CharField(max_length=50)
    common_name = models.CharField(max_length=30)
    family = models.CharField(max_length=30)
    clade = models.CharField(max_length=50)
    photosystem = models.CharField(max_length=10)

    def __str__(self):
        return self.species_name

    def insert_species_ncbi_taxid(taxid):
        ''' Inserts Species based on TaxID


        '''

        Entrez.email = "bih.08.vgsul@gmail.com"     # Always tell NCBI who you are
        handle = Entrez.efetch(db="taxonomy", id=taxid, retmode="xml")

        records = Entrez.parse(handle)

        for tax_item in records:
            # print(tax_item['TaxId'],tax_item['ScientificName'],tax_item['OtherNames'], tax_item['Lineage'])
            lineage_list = tax_item['Lineage'].split(';')
            


