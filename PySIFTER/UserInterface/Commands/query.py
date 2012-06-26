"""Create protein function query structure in a project."""

import logging
log = logging.getLogger(__name__)

from Project.SifterAnalysisProject import SifterAnalysisProject

def build_parser(parser):
    parser.add_argument(
        '-d', '--project_directory',
        dest = 'project_directory',
        metavar = 'FILE',
        required = True,
        help = 'SIFTER project directory')

    parser.add_argument(
        '-p', '--query_pfam_with_fasta',
        dest = 'query_fasta',
        metavar = 'FILE',
        help = """For each sequence in fasta format input,
        scans Pfam's HMM db for domain hits. For each hit,
        retrieves Pfam MSA and phylogeny, creates a reference
        package for pplacer by HMMER3 aligning the hit into the
        Pfam alignment.
        """)
    
def action(args):
    '''
    Query related actions
    '''
    sifter_project = SifterAnalysisProject()
    
    sifter_project.open_project(project_identifier=args.project_directory)
    
    # Pfam query route
    if args.query_fasta:
        sifter_project.make_queries_pfamscan(query_file=args.query_fasta)