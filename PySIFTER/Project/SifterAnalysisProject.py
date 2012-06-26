'''
This module contains SifterAnalysisProject, which controls
creation and running of SIFTER procedures.

See UserInterface.cli or UserInterface.web to see it viewed
 
'''

# External libs used (Biopython, python lang libs, etc)
from zope.interface import implements
from datetime import datetime
import os
import gzip
try:
    import cStringIO
    StringIO = cStringIO
except ImportError:
    import StringIO
# Internal modules used in this project
import Interfaces.AnalysisProject as pc
from GitAnalysisProject import GitAnalysisProject
from ProteinRepresentation.Features.ProteinInformation import ProteinInformation
from ThirdPartyWrappers.PfamHMMERQuery import PfamHMMERQuery
from ThirdPartyWrappers.PfamMySQLQuery import PfamMySQLQuery
from SifterQueryCollection import SifterQueryCollection


class SifterAnalysisProject(GitAnalysisProject):
    '''
    This project controller extends the "GitAnalysisProject"
    adding lots of functionality specific to doing a SIFTER analysis
    '''
    
    implements(pc.IAnalysisProject)
    
    def __init__(self):
        '''
        Initializes an empty query container
        '''
        self.query_collection = SifterQueryCollection()
    
    def parse_hypothetical_pfam_domains(self, pfam_results):
        '''
        Given pfam_results (from PfamHMMERQuery().parse_results()
        Creates domain_architecture entries for queries
        '''
        # For each HMMER hit, adds a domain entry.
        for i in range(len(pfam_results)):
            #pprint(vars(pfam_hmm_scan.parsed_results[i]))
            if not hasattr(pfam_results[i], "_annotations"):
                continue
            
            seq_id = pfam_results[i]._annotations['seqName']
            domain_id = pfam_results[i]._annotations['hmmName']
            new_domain_region = ProteinInformation(
                                identifier=domain_id,
                                content = pfam_results[i],
                                retrieval_method="PFamQuery",
                                retrieval_date=datetime.now().strftime("%Y-%m-%d %H:%M"))
            
            q = self.query_collection.get_query(query_id=seq_id)
            p = q.protein_collection.get_protein(protein_id=seq_id)
            
            p.domain_architecture.add_domain_region(domain_region=new_domain_region)
        
    def setup_pfam_mysql(self):
        '''
        Establishes a connection to Pfam MySQL db using settings from file
        '''
        if hasattr(self, "pfam_mysql"):
            return
        
        self.pfam_mysql = PfamMySQLQuery()
        
        executable_locs = {}
        params = {}
        for s in ['db_username', 'db_password', 'db_address', 'db_name']:
            params[s] = self.settings_repository.get_item_value(('mysql_database_pfam', s))
        
        self.pfam_mysql.setup_caller(executable_locations=executable_locs, params=params)
        
    def get_pfam_mysql_for_each_query(self, db_table, db_field, extra_where_str, file_postfix, gzipped=True):
        '''
        For each query, extracts the Pfam MSA from MySQL.
        '''
        self.setup_pfam_mysql()
        
        # For each query, loop over each domain and get each 
        # Pfam MSA from the pre-computed Pfam table.
        for q in self.query_collection:
            p = q.protein_collection.get_protein(q.query_id)
            
            cache_ids = []
            
            for d in p.domain_architecture:
                outpt_fname = os.path.dirname(q.destination) + "/" + d.identifier + file_postfix
                
                if d.identifier in cache_ids:
                    # If we've already queried this then no need to duplicate.
                    continue
                else:
                    # Get file from MySQL query, gunzip, and save into query directory.
                    mysql_aq =  "(select auto_pfamA from pfamA where pfamA_id='" + d.identifier + "')"
                    mysql_q = "select "+db_field+" from "+db_table+" " \
                            + "where auto_pfamA = "+mysql_aq+" " \
                            + extra_where_str + ";"
                    print mysql_q
                    self.pfam_mysql.call({'query': mysql_q})
                    self.pfam_mysql.parse_results()
                    
                    f_output = open(outpt_fname, "w")
                    if gzipped:
                        f_gzipped = StringIO.StringIO(self.pfam_mysql.parsed_results[0][0][0])
                        f = gzip.GzipFile(fileobj=f_gzipped, mode='rbU')
                        f_output.write(f.read())
                        f.close()
                        f_gzipped.close()
                    else:
                        f_output.write(self.pfam_mysql.parsed_results[0][0][0])
                    f_output.close()
                        
                    # Store id into cache to not retrieve multiple times
                    cache_ids.append(d.identifier)
                
                # Store reference to files created in the query.
                if d.meta_data is None:
                    d.meta_data = {}
                d.meta_data[db_field] = os.path.basename(outpt_fname)
    
    def make_phylo_placers_for_queries(self):
        '''
        Creates phylogenetic placement infrastructure for
        queries.
        This will use the ThirdPartyWrappers.PplacerWrapper
        '''
        for q in self.query_collection:
            p = q.protein_collection.get_protein(q.query_id)
            
            for d in p.domain_architecture:
                # Get file from MySQL query, gunzip, and save into query directory.
                #d.identifier
                #d.meta_data[db_field]
                pass
    
    def make_queries_pfamscan(self, query_file):
        '''
        Calls HMMER on PFam HMM files
        Creates ProteinCollection, adding a scaffold AnnotatedProtein for the
        query sequences in query_file.
        '''
        
        # Create project infrastructure for queries
        self.query_collection.create_query_scaffolds(query_file=query_file,
                                                     destination_base_dir=self.file_repository.identity)
        
        self.query_collection.export_to_files()
        
        self.file_repository.save_repository(save_description="Query scaffolds created.")
        
        # Call HMMER on Pfam HMMs for the input fasta file
        pfam_hmm_scan = PfamHMMERQuery()
        # Get necessary executable locations from project settings
        executable_locs = {}
        executable_locs['hmmpress'] = self.settings_repository.get_item_value(('executable_locations', 'hmmpress'))
        executable_locs['hmmscan'] = self.settings_repository.get_item_value(('executable_locations', 'hmmscan'))
        # Get necessary parameters from project settings 
        params = {}
        params['pfam_db_loc'] = self.settings_repository.get_item_value(('local_database_locations', 'pfam_data')) 
        params['query_sequences_fasta_file'] = query_file
        # Make call and do initial parsing of results into format for ProteinInformation retrievers.
        pfam_hmm_scan.setup_caller(executable_locations=executable_locs, params=params)
        pfam_hmm_scan.call()
        pfam_hmm_scan.parse_results()
        
        # Create domain regions for each HMM hit
        self.parse_hypothetical_pfam_domains(pfam_results=pfam_hmm_scan.parsed_results)
        self.query_collection.export_to_files()
        self.file_repository.save_repository(save_description="Hypothetical domain architectures from Pfam HMMs written to query files.")
        
        # Get and gunzip MSAs, trees.
        self.get_pfam_mysql_for_each_query(db_table="alignments_and_trees",
                                            db_field="alignment",
                                            extra_where_str="and type='full'",
                                            file_postfix=".sto")
        self.get_pfam_mysql_for_each_query(db_table="alignments_and_trees",
                                            db_field="tree",
                                            extra_where_str="and type='full'",
                                            file_postfix=".tree")
        self.query_collection.export_to_files()
        self.file_repository.save_repository(save_description="Exported alignments and trees into query directories from Pfam MySQL.")
        
        '''
        self.get_pfam_mysql_for_each_query(db_table="pfamA_HMM",
                                            db_field="hmm",
                                            extra_where_str="",
                                            file_postfix=".hmm",
                                            gzipped=False)
        '''