'''
Created on Jun 14, 2014

@author: esmail
'''

import unittest
import os

from ..utils import from_json
from test_export_spss_syntax import parse_spss_syntax


class TestExportFromJson(unittest.TestCase):
    '''
    Integration tests for the exporting of variable metadata from JSON-formatted 
    ODK Collect forms to SPSS ".sps" syntax files.
    '''

    def test_export_from_json(self):
        '''
        Load a JSON-formatted ODK Collect form from file and test the generated SPSS syntax output against a canonical output example.
        '''
        
        # Magic to get the path of the directory that contains this module.
        module_dir= os.path.dirname(os.path.realpath(__file__))
        
        test_form_path= os.path.join(module_dir, 'test_form.json')
        with open(test_form_path, 'r') as f:
            form_text_json= f.read()
            
        exported_spss_syntax= from_json(form_text_json)
        exported_variable_mappings, exported_all_value_mappings= parse_spss_syntax(self, exported_spss_syntax)
        
        test_syntax_path= os.path.join(module_dir, 'test_syntax.sps')
        with open(test_syntax_path, 'r') as f:
            canonical_spss_syntax= f.read()
            
        expected_variable_mappings, expected_all_value_mappings= parse_spss_syntax(self, canonical_spss_syntax)
        
        self.assertDictEqual(exported_variable_mappings, expected_variable_mappings)
        self.assertDictEqual(exported_all_value_mappings, expected_all_value_mappings)
