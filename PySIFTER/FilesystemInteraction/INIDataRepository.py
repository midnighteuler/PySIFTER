'''
Created on Jun 15, 2012

@author: msouza
'''
from zope.interface import implements

from FilesystemInteraction.Interfaces.DataRepository import IDataRepository

import ConfigParser

class INIDataRepository(object):
    '''
    This creates a text (ini) config file to store (name, value) pairs.
    
    
    Uses ConfigParser. See: http://wiki.python.org/moin/ConfigParserExamples
    '''
    
    implements(IDataRepository)
    
    identity = None
    
    def create_repository(self, repo_identity):
        '''
        Create a new ini file, taking "repo_identity" to
        be the the local file path to create the file into.
        '''
        self.identity = repo_identity
        self.cfgfile = open(repo_identity, 'w')
        self.ini_parser = ConfigParser.SafeConfigParser()
    
    def open_repository(self, repo_identity):
        '''
        Update internal reference to repository matching repo_identity
        '''
        self.identity = repo_identity
        self.ini_parser = ConfigParser.SafeConfigParser()
        
        self.cfgfile = open(repo_identity)
        self.ini_parser.readfp(self.cfgfile)
    
    def save_repository(self):
        '''
        Called to save the state of the repository.
        '''
        self.ini_parser.write(self.cfgfile)
    
    def close_repository(self):
        '''
        Called when repository is no longer needed.
        '''
        self.cfgfile.close()
    
    def create_item(self, item_identifier, item_value):
        '''
        Create a new variable in the repository identified by item_identifier
        having value item_value.
        
        For this implementation:
            item_identifier is tuple (section, varname)
            and
            item_value is the value of the setting.
        '''
        var_section, var_name = item_identifier
        if not(self.ini_parser.has_section(var_section)):
            self.ini_parser.add_section(var_section)
        
        self.ini_parser.set(var_section, var_name, item_value)
            
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
        var_section, var_name = item_identifier
        return self.ini_parser.get(var_section, var_name)
    
    def set_item_value(self, item_identifier, item_value):
        '''
        Set item having identifier item_identifier to value item_value.
        '''
        assert "Not implemented" == 0
    
    def get_available_items(self, query_constraints=None):
        '''
        Returns iterator of items in the repository matching query_constraints.
        '''
        for section_name in self.ini_parser.sections():
            for name, value in self.ini_parser.items(section_name):
                yield [(section_name, name), value]
        
        
    
    