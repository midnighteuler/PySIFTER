'''
Created on Jun 15, 2012

@author: msouza
'''
from zope.interface import implements

from FilesystemInteraction.Interfaces.DataRepository import IDataRepository

import git

class GitDataRepository(object):
    '''
    This creates a git repository to store files.
    Upon updating an "item", it commits the change.
    
    Uses GitPython. See: http://packages.python.org/GitPython/0.3.2/tutorial.html
    '''
    
    implements(IDataRepository)
    
    identity = None
    
    def create_repository(self, repo_identity):
        '''
        Create a new git repository, taking "repo_identity" to
        be the project directory it's created into.
        '''
        self.identity = repo_identity
        self.git_repo = git.Repo.init(repo_identity)
        
        self.git_repo.index.add(self.git_repo.untracked_files)
        self.git_repo.index.commit("Project created.")
        
    def open_repository(self, repo_identity):
        '''
        Update internal reference to repository matching repo_identity
        '''
        self.identity = repo_identity
        self.git_repo = git.Repo(repo_identity)
    
    def save_repository(self, save_description="Project saved."):
        '''
        Called to save the state of the repository.
        '''
        self.git_repo.index.add(self.git_repo.untracked_files)
        self.git_repo.index.commit(save_description)
    
    def close_repository(self):
        '''
        Called when repository is no longer needed.
        In the git case, we don't need to 'close' anything.
        '''
        pass
    
    def create_item(self, item_identifier, item_value):
        '''
        Create a new variable in the repository identified by item_identifier
        having value item_value.
        
        For git, item_identifier is path to file in the repository (which is
        "added" for the commit.
        
        While "item_value" is taken to be the description of the item added.
        '''
        #print self.git_repo.untracked_files
        self.git_repo.index.add([item_identifier])
    
    def destroy_item(self, item_identifier, destruction_information):
        '''
        Destroys the item having identifier item_identifier,
        providing destruction_information to destruction implementation.
        
        The file at path item_identifier in the git repository is
        deleted, and a commit is performed with description taken 
        as destruction_information. 
        '''
        assert "Not implemented" == 0
    
    def get_item_value(self, item_identifier):
        '''
        Retrieve item from repository for variable item_identifier.
        '''
        assert "Not implemented" == 0
    
    def set_item_value(self, item_identifier, item_value):
        '''
        Set item having identifier item_identifier to value item_value.
        '''
        assert "Not implemented" == 0
    
    def get_available_items(self, query_constraints):
        '''
        Returns list of items in the repository matching query_constraints.
        '''
        assert "Not implemented" == 0
    