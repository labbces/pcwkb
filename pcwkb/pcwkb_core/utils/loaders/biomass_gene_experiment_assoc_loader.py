import django
from pathlib import Path
import json
import os
import sys
from django.core.exceptions import ObjectDoesNotExist

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pcwkb.settings")
print((str(BASE_DIR)), "DJANGO_SETTINGS_MODULE:", os.environ.get("DJANGO_SETTINGS_MODULE"))
django.setup()

from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species
from pcwkb_core.models.ontologies.plant_related.po import PlantOntologyTerm
from pcwkb_core.models.ontologies.plant_related.to import TOTerm
from pcwkb_core.models.ontologies.molecular_related.chebi import ChEBI
from pcwkb_core.models.functional_annotation.experimental.experiment import Experiment
from pcwkb_core.models.literature.literature import Literature
from pcwkb_core.models.molecular_components.genetic.genes import Gene

def get_id(model, **fields):
    for field, value in fields.items():
        if value is not None:
            try:
                return model.objects.get(**{field: value}).id
            except ObjectDoesNotExist:
                continue
            except ValueError:
                continue
        else:
            continue

# Load the original JSON file
if len(sys.argv) != 2:
        print("Usage: python preprocess_data.py <json_file>")
        sys.exit(1)

json_data=sys.argv[1]

with open(json_data, 'r') as file:
    data = json.load(file)

processed_data = []

# Process each record
for record in data:
    fields = record['fields']

    # Fetch the IDs based on the readable names or IDs
    fields['experiment_species'] = get_id(Species, pk=fields.get('experiment_species'), species_code=fields.get('experiment_species'), scientific_name=fields.get('experiment_species'), taxid=fields.get('experiment_species'))
    fields['po'] = get_id(PlantOntologyTerm, pk=fields.get('po'), po_name=fields.get('po'), po_id=fields.get('po'))
    fields['chebi'] = get_id(ChEBI, pk=fields.get('chebi'), chebi_name=fields.get('chebi'), chebi_id=fields.get('chebi'))
    fields['experiment'] = [get_id(Experiment, experiment_name=value, pk=value, eco_term=value) for value in fields.get('experiment', [])]
    fields['literature'] = get_id(Literature, doi=fields.get('literature'), title=fields.get('literature'), pk=fields.get('literature'), pmid=fields.get('literature'))
    fields['gene'] = get_id(Gene, gene_name=fields.get('gene'), gene_id=fields.get('gene'), pk=fields.get('gene'))
    fields['to'] = get_id(TOTerm, to_name=fields.get('to'), to_id=fields.get('to'), pk=fields.get('to'))

    # Append the processed record
    processed_data.append(record)

print(processed_data)
# Save the processed data to a temporary JSON file
temp_json_path = 'processed_data.json'
with open(temp_json_path, 'w') as file:
    json.dump(processed_data, file, indent=2)

# Load the processed JSON data into the database using Django's loaddata
os.system(f'python manage.py loaddata {temp_json_path}')

# Clean up the temporary JSON file
os.remove(temp_json_path)
