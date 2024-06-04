from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.molecular_components.genetic.genes import Gene

import gzip

class GFF3Parser:
    def __init__(self):
        pass

    def parse(self, gff3_file, compressed=False):
        genes = []
        if compressed:
            f = gzip.open(gff3_file, "rt")
        else:
            f = open(gff3_file, "r")
            for line in f:
                if not line.startswith('#'):
                    fields = line.strip().split('\t')
                    if fields[2] == 'gene':
                        attributes = self.parse_attributes(fields[8])
                        gene_data = {
                                    'gene_id': attributes.get('ID', ''),
                                    'gene_name': attributes.get('Name', ''),
                                    'source': fields[1]
                                    }
                        genes.append(gene_data)
            print(genes)

        f.close()
        
        return genes
        
        

    def parse_attributes(self, attribute_string):
        attributes = {}
        for attribute in attribute_string.split(';'):
            if attribute:
                key, value = attribute.split('=')
                attributes[key] = value
        return attributes

    @staticmethod
    def add_from_gff3(gff3_file, species_id, compressed=False):
        i = 1
        parser = GFF3Parser()
        genes = parser.parse(gff3_file, compressed)
        for gene in genes:
            print(i)
#            print(Species.objects.get(id=species_id).scientific_name,
#                  Species.objects.get(id=species_id).id)
#            print(gene, species_id)

            if not Gene.objects.filter(gene_name=gene['gene_name'],
                                       gene_id=gene['gene_id'],
                                    original_db=gene['source'],
                                    species=Species.objects.get(id=species_id),
                                    source="gff3"
                                    ):
                g = Gene.objects.create(gene_name=gene['gene_name'],
                                        gene_id=gene['gene_id'],
                                    original_db=gene['source'],
                                    species=Species.objects.get(id=species_id),
                                    source="gff3"
                                    )
            else:
                print("Já existe")
            i=i+1
        return g
