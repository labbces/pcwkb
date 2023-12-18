from django.db import models
from pcwkb_core.models.molecular_components.genetic.proteins import Protein

class GeneOntologyTerm(models.Model):
    """ todo: documentation
    """
    go_term = models.CharField(max_length=50, unique=True)
    go_class = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.go_term

    def add_from_obo(filename, empty=True, compressed=False):
        """
        Parses GeneOntology's OBO file and adds it to the database

        :param filename: Path to the OBO file to parse
        :param compressed: load data from .gz file if true (default: False)
        :param empty: Empty the database first when true (default: True)
        """
        # If required empty the table first
        # TODO: verificar se o banco está vazio antes de colocar os termos do GO

        obo_parser = OBOParser()
        obo_parser.readfile(filename, compressed=compressed)
        obo_parser.extend_go()

        if empty:
            # Assuming your model is named GO and is in your_django_app.models
            GO.objects.all().delete()

        for i, term in enumerate(obo_parser.terms):
            go = GO(
                term_id=term.id,
                name=term.name,
                namespace=term.namespace,
                definition=term.definition,
                is_obsolete=term.is_obsolete,
                is_a=";".join(term.is_a),
                extended_go=";".join(term.extended_go),
            )

            go.save()

            if i % 40 == 0:
                # commit to the db frequently to allow indexing functions to work without timing out
                try:
                    # Assuming you are using Django ORM
                    transaction.commit()
                except Exception as e:
                    transaction.rollback()
                    print(e)

        try:
            # commit remaining changes
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            print(e)


    

class GOProteinAssociation(models.Model):
    go_id = models.ForeignKey(GeneOntologyTerm, on_delete=models.CASCADE)
    protein_id = models.ForeignKey(Protein, on_delete=models.CASCADE)

