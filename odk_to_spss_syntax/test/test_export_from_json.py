'''
Created on Jun 14, 2014

@author: esmail
'''

import unittest
import os
import sys

from ..main import from_json
from ..main import main
from test_export_spss_syntax import parse_spss_syntax


class TestExportFromJson(unittest.TestCase):
    '''
    Integration tests for the exporting of variable metadata from JSON-formatted 
    ODK forms to SPSS ".sps" syntax files.
    '''
    
    def setUp(self):
        # Magic to get the path of the directory that contains this module.
        self.module_dir= os.path.dirname(os.path.realpath(__file__))
        
        self.test_form_path= os.path.join(self.module_dir, 'test_form.json')
        self.test_syntax_path= os.path.join(self.module_dir, 'test_syntax.sps')

    def test_export_from_json(self):
        '''
        Load a JSON-formatted ODK form from file and test the generated SPSS syntax output against a canonical output example.
        '''
        
        with open(self.test_form_path, 'r') as f:
            form_text_json= f.read()
            
        exported_spss_syntax= from_json(form_text_json)
        
        with open(self.test_syntax_path, 'r') as f:
            canonical_spss_syntax= f.read()
        
        self.assert_syntaxes_equivalent(exported_spss_syntax, canonical_spss_syntax)
            
        
    def assert_syntaxes_equivalent(self, exported_spss_syntax, canonical_spss_syntax):
        '''Reusable assertion to compare two SPSS syntax texts.'''
        exported_variable_mappings, exported_all_value_mappings= parse_spss_syntax(self, exported_spss_syntax)
        
        expected_variable_mappings, expected_all_value_mappings= parse_spss_syntax(self, canonical_spss_syntax)
        
        self.assertDictEqual(exported_variable_mappings, expected_variable_mappings)
        self.assertDictEqual(exported_all_value_mappings, expected_all_value_mappings)
        
class TestCli(TestExportFromJson):
    '''
    Test the command line interface building on functionality from :py:class:`TestExportFromJson`.
    '''
    
    def setUp(self):
        '''Specify a temporary output file.'''
        super(TestCli, self).setUp()
        self.exported_syntax_file= os.path.join(self.module_dir, 'exported.sps')
    
    def tearDown(self):
        '''Delete the temporary output file if it was created.'''
        super(TestCli, self).tearDown()
        if os.path.exists(self.exported_syntax_file):
            os.remove(self.exported_syntax_file)
            
    def test_cli(self):
        '''Test the command line interface.'''
                
        exported_syntax_file= os.path.join(self.module_dir, 'exported.sps')
        argv= '--json ' + self.test_form_path + ' ' + exported_syntax_file
        argv= argv.split(' ')
        main(argv)
        
        with open(exported_syntax_file, 'r') as f:
            exported_spss_syntax= f.read()
        
        with open(self.test_syntax_path, 'r') as f:
            canonical_spss_syntax= f.read()
        
        self.assert_syntaxes_equivalent(exported_spss_syntax, canonical_spss_syntax)


    