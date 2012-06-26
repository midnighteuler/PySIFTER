'''

'''
from AnnotatedProtein import AnnotatedProtein

class ProteinCollection(object):
    '''
    This class is to manage multiple AnnotatedProtein objects.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.proteins = {}
    
    def __iter__(self):
        '''
        Iterates over proteins in this set.
        '''
        for p in self.proteins.itervalues():
            yield p
        
    def __str__(self):
        '''
        String representation
        '''
        res_str = ""
        for p in self.__iter__():
            res_str += str(p) + "\n"
        
        return res_str
    
    def add_protein(self, protein_id, protein_content):
        '''
        Appends (protein_id, protein_content) into collection.
        '''
        if protein_id in self.proteins:
            raise Exception,"Protein already exists in collection with that id."
        
        self.proteins[protein_id] = protein_content
    
    def get_protein(self, protein_id):
        '''
        Returns AnnotatedProtein object if found
        '''
        if not protein_id in self.proteins:
            raise Exception, "Requested protein %s not in this collection."%protein_id
        
        return self.proteins[protein_id]
    
    def export_as_xml(self):
        '''
        Arbitrary serialization to XML
        '''
    
    def import_from_xml(self, xml_source):
        '''
        Load from arbitrary XML format
        '''