'''
@author: msouza

This defines an interface for interacting with the inputs/outputs
for a "project".

The use-case it was created for is computational biology workflows.

When new files or settings for a workflow are created/changed,
the class implementing this interface dictates how to handle
those actions.

A "Project" has the following abstract structure:

Project
---Identifier
    A key used to identify this project.

---Settings Repository
    Infrastructure to deal with input/output of short 
    text/numeric variables dictating project properties.
    Envisioned implementations for this:
        Local INI config files (ConfigParser read/write).
        Remotely retrieved/stored files
        MySQL or SQLITE or (...) table storage.

---File Repository
    Infrastructure to deal with input/output of files.
    Envisioned implementation:
        Local storage/update of version control repository
        git, svn, etc.
        Storage into MySQL or SQLITE or (...) structure.
        
---History Repository
    Infrastructure to deal with logging and reporting details
    describing the progression of the project.

'''

from zope.interface import Interface, Attribute

class IAnalysisProject(Interface):
    '''
    A generic project controller. 
    
    Contains three DataRepository implementations.
    '''
    identifier = Attribute("Identifying key for this project")
    
    settings_repository = Attribute("DataRepository to deal with storing project properties.")
    history_repository = Attribute("DataRepository to deal with project history.")
    file_repository = Attribute("DataRepository to deal with input/output of files.")
        
    def create_project(self, project_identifier, settings_source=None):
        """
        Create new project container at given directory, initializing the repos into it.
        """
    
    def open_project(self, project_identifier):
        """Point internal project reference to existing project"""
    
    def load_default_settings(self, settings_source):
        """
        Load in default settings from some source
        """