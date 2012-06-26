'''
'''

from zope.interface import implements
from Interfaces.ProteinInformation import IProteinInformation

class ProteinInformation(object):
    '''
    Generic protein information class
    '''
    implements(IProteinInformation)
    
    def __init__(self, identifier,
                content,
                retrieval_method=None,
                retrieval_date=None,
                derived_properties=None,
                meta_data=None):
        '''
        Creates information object
        '''
        self.identifier = identifier
        self.content = content
        self.retrieval_method = retrieval_method
        self.retrieval_date = retrieval_date
        self.derived_properties = derived_properties
        self.meta_data = meta_data
    
    def __str__(self):
        '''
        String representation
        '''
        res_str = ''
        res_str += "Identifier: " + str(self.identifier) + "\n"
        res_str += "Content: " + str(self.content) + "\n"
        res_str += "Retrieval method: " + str(self.retrieval_method) + "\n"
        res_str += "Retrieval date: " + str(self.retrieval_date) + "\n"
        res_str += "Derived properties: " + str(self.derived_properties) + "\n"
        res_str += "Meta data: " + str(self.meta_data) + "\n\n"
        
        return res_str
    
    def export_as_xml(self):
        '''
        Represents this object as arbitrary format XML
        ''' 
        raise Exception,"Not implemented"
    
    def import_from_xml(self, xml_source):
        '''
        Import this object from arbitrary format XML
        ''' 
        raise Exception,"Not implemented"