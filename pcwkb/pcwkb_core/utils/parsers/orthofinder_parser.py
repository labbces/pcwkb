from pcwkb_core.models.molecular_components.relationships.orthogroups import Orthogroup,OrthogroupMethods
from pcwkb_core.models.molecular_components.relationships.protein_orthogroup import ProteinOrthogroup
from pcwkb_core.models.molecular_components.genetic.proteins import Protein

import gzip

class OrthogroupParser:
    def __init__(self):
        self.orthogroups = {}
    
    def read_orthofinder(self,orthofinder_file,compressed=False):
        if compressed:
            f = gzip.open(orthofinder_file, "rt")
        else:
            f = open(orthofinder_file, "r")

        for line in f:
            line = line.rstrip()
            og_id,polypep = line.split(": ")
            polypep_list = polypep.split(" ")

            self.orthogroups[og_id]=polypep_list
        
        print(og_id,self.orthogroups[og_id])
        f.close()
        
    @staticmethod
    def add_from_orthofinder(orthofinder_file,og_method_id,compressed=False):

        i=1

        try:
            og_method = OrthogroupMethods.objects.get(id=og_method_id)
        except Exception as e:
            return f"Orthogroup Methods identifier does not exists, please inform a existing identifier || {e}"


        og_data=OrthogroupParser()
        og_data.read_orthofinder(orthofinder_file, compressed)

        for og in sorted(og_data.orthogroups.keys()):
            if not Orthogroup.objects.filter(orthogroup_id = og, og_method = og_method):
                 Orthogroup.objects.create(orthogroup_id = og,
                                           og_method = og_method
                                           )
            else:
                print(f"orthogroup_id: {og} with the method: {og_method} already exists")
            print(i)
            i=i+1

        i=1

        for p in Protein.objects.all():
            for og in sorted(og_data.orthogroups.keys()):
                if p.protein_name in og_data.orthogroups[og]:
                    print(p.protein_name, og)
                    if not GeneOrthogroup.objects.filter(orthogroup=Orthogroup.objects.get(orthogroup_id=og),protein=p):
                        GeneOrthogroup.objects.create(orthogroup=Orthogroup.objects.get(orthogroup_id=og),
                                                      protein=p
                                                      )

#        for p in Protein.objects.all():
#            for og in Orthogroup.objects.all():
#                if p.protein_name in og_data.orthogroups[og.orthogroup_id]:
#                    print(p.protein_name, og)
#                    if not ProteinOrthogroup.objects.filter(orthogroup=og,protein=p):
#                        ProteinOrthogroup.objects.create(orthogroup=og,
#                                                      protein=p
#                                                     )
#                    else:
#                        print(f"protein: {p} in orthogroup_id: {og} already exists")
#                    print(i)
#                    i=i+1

        return
