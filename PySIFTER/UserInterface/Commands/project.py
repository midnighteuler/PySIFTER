"""Create or modify a SIFTER project"""

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
        '-c', '--create',
        dest = 'create_project',
        metavar = 'FILE',
        help = """A directory is created into the specified
        directory for this program to store result files.
        (Note: The project directory actually becomes a git
        repository that you can use the git cli to interact
        with.)
        """)
    
    parser.add_argument(
        '-s', '--project_settings',
        dest = 'project_settings_file',
        metavar = 'FILE',
        default=None,
        help = """Settings for the project are stored into a
        text configuration file within the project directory.
        You can provide the path to a settings file to initiate
        it.
        """)
    
def action(args):
    '''
    Project related actions
    '''
    sifter_project = SifterAnalysisProject()
    
    print "Parsed args:", args,"\n"
    # Project Create
    if hasattr(args, 'create_project'):
        sifter_project.create_project(project_identifier=args.project_directory,
                                      settings_source=args.project_settings_file)
