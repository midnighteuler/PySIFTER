'''
'''

from zope.interface import implements
from Interfaces.ProteinInformation import IProteinInformation
import ProteinInformation

from datetime import datetime
    
    
class DomainArchitecture(object):
    '''
    A domain architecture consists of a set of (possibly overlapping)
    sequence regions, and identifiers into some domain database
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.domains = []
    
    def __iter__(self):
        '''
        Returns iterator over the domains.
        '''
        for d in self.domains:
            yield d
    
    def __str__(self):
        '''
        String representation
        '''
        res_str = ''
        for d in self.__iter__():
            res_str += str(d)
        
        return res_str
    
    def add_domain_region(self, domain_region):
        '''
        Create a new domain region.
        Returns nothing.
        '''
        self.domains.append(domain_region)
    
    def export_as_xml(self):
        '''
        Represent as arbitrary XML format.
        '''
        raise Exception,"Not implemented"
    
    def import_from_xml(self, xml_source):
        '''
        Import from arbitrary XML format.
        '''
        raise Exception,"Not implemented"