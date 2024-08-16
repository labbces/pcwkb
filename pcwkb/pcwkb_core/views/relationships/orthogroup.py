from django.shortcuts import render, get_object_or_404

from pcwkb_core.models.molecular_components.relationships.orthogroups import Orthogroup

def og_page(request, og_name):
    orthogroup = get_object_or_404(Orthogroup, og_name=og_name)

    # Retrieve related proteins for the orthogroup
    proteins = orthogroup.proteinorthogroup_set.select_related('protein')

     # Access the associated OrthogroupMethods using the ForeignKey relationship
    orthogroup_methods = orthogroup.og_method

    return render(request, 'relationships/og_page.html', {'orthogroup': orthogroup, 'proteins': proteins, 'method':orthogroup_methods})