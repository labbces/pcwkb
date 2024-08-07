# Adding data to PCW KB

## Loading data

Now that the databases are established, we have to populate it with some data.

Inside `pcwkb/pcwkb/pcwkbcore/tests` are some files to populate the site with a minimum data for the pages to work. But, for those there, is a need to insert the data in the correct order so the foreign keys that link each model/table works properly.

The command that will be used is manage.py loaddata that based on a json file, it populates the database.

```
python manage.py loaddata pcwkb_core/tests/data/taxonomy/species.json
python manage.py loaddata pcwkb_core/tests/data/literature/literature.json
python manage.py loaddata pcwkb_core/tests/data/molecular_components/genome.json
python manage.py loaddata pcwkb_core/tests/data/molecular_components/genes.json
```

## Django shell

To include other necessary data we will be using the shell. To access the shell you simply need to type:

```bash
python manage.py shell
```

### Ontology parser
As this project relys on ontology terms as the main categorators and the majority of the models in this project is related to it, we have a parser to include thse in our db.

The parser is on `pcwkb_core/utils/parsers/obo_related.py` and unfotunately only works with OBO files

Inside the shell environment, type:

```python
from pcwkb_core.utils.parsers.obo_related import Parser
```

and then

```python
Parser.add_from_obo("<path_to_obo_file>",ont="<ontology_abbreviation>")
```

You can also use `target_id=<ontology_id>` to parse only those ids that leads to a specific ontology id and `compressed=True` to use compressed files inside `Parser.add_from_obo`.

The <ontology_abbreviation> for each ontology used in this project is writeen inside `pcwkb_core/utils/parsers/obo_related.py`

Inside `pcwkb_core/tests/data/ontologies` we have some files to be included:

```python
Parser.add_from_obo("./pcwkb_core/tests/data/ontologies/chebi_data.tar.gz",ont="chebi",compressed=True)
Parser.add_from_obo("./pcwkb_core/tests/data/ontologies/to.obo",ont="to")
Parser.add_from_obo("./pcwkb_core/tests/data/ontologies/po.obo",ont="po")
Parser.add_from_obo("./pcwkb_core/tests/data/ontologies/eco.obo",ont="eco")
```

After loading those, now we can use loaddata to load data that relys on ontology terms.

```python
python manage.py loaddata pcwkb_core/tests/data/relationships/biomasscomposition_test_data.json
python manage.py loaddata pcwkb/pcwkb/pcwkb_core/tests/data/experiment/experiment_details.json
```

And load the first biomass-gene-experiment association file:

```python
python ./pcwkb_core/utils/loaders/biomass_gene_experiment_assoc_loader.py ./pcwkb_core/tests/data/experiment/biomass_gene_experimen_assoc.json
```


## GFF# Parser

from pcwkb_core.utils.parsers.gff3parser import GFF3Parser

GFF3Parser().add_from_gff3("<gff3_file>", <species_id>, <genome_id>)

You can also use `compressed=True` to use compressed files

Try:

"GFF3Parser().add_from_gff3("/home/jnov/PlantCellWall/Phytozome/Tests/Bdi_minimal_gff3.gff3", 15, 2)"


## Fasta parser

The correct order to input is transcript, cds and protein

from pcwkb_core.utils.parsers.fasta import Fasta

Fasta.add_from_fasta("<fasta_file>", "<sequence_type>", source="<source>")

The allowed sequence types are: protein, cds and transcript.

You can also use `compressed=True` to use compressed files

Try:

Fasta.add_from_fasta("/home/jnov/PlantCellWall/Phytozome/Tests/Bdi_minimal_transcripts.fa","transcript",source="Phytozome")
Fasta.add_from_fasta("/home/jnov/PlantCellWall/Phytozome/Tests/Bdi_minimal_cds.fa","cds",source="Phytozome")
Fasta.add_from_fasta("/home/jnov/PlantCellWall/Phytozome/Tests/Bdi_minimal_protein.fa","protein",source="Phytozome")


# Ortogroup parser

from pcwkb_core.utils.parsers.orthofinder_parser import OrthogroupParser
OrthogroupParser().add_from_orthofinder('Phytozome/Tests/Orthogroups.txt',1)