'''
'''

from zope.interface import implements
from Interfaces.ThirdPartyWrapper import IThirdPartyWrapper

import os
from StringIO import StringIO

# Unofficial biopython from "kellrott" fork
# branch "hmmer_bsd" (Retrieved June 22, 2012)
import biopython_temp.AlignIO as AlignIO
from biopython_temp._Hmmer import HmmScanCommandline, HmmPressCommandline, HmmAlignCommandline

class PfamHMMERQuery(object):
    '''
    classdocs
    '''
    implements(IThirdPartyWrapper)
    
    expected_params = ['query_sequences_fasta_file', 'pfam_db_loc']
    expected_executable_locations = ['hmmscan', 'hmmpress']
    
    def setup_caller(self, executable_locations, params):
        '''
        Sets up self.executable_location
        '''
        for p in self.expected_params:
            if not p in params:
                raise Exception, "PfamQuery parameter %s not provided to call."%p
        for p in self.expected_executable_locations:
            if not p in executable_locations:
                raise Exception, "PfamQuery executable %s not provided to call."%p
        
        self.executable_locations = executable_locations
        self.params = params
        
    def call(self):
        """
        Call executable with provided params.
        """
        #try:
        # Call HMM press (if it hasn't happened already.)
        if not os.path.isfile(self.params['pfam_db_loc']+'/Pfam-A.hmm.h3i'):
            call_cmd = HmmPressCommandline(cmd=self.executable_locations['hmmpress'],
                                       hmm=self.params['pfam_db_loc']+'/Pfam-A.hmm',
                                       force=False)
            self.stdout_data, self.stderr_data = call_cmd()
        
        
        call_cmd = HmmScanCommandline(cmd=self.executable_locations['hmmscan'],
                                      hmm=self.params['pfam_db_loc']+'/Pfam-A.hmm',
                                      input=self.params['query_sequences_fasta_file'])       
        self.stdout_data, self.stderr_data = call_cmd()
        
        # Flag success
        self.status = 0
        #except:
        #    # Flag failure
        #    self.status = 1    
        
        
    def parse_results(self):
        """
        Parse the stored call results and return
        parsed data structure.
        Result structure is usable by ProteinInformation retriever methods.
        """
        # Expect return code to be zero
        if not(self.status == 0):
            raise Exception, "PfamScan didn't succeed. (Return status: %i)\nStderr: %s"%(self.status, self.stderr_data)
            
        # Store matches for processing
        pfam_hmm_io = AlignIO.parse(StringIO(self.stdout_data), "hmmer3")
        pfam_hmm_matches = []
        for s in pfam_hmm_io:
            pfam_hmm_matches.append(s)
        
        self.parsed_results = pfam_hmm_matches