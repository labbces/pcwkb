"""
Parser class for obo files (ontology structure files).
Copied and adapted Conekt source code (https://github.com/sepro/conekt)
"""
from pcwkb_core.models.molecular_components.genetic.genes import Gene
from pcwkb_core.models.taxonomy.ncbi_taxonomy import Species


import sys
import gzip


class Fasta:
    def __init__(self):
        self.sequences = {}

    def remove_subset(self, length):
        """
        Removes a set of sequences and returns those as a subset

        :param length: number of sequences to remove
        :return: Fasta object with the sequences removed from the current one
        """
        output = Fasta()
        keys = list(self.sequences.keys())
        output.sequences = {k: self.sequences[k] for k in keys[:length]}

        self.sequences = {k: self.sequences[k] for k in keys[length:]}

        return output

    def readfile(self, filename, compressed=False, verbose=True):
        """
        Reads a fasta file to the dictionary

        :param filename: file to read
        :param compressed: set to true if reading form a gzipped file
        :param verbose: set to true to get extra debug information printed to STDERR
        """
        if verbose:
            print("Reading FASTA file:" + filename + "...", file=sys.stderr)

        # Initialize variables
        header = ""
        sequence = []
        count = 1

        # open file
        if compressed:
            f = gzip.open(filename, "rt")
        else:
            f = open(filename, "r")

        for line in f:
            line = line.rstrip()
            if line.startswith(">"):
                # ignore if first
                if not header == "":
                    self.sequences[header] = "".join(sequence)
                    count += 1
                header = line.lstrip(">")
                sequence = []
            else:
                sequence.append(line)

        # add last gene
        self.sequences[header] = "".join(sequence)

        f.close()
        if verbose:
            print("Done! (found ", count, " sequences)", file=sys.stderr)

    def writefile(self, filename):
        """
        writes the sequences back to a fasta file

        :param filename: file to write to
        """
        with open(filename, "w") as f:
            for k, v in self.sequences.items():
                print(">" + k, file=f)
                print(v, file=f)
    
    @staticmethod
    def add_from_fasta(filename, seq_type, source="",compressed=False, verbose=True):

        # the correct order to input is transcript, cds and protein
        
        fasta_data = Fasta()
        fasta_data.readfile(filename, compressed, verbose)

        new_sequences = []

        # Loop over sequences, sorted by name (key here) and add to db
        for i, (header, sequence) in enumerate(sorted(fasta_data.sequences.items()), start=1):

            fa_id = ""
            transcript_name = ""
            protein_name = ""
            gene_id = ""

            header = header.split()
            name=header[0]
            
            for str in header:
                if str.startswith("locus"):
                    _, gene_id = str.split("=")
                elif str.startswith("ID"):
                    _, fa_id = str.split("=")
                elif str.startswith("transcript"):
                    _, transcript_name = str.split("=")
                elif str.startswith("polypeptide"):
                    _, protein_name  = str.split("=")
            
            if Gene.objects.filter(gene_id=gene_id).exists(): #could be a try and except to raise a gene obligatory request
                gene = Gene.objects.get(gene_id=gene_id)
            else:
                gene = ""

            if seq_type == 'transcript':
                from pcwkb_core.models.molecular_components.genetic.transcripts import Transcript

                if not Transcript.objects.filter(transcript_name = name,
                                                       transcript_id = fa_id,
                                                       sequence = sequence,
                                                       gene = gene):
                    model_data = Transcript.objects.create(transcript_name = name,
                                                           transcript_id = fa_id,
                                                           sequence = sequence,
                                                           gene = gene,
                                                           source = source)
                else:
                    print("This transcript fasta data is already in the database")                 

            elif seq_type == 'cds':
                from pcwkb_core.models.molecular_components.genetic.transcripts import Transcript
                from pcwkb_core.models.molecular_components.genetic.cds import CDS

                if Transcript.objects.filter(transcript_name=name).exists():
                    transcript = Transcript.objects.get(transcript_name=name)
                else:
                    transcript = ""
                
                if not CDS.objects.filter(cds_name = name,
                                          cds_id = fa_id,
                                          sequence = sequence,
                                          gene = gene,
                                          transcript = transcript,
                                          protein_name = protein_name):
                    
                    model_data = CDS.objects.create(cds_name = name,
                                               cds_id = fa_id,
                                               sequence = sequence,
                                               gene = gene,
                                               transcript = transcript,
                                               protein_name = protein_name,
                                               source = source,
                                               )
                else:
                    print("This cds fasta data is already in the database")

            elif seq_type == 'protein':
                
                from pcwkb_core.models.molecular_components.genetic.transcripts import Transcript
                from pcwkb_core.models.molecular_components.genetic.proteins import Protein
                from pcwkb_core.models.molecular_components.genetic.cds import CDS

                if Transcript.objects.filter(transcript_name=transcript_name).exists():
                    transcript = Transcript.objects.get(transcript_name=transcript_name)
                else:
                    transcript = None
                
                if CDS.objects.filter(protein_name=name).exists():
                    cds = CDS.objects.get(protein_name=name)
                else:
                    cds = None
            
                
                if not Protein.objects.filter(protein_name = name,
                                              protein_id = fa_id,
                                              sequence = sequence,
                                              gene = gene,
                                              transcript = transcript,
                                              cds = cds):

                    model_data = Protein.objects.create(protein_name = name,
                                                        protein_id = fa_id,
                                                        sequence = sequence,
                                                        gene = gene,
                                                        transcript = transcript,
                                                        cds = cds,
                                                        source = source,
                                                        )
                else:
                    print(f"This protein '{name}'fasta data is already in the database")


        print(f"{i+1} {seq_type} fasta data parsed to the database")
        
        return model_data