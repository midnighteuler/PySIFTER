'''
@author: msouza

This defines an interface for interacting with a "data repository"

It abstracts storage/retrieval of files or variable settings,
providing a means to implement specific desires in data handling.
'''

from zope.interface import Interface, Attribute

class IDataRepository(Interface):
    identity = Attribute("Identifier information for repository")
    
    def create_repository(self, repo_identity):
        '''
        Create a new repository having provided identity
        '''
    
    def open_repository(self, repo_identity):
        '''
        Open an existing repository corresponding to repo_identity
        '''
    
    def save_repository(self):
        '''
        Called to save the state of the repository.
        '''
    
    def close_repository(self):
        '''
        Called when repository is no longer needed.
        '''
    
    def create_item(self, item_identifier, item_value):
        '''
        Create a new variable in the repository identified by item_identifier
        having value item_value.
        '''
    def destroy_item(self, item_identifier, destruction_information):
        '''
        Destroys the item having identifier item_identifier,
        providing destruction_information to destruction implementation. 
        '''
    def get_item_value(self, item_identifier):
        '''
        Retrieve item from repository for variable item_identifier.
        '''
    def set_item_value(self, item_identifier, item_value):
        '''
        Set item having identifier item_identifier to value item_value.
        '''
    def get_available_items(self, query_constraints=None):
        '''
        Returns iterator of items in the repository matching query_constraints.
        '''
