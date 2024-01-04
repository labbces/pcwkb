from django.db import models
from Bio import Entrez


class Species(models.Model):
    """Receive Species information.
    
    This class stores information about a specie, such as its scientific 
    and common name, the description of the specie, the family and clade 
    where the specie is assigned and its photosystem type.  
    """
    species_code = models.CharField(max_length=10, null=False, blank=True)
    taxid = models.IntegerField()
    scientific_name = models.CharField(max_length=50, null=False, blank=True)
    common_name = models.CharField(max_length=30, null=True, blank=True)
    family = models.CharField(max_length=30, null=False, blank=True)
    clade = models.CharField(max_length=50, null=False, blank=True)
    photosystem = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.scientific_name

    def insert_species_ncbi_taxid(taxid):
        ''' Inserts Species based on TaxID.

        This function uses the Biopython library and  the TaxID from 
        NCBI to collect the information that will be used to fill the 
        species table in the database.
        '''

        Entrez.email = "pcwkb@gmail.com"     # Always tell NCBI who you are
        handle = Entrez.efetch(db="taxonomy", id=taxid, retmode="xml")

        records = Entrez.parse(handle)

        scientific_name = ''
        species_code = ''
        common_name = ''
        family = ''
        clade = ''
        photosystem = ''    

        for tax_item in records:

            scientific_name = tax_item['ScientificName']
            species_code = scientific_name.split(' ')[0][0] + scientific_name.split(' ')[1][0:2]

            db_species = Species.objects.filter(species_code=species_code).first()

            i = 0
            while db_species:
                i = i + 1
                species_code = species_code + str(i)
                db_species = Species.objects.filter(species_code=species_code).first()
            
            common_name = 'batata' #tax_item['OtherNames']
            family = 'Poaceae'
            clade = 'mmonocot'
            photosystem = 'C4'
    
        new_species = Species(scientific_name = scientific_name,
        taxid = taxid,
        species_code = species_code,
        common_name = common_name,
        family = family,
        clade = clade,
        photosystem = photosystem)

        return new_species
            


