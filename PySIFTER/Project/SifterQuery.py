from ProteinRepresentation.ProteinCollection import ProteinCollection
import os

class SifterQuery(object):
    '''
    classdocs
    '''
    def __init__(self, query_id):
        '''
        Constructor
        '''
        self.query_id = query_id
        self.protein_collection = ProteinCollection()
    
    def __str__(self):
        '''
        String representation
        '''
        res_str = ""
        res_str += "Query from seq with id: %s\n"%self.query_id
        res_str += "Protein collection: \n"
        res_str += str(self.protein_collection)
        
        return res_str
    
    def set_query_destination(self, destination):
        '''
        Setter for export directory
        '''
        self.destination = destination
    
    def get_query_destination(self):
        '''
        Getter for export directory
        '''
        return self.destination
    
    def export_to_file(self, destination=None):
        '''
        Saves query to file
        '''
        if not(destination is None):
            self.destination = destination
        
        if not os.path.exists(os.path.dirname(self.destination)):
                os.mkdir(os.path.dirname(self.destination))
                
        # Make query file in XML representation.
        f = open(self.destination, "w")
        f.write(self.export_as_xml())
        f.close()
    
    def export_as_xml(self):
        '''
        Export into arbitrary XML format.
        '''
        # Need to write protein collection
        # Query id
        return str(self)
    
    def import_from_xml(self, xml_source):
        '''
        Imports from XML.
        '''
        raise Exception, "Not implemented yet."
    