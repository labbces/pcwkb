import pandas as pd
from django.db import transaction
from pcwkb_core.models.functional_annotation.computational.annotation_method import AnnotationMethod
from pcwkb_core.models.functional_annotation.computational.cazyme import CAZyme, CAZymeProteinAssociation
from pcwkb_core.models.molecular_components.genetic.proteins import Protein

# Dictionary mapping CAZyme family prefixes to their classes
cazyme_class_mapping = {
    'GH': 'Glycoside Hydrolase',
    'GT': 'Glycosyltransferase',
    'PL': 'Polysaccharide Lyase',
    'CE': 'Carbohydrate Esterase',
    'CBM': 'Carbohydrate-Binding Module',
    'AA': 'Auxiliary Activities',
}

def get_cazyme_class(family_name):
    # Extract the prefix (e.g., 'GH' from 'GH5_7')
    family_name = family_name.replace('.hmm', '')
    prefix = ''.join([char for char in family_name if not char.isdigit() and char != '_'])
    return cazyme_class_mapping.get(prefix, 'Unknown')  # Default to 'Unknown' if not found

def import_cazyme_hmmer_data(file_path):
    # Load the CAZyme HMMER data from the file
    df = pd.read_csv(file_path, delimiter='\t', header=None)
    
    # Assign column names
    df.columns = ['CAZyme Family', 'HMM Length', 'Protein ID', 'Query Length', 'E-Value',
                  'HMM Start', 'HMM End', 'Query Start', 'Query End', 'Accuracy']
    
    print("First rows of the DataFrame:")
    print(df.head())
    
    # Retrieve or create the annotation method for HMMER
    annotation_method, created = AnnotationMethod.objects.get_or_create(
        software='HMMER',
        software_version='3.3',
        literature=None  # Adjust this if literature information is available
    )
    
    # Use a database transaction to ensure data integrity
    with transaction.atomic():
        for index, row in df.iterrows():
            family_name = row['CAZyme Family']
            protein_id = row['Protein ID'].strip()
            
            try:
                # Fetch the Protein instance from the database
                protein = Protein.objects.get(protein_id=protein_id)
            except Protein.DoesNotExist:
                print(f"Protein {protein_id} not found in the database.")
                continue
            
            # Get or create the CAZyme instance with the correct class
            cazyme_class = get_cazyme_class(family_name)
            cazyme, created = CAZyme.objects.get_or_create(
                family=family_name,
                defaults={
                    'cazyme_class': cazyme_class,
                    'putative_activities': 'Unknown'  # Adjust this field as needed
                }
            )
            
            if not CAZymeProteinAssociation.objects.filter(
                annotation_method=annotation_method,
                protein=protein,
                cazyme=cazyme
            ):
            # Create the CAZymeProteinAssociation
                CAZymeProteinAssociation.objects.create(
                    annotation_method=annotation_method,
                    protein=protein,
                    cazyme=cazyme
                )
                print(f"Association created for Protein {protein.protein_id} with CAZyme {cazyme.family} from {cazyme.cazyme_class}.")
            else:
                print(f"Association for Protein {protein.protein_id} with CAZyme {cazyme.family} already exists.")