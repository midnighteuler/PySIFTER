'''
@author: msouza

'''

from zope.interface import Interface, Attribute

class IThirdPartyWrapper(Interface):
    '''
    Generic wrapper for calling third party tool
    '''
    
    expected_params = Attribute("List of parameter strings a call expects")
    expected_executable_locations = Attribute("List of executable setting labels a command expects")
    
    stdout_data = Attribute("Stdout data")
    stderr_data = Attribute("Stderr data")
    status = Attribute("Process status")
    
    parsed_results = Attribute("Results in parsed format")
    
    def setup_call(self, call_settings):
        """
        Provide settings for the caller.
        """
        
    def call(self, params):
        """
        Call executable with provided params
        """
    
    def parse_results(self):
        """
        Parse the stored call results and return
        parsed data structure.
        """