'''
@author: msouza

This defines an interface for a protein feature.
Expected Implementations:
    ProteinSequence
    ProteinAnnotation
    DomainArchitecture.

'''

from zope.interface import Interface, Attribute

class IProteinInformation(Interface):
    '''
    A generic protein feature. 
    
    Each feature has:
        Identifier
        Content
        Retrieval_method
        Retrieval_date
        Derived_properties
        Meta_data
    '''
    identifier = Attribute("Identifier for this feature")
    content = Attribute("Content of this feature")
    retrieval_method = Attribute("Method used to retrieve this feature")
    retrieval_date = Attribute("Timestamp for feature retrieval")
    derived_properties = Attribute("Derived properties container")
    meta_data = Attribute("Generic meta-data container")
    
    def export_as_xml(self):
        '''
        Represent as arbitrary XML format.
        '''
    
    def import_from_xml(self, xml_source):
        '''
        Import from arbitrary XML format.
        '''