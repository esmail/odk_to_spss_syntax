'''
Created on Jun 14, 2014

@author: Esmail Fadae
'''

import unittest

from ..variable_metadata import VariableMetadata

class TestExportSpssSyntax(unittest.TestCase):
    '''
    Test exporting SPSS ".sps" syntax files from :py:class:`VariableMetadata` 
    objects.
    '''
    
    def setUp(self):
        '''
        Create a :py:class:`VariableMetadata` object for use in multiple tests.
        '''
        
        self.ordinary_variable_metadata= VariableMetadata(name='var_name', label='Variable label.'
                                      , value_mappings={'0':'True', '1':'Banana'})


    def test_export_zero_variables(self):
        '''Test exporting zero variables (to increase test coverage).'''
        self.assert_correct_export([])
        
        
    def test_export_single_variable(self):
        '''Test exporting a single variable's metadata.'''
        variable_metadata_list= [self.ordinary_variable_metadata]
        self.assert_correct_export(variable_metadata_list)
         

    def test_export_multiple_variables(self):
        '''Test exporting the metadata of multiple variables.'''
        another_variable_metadata= VariableMetadata(name='var2', label='Way cool label.'
                                                    , value_mappings={'you_say':'goodbye', 'i_say':'hello'})
        no_val_label_metadata= VariableMetadata(name='v3', label='Boring label.'
                                      , value_mappings=None)
        variable_metadata_list= [self.ordinary_variable_metadata
                                 , another_variable_metadata
                                 , no_val_label_metadata]
        self.assert_correct_export(variable_metadata_list)


    def assert_correct_export(self, variable_metadata_list):
        '''Reusable assertion for testing with various inputs.'''
        
        syntax_text= VariableMetadata.export_spss_syntax(variable_metadata_list)
        
        if len(variable_metadata_list) == 0:
            self.assertEquals(syntax_text, '')
            return
        
        # Surround the prepend and append newlines to the text to ease testing.
        syntax_text= '\n' + syntax_text + '\n'
        syntax_lines= (line for line in syntax_text.splitlines()) # Generator.
        
        # Default error message would print the entire `syntax_text`...
        self.assertIn('\nVARIABLE LABELS\n', syntax_text, '"VARIABLE LABELS"'
                      + ' line not found in exported syntax text.')
        while syntax_lines.next() != 'VARIABLE LABELS':
            # Skip any preceding lines.
            pass  
        
        expected_variable_label_lines= list()
        for var_metadata in variable_metadata_list:
            variable_label= '/' + var_metadata.name + ' "' + var_metadata.label + '"'
            expected_variable_label_lines.append(variable_label)
        
        variable_label_line= syntax_lines.next()
        # Prepend a '/' to the first line so it can be handled in the same way 
        #   as the rest.
        variable_label_line= '/' + variable_label_line
        exported_variable_label_lines= list()
        while variable_label_line != '':
            exported_variable_label_lines.append(variable_label_line)
            variable_label_line= syntax_lines.next()
        
        expected_variable_label_lines.sort()
        exported_variable_label_lines.sort()
        self.assertListEqual(exported_variable_label_lines, expected_variable_label_lines)
        
        self.assertIn('\nVALUE LABELS\n', syntax_text, '"VALUE LABELS" line not'
                      + ' found in exported syntax text.')
        while syntax_lines.next() != 'VALUE LABELS':
            # Skip any intermediate lines.
            pass
        
        expected_all_value_mappings= dict()
        for var_metadata in variable_metadata_list:
            val_mappings= var_metadata.value_mappings
            # Don't record anything if the variable has no value mappings.
            if val_mappings != None:
                expected_all_value_mappings[var_metadata.name]= var_metadata.value_mappings
        
        value_label_line= syntax_lines.next()
        exported_all_value_mappings= dict()
        while value_label_line != '':
            var_name= value_label_line.split('/')[1].split(' ')[0]
            
            value_mappings_string= value_label_line.split(var_name)[1].strip()
            value_mappings= dict()
            while value_mappings_string != '':
                val_name= value_mappings_string.split(' ')[0]
                val_label= value_mappings_string.split('"')[1]
                value_mappings[val_name]= val_label
                # Chomp off the portion just consumed and proceed.
                value_mappings_string= value_mappings_string.split(val_label+'"')[1].strip()
                
            exported_all_value_mappings[var_name]= value_mappings
            value_label_line= syntax_lines.next()
        
        self.assertDictEqual(exported_all_value_mappings, expected_all_value_mappings)
