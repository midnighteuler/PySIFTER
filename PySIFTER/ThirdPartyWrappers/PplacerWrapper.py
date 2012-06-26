'''
This isn't finished.
Idea is to take inputs:
    * Pfam generated alignment
    * Pfam generated tree

and to create:
    * hmm from alignment (to extend alignment using hmmalign with --mapali)
    * wrapper to pplacer/taxi to:
        * Create reference package
            * Have to remove duplicates from alignment
              and then create an intermediate newick tree such that any
              nodes with 0 "pendant branch length" are merged into that deduplicated
              intermediate placeholder.
            * Want to be able to add those duplicates back onto the
              placeholder to give a complete newick.
        * Place queries onto reference package and generate
          newick (possibly containing duplicates as provided before "reference package" creation)
'''

from zope.interface import implements
from Interfaces.ThirdPartyWrapper import IThirdPartyWrapper

import os
from StringIO import StringIO

import _mysql as mysql
import _mysql_exceptions as mysql_exceptions

class PplacerWrapper(object):
    '''
    classdocs
    '''
    implements(IThirdPartyWrapper)
    
    expected_params = ['db_username',
                       'db_password',
                       'db_address',
                       'db_name']
    expected_executable_locations = []
    
    def setup_caller(self, executable_locations={}, params={}):
        '''
        Sets up self.executable_location
        '''
        for p in self.expected_params:
            if not p in params:
                raise Exception, "PfamMySQLQuery parameter %s not provided to call."%p
        for p in self.expected_executable_locations:
            if not p in executable_locations:
                raise Exception, "PfamMySQLQuery executable %s not provided to call."%p
        
        self.db = mysql.connect(host=params['db_address'],
                                user=params['db_username'],
                                passwd=params['db_password'],
                                db=params['db_name'])
        
        self.executable_locations = executable_locations
        self.params = params
        
    def call(self, other_params={}):
        """
        Call executable with provided params.
        """              
        for k,v in other_params.iteritems():
            self.params[k] = v
        
        self.db.query(self.params['query'])
        r = self.db.store_result()
        
        self.stdout_data = r
        #self.stdout_data, self.stderr_data = ''
        
        # Flag success
        self.status = 0
        
    def parse_results(self):
        """
        Parse the stored call results and return
        parsed data structure.
        Result structure is usable by ProteinInformation retriever methods.
        """
        # Expect return code to be zero
        if not(self.status == 0):
            raise Exception, "PfamMySQLQuery didn't succeed. (Return status: %i)\nStderr: %s"%(self.status, self.stderr_data)
        
        # Store matches for processing
        results = []
        m1 = self.stdout_data.fetch_row()
        while not len(m1) == 0:
            results.append(m1)
            m1 = self.stdout_data.fetch_row()
        
        self.parsed_results = results