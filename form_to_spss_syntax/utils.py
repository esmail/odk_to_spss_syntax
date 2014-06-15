'''
Contains the outward interface of the package.
Created on Jun 14, 2014

@author: esmail
'''

from variable_metadata import VariableMetadata

def from_json(json_text):
    '''
    Create an SPSS ".sps" syntax file based on form variable metadata from the 
    provided JSON-formatted ODK Collect form.
    
    :param str json_text:
    '''
    
    variable_metadata_list= VariableMetadata.import_json(json_text)
    spss_syntax_string= VariableMetadata.export_spss_syntax(variable_metadata_list)
    
    return spss_syntax_string