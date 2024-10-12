# Adding data to PCW KB

## Loading data

Now that the databases are established, we have to populate it with some data.

Before the site can operate effectively, it is essential to populate the database with initial data. The following commands will load necessary data from JSON files into the database. Ensure that each JSON file is consistent with the schema defined by your models to avoid foreign key issues.

Inside `pcwkb/pcwkb/pcwkbcore/tests` are some files to populate the site with a minimum data for the pages to work. But, for those there, is a need to insert the data in the correct order so the foreign keys that link each model/table works properly.

The command that will be used is manage.py loaddata that based on a json file, it populates the database.

```
python manage.py loaddata pcwkb_core/tests/data/taxonomy/species.json
python manage.py loaddata pcwkb_core/tests/data/literature/literature.json
python manage.py loaddata pcwkb_core/tests/data/molecular_components/genome.json
python manage.py loaddata pcwkb_core/tests/data/molecular_components/genes.json
python manage.py loaddata pcwkb_core/tests/data/relationships/gene_regulation.json
```

## Django shell

To include other necessary data we will be using the shell. To access the Django shell, ensure your virtual environment is activated. Then type:

```bash
python manage.py shell
```

### Ontology parser

As this project relies on ontology terms as the primary classifiers and most of the models are related to them, we have implemented a parser to include these terms in our database.

The parser is on `pcwkb_core/utils/parsers/obo_related.py` and unfortunately only works with OBO files

Inside the shell environment, type:

```python
from pcwkb_core.utils.parsers.obo_related import Parser
```

and then

```python
Parser.add_from_obo("<path_to_obo_file>",ont="<ontology_abbreviation>")
```

You can also use `target_id=<ontology_id>` to parse only those IDs that leads to a specific ontology ID and `compressed=True` to use compressed files inside `Parser.add_from_obo`.

The parser relies on ontology terms as primary classifiers. The <ontology_abbreviation> for each ontology used in this project is defined in `pcwkb_core/utils/parsers/obo_related.py`

Inside `pcwkb_core/tests/data/ontologies` we have some files to be included:

```python
Parser.add_from_obo("./pcwkb_core/tests/data/ontologies/chebi_data.tar.gz",ont="chebi",compressed=True)
Parser.add_from_obo("./pcwkb_core/tests/data/ontologies/to.obo",ont="to")
Parser.add_from_obo("./pcwkb_core/tests/data/ontologies/po.obo",ont="po")
Parser.add_from_obo("./pcwkb_core/tests/data/ontologies/eco.obo",ont="eco")
```

Also include some objects to CellWallComponent model:


After loading those, now we can use loaddata to load data that relies on ontology terms.

```bash
python manage.py loaddata pcwkb_core/tests/data/molecular_components/cellwallcomponents.json
python manage.py loaddata pcwkb_core/tests/data/relationships/biomasscomposition_test_data.json
python manage.py loaddata pcwkb_core/tests/data/experiment/experiment_details.json
```

And load the first biomass-gene-experiment association file:


```bash
python ./pcwkb_core/utils/loaders/biomass_gene_experiment_assoc_loader.py ./pcwkb_core/tests/data/experiment/biomass_gene_experimen_assoc.json
```


### Gene associated data 

Gene associated data can be included using specific parsers designed to work with files formatted in a particular way. These parsers are primarily intended for Phytozome data but may be adaptable for other formats with similar headers.

All the codes in here should run inside the shell environment.

## GFF3 Parser

The GFF3 parser is a parser to include all the genes in a gff3 file.

```python
from pcwkb_core.utils.parsers.gff3parser import GFF3Parser

GFF3Parser().add_from_gff3("<gff3_file>", <species_id>, <genome_id>)
```

Try:

```python
GFF3Parser().add_from_gff3("./pcwkb_core/tests/data/molecular_components/Bdi_minimal_gff3.gff3", 15, 2)
```

## FASTA parser

The FASTA parser is used to extract transcript, CDS (coding sequence), and protein data to be entered into the database, ensuring that each is correctly associated with its corresponding gene. The data should be input in the following order: transcript, CDS, and then protein. This sequence allows for proper linking of a transcript to its CDS and a CDS to its protein.

```python
from pcwkb_core.utils.parsers.fasta import Fasta

Fasta.add_from_fasta("<fasta_file>", "<sequence_type>", source="<source>")
```

The allowed sequence types are: "protein", "cds" and "transcript".

Try:

```python
Fasta.add_from_fasta("./pcwkb_core/tests/data/molecular_components/Bdi_minimal_transcripts.fa","transcript",source="Phytozome")
Fasta.add_from_fasta("./pcwkb_core/tests/data/molecular_components/Bdi_minimal_cds.fa","cds",source="Phytozome")
Fasta.add_from_fasta("./pcwkb_core/tests/data/molecular_components/Bdi_minimal_protein.fa","protein",source="Phytozome")
```

# Orthogroup parser

To use the orthogroup parser you will need an orthogroup method that defines the tool or approach used to create orthogroups, here we provide an example:

```python
python manage.py loaddata pcwkb_core/tests/data/relationships/orthogroupmethods_test_data.json
```

After loading the orthogroup method, you can use the orthogroup parser to include orthogroups and associate with proteins inside your database. To do it execute the following commands:

```python
from pcwkb_core.utils.parsers.orthofinder_parser import OrthogroupParser
OrthogroupParser.add_from_orthofinder("<orthogroup_txt_file.txt>", <orthogroup_method>)
```

Try it using:
```python
OrthogroupParser.add_from_orthofinder("./pcwkb_core/tests/data/relationships/orthogroup_minimal.txt", 1)
```

Then you can add orthogroup trees files to each orthogroup as long as you have a zipped folder with orthogroup trees .txt files inside it. The usage is as it follows:

```python
OrthogroupParser.import_trees_zipped_folder("<orthogroup_tree_zipped_folder.zip>", <orthogroup_method>)
```

Try it using:
```python
OrthogroupParser.import_trees_zipped_folder("./pcwkb_core/tests/data/molecular_components/Gene_Trees_Test.zip", 1)
```

For all the parsers, except when using `OrthogroupParser.import_trees_zipped_folder` that requires a zipped folder, you can also use `compressed=True` to use compressed files.