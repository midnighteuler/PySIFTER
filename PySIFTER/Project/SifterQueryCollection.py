from ProteinRepresentation.Features.ProteinInformation import ProteinInformation
from ProteinRepresentation.Features.DomainArchitecture import DomainArchitecture
from ProteinRepresentation.AnnotatedProtein import AnnotatedProtein

from SifterQuery import SifterQuery

from datetime import datetime
import os
from Bio import SeqIO

class SifterQueryCollection(object):
    '''
    This class is to manage multiple SifterQuery objects.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.queries = {}
    
    def __str__(self):
        '''
        String representation
        '''
        return "Queries: "+str(self.queries.keys())
    
    def __iter__(self):
        '''
        Iterates over queries
        '''
        for q in self.queries.itervalues():
            yield q
        
    def add_query(self, query_id, query_content):
        '''
        Stores a query into this collection.
        '''
        if query_id in self.queries:
            raise Exception,"Query already exists in collection with that id."
        
        self.queries[query_id] = query_content
    
    def get_query(self, query_id):
        '''
        Returns query having given id
        '''
        if not query_id in self.queries:
            return None
        return self.queries[query_id]
    
    def create_query_scaffolds(self, query_file, destination_base_dir):
        '''
        Makes project infrastructure for queries
        '''
        q_dir = destination_base_dir + "/queries"
        if not os.path.exists(q_dir):
            os.mkdir(q_dir)
        
        # Scan over input fasta file, creating protein information
        # entities that we'll populate.
        handle = open(query_file, "rU")
        for record in SeqIO.parse(handle, "fasta"):
            # Create annotated protein
            p = AnnotatedProtein()
            p.protein_sequence = ProteinInformation(identifier=record.id,
                                                 content=record,
                                                 retrieval_method="Input Sequence",
                                                 retrieval_date=datetime.now().strftime("%Y-%m-%d %H:%M"))
            p.domain_architecture = DomainArchitecture()
            
            # Create new query object, and append this protein into it.
            new_query = SifterQuery(query_id=record.id)
            new_query.protein_collection.add_protein(record.id, p)
            
            # Set up where to save file
            q_dest = q_dir + "/query_%i"%len(self.queries)
            
            new_query.set_query_destination(destination = q_dest + "/query_file.xml")
            
            # Store query, and export into project infrastructure
            self.add_query(record.id, new_query)
        handle.close()
    
    def export_to_files(self):
        '''
        Exports each query to file.
        '''
        for q in self.__iter__():
            q.export_to_file()
        
    def export_as_xml(self):
        '''
        Arbitrary serialization to XML
        '''
    
    def import_from_xml(self, xml_source):
        '''
        Load from arbitrary XML format
        '''