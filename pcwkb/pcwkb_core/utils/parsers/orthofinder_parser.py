from pcwkb_core.models.molecular_components.relationships.orthogroups import Orthogroup, OrthogroupMethods
from pcwkb_core.models.molecular_components.relationships.protein_orthogroup import ProteinOrthogroup
from pcwkb_core.models.molecular_components.genetic.proteins import Protein
import tempfile
import zipfile
import os
import gzip


class OrthogroupParser:
    def __init__(self):
        self.orthogroups = {}

    def read_orthofinder(self, orthofinder_file, compressed=False):
        if compressed:
            f = gzip.open(orthofinder_file, "rt")
        else:
            f = open(orthofinder_file, "r")

        for line in f:
            line = line.rstrip()
            og_id, polypep = line.split(": ")
            polypep_list = polypep.split(" ")

            self.orthogroups[og_id] = polypep_list

        print(og_id, self.orthogroups[og_id])
        f.close()

    @staticmethod
    def add_from_orthofinder(orthofinder_file, og_method_id, compressed=False):

        try:
            og_method = OrthogroupMethods.objects.get(id=og_method_id)
        except Exception as e:
            return f"Orthogroup Methods identifier does not exists, please inform a existing identifier || {e}"

        og_data = OrthogroupParser()
        og_data.read_orthofinder(orthofinder_file, compressed)

        for i, og in enumerate(sorted(og_data.orthogroups.keys()), start=1):
            if not Orthogroup.objects.filter(orthogroup_id=og, og_method=og_method):
                Orthogroup.objects.create(orthogroup_id=og,
                                          og_method=og_method
                                          )
            else:
                print(f"orthogroup_id: {og} with the method: {og_method} already exists")
                
            print(f"{i} orthogroup object  parsered to the database")

        for p in Protein.objects.all():
            for i, og in enumerate(sorted(og_data.orthogroups.keys()), start=1):
                if p.protein_name in og_data.orthogroups[og]:
                    print(p.protein_name, og)
                    if not ProteinOrthogroup.objects.filter(orthogroup=Orthogroup.objects.get(orthogroup_id=og), protein=p):
                        ProteinOrthogroup.objects.create(orthogroup=Orthogroup.objects.get(orthogroup_id=og),
                                                      protein=p
                                                      )
                    else:
                        print(
                            f"protein: {p} in orthogroup_id: {og} already exists")
                        
                    print(f"{i} proteins object parsered to the database")

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

    @staticmethod
    def import_trees_zipped_folder(tree_data_folder, og_method_id):
        count = 1
        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                with zipfile.ZipFile(tree_data_folder, 'r') as zip_ref:
                    zip_ref.extractall(tmp_dir)

                for file_name in os.listdir(tmp_dir):
                    og_id = file_name.split("_")[0]
                    file_path = os.path.join(tmp_dir, file_name)

                    lines = []
                    with open(file_path, "r") as f:
                        for line in f:
                            line = line.strip()
                            lines.append(line)

                    tree_data = '\n'.join(lines)

                    if Orthogroup.objects.filter(orthogroup_id=og_id, og_method=og_method_id):
                        og = Orthogroup.objects.get(orthogroup_id=og_id, og_method=og_method_id)
                        og.tree = tree_data
                        og.save()

                        print(count)
                        count=count+1

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            print("Import completed")
