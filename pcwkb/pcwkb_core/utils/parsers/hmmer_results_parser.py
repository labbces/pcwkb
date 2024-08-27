import pandas as pd
from pcwkb_core.models.functional_annotation.computational.annotation_method import AnnotationMethod
from pcwkb_core.models.functional_annotation.computational.transcriptional_regulation import TranscriptionalRegulatorFamily, GeneTFAssociation
from pcwkb_core.models.molecular_components.genetic.genes import Gene

def import_hmmer_data(file_path):

    df = pd.read_csv(file_path, delimiter='\t', header=None, skiprows=1)
    

    print("Primeiras linhas do DataFrame:")
    print(df.head())
    print("Número de colunas:", df.shape[1])
    
    df.columns = ['Gene', 'Family', 'Unnamed']
    

    print("DataFrame corrigido:")
    print(df.head())
    
    annotation_method, created = AnnotationMethod.objects.get_or_create(
        software='HMMER',
        software_version='3.3',
        literature=None
    )
    
    for index, row in df.iterrows():
        print(row)
        class_name = row['Family']
        family_name = row['Unnamed']
        
        try:
            # Divide o Gene ID em partes
            gene_parts = row['Gene'].split('.')
            
            # Inicializa o gene_id com a primeira parte
            gene_id = gene_parts[0]
            
            # Tenta concatenar até 4 partes no total
            for i in range(1, min(4, len(gene_parts))):
                gene_id += f".{gene_parts[i]}"
                try:
                    gene = Gene.objects.get(gene_id=gene_id)
                    break  # Sai do loop se encontrar o gene
                except Gene.DoesNotExist:
                    continue  # Continua a adicionar mais partes se o gene não for encontrado
            
            # Se nenhum gene for encontrado após o loop, gera um erro
            else:
                raise Gene.DoesNotExist
            
        except Gene.DoesNotExist:
            print(f"Gene {gene_id} não encontrado no banco de dados.")
            continue
        
        # Busca ou cria a família reguladora de transcrição
        transcriptional_regulator_family, created = TranscriptionalRegulatorFamily.objects.get_or_create(
            regulator_class=class_name,
            family=family_name
        )
        
        # Cria a associação Gene-TF
        GeneTFAssociation.objects.create(
            annotation_method=annotation_method,
            gene=gene,
            transcriptionalregulatorfamily=transcriptional_regulator_family
        )
        print(f"Associação criada para Gene {gene.gene_id} com a família {transcriptional_regulator_family.family}.")
