'''
Created on Jun 18, 2012

@author: msouza
'''

#from Features.DomainArchitecture import DomainArchitecture
#from Features.ProteinAnnotation import ProteinAnnotation
#from Features.ProteinInformation import ProteinInformation

class AnnotatedProtein(object):
    '''
    This is an object to represent annotated proteins.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.domain_architecture = None
        self.protein_sequence = None
        self.annotations = []
    
    def __str__(self):
        '''
        String representation.
        '''
        res_str = ''
        res_str += "Protein sequence: \n" 
        res_str += str(self.protein_sequence) + "\n"
        
        res_str += "Domain architecture: \n"
        res_str += str(self.domain_architecture) + "\n"
        
        res_str += "Annotations: \n"
        res_str += str(self.annotations) + "\n"
        
        return res_str
        #raise Exception,"Not implemented"
    
    def export_as_xml(self):
        '''
        Exports to arbitrary XML format.
        '''
        raise Exception,"Not implemented"
    
    def import_from_xml(self, xml_source):
        '''
        Imports from arbitrary XML format.
        '''
        raise Exception,"Not implemented"
    
   
        
    