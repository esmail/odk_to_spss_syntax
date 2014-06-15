'''
Created on Jun 14, 2014

@author: Esmail Fadae
'''

import unittest

from ..variable_metadata import VariableMetadata


def parse_spss_syntax(test_case, spss_syntax_text):
    '''
    Check the formatting of the provided syntax text, checking for a variable 
    labels section and possibly a value labels section. Return any parsed 
    variable labels and value labels. 
    
    :param :py:class:`unittest.TestCase` test_case: Making this an explicit 
    parameter allows this function to be called from any :py:class:`unittest.TestCase`
    descendant.
    :param str spss_syntax_text: The text of a SPSS ".sps" syntax file.
    :return: A dictionary of parsed mappings from variable names to their 
    corresponding labels. Another dictionary with an entry for each variable 
    with parsed mappings from value names to value labels.  
    :rtype: tuple(dict, dict)
    '''
    
    # Surround the prepend and append newlines to the text to ease processing.
    spss_syntax_text= '\n' + spss_syntax_text + '\n'
    syntax_lines= (line for line in spss_syntax_text.splitlines()) # Generator.
    
    # Default error message would print `spss_syntax_text` in its entirety...
    test_case.assertIn('\nVARIABLE LABELS\n', spss_syntax_text, '"VARIABLE LABELS"'
                  + ' line not found in exported syntax text.')
    while syntax_lines.next() != 'VARIABLE LABELS':
        # Skip any preceding lines.
        pass  
    
    variable_label_line= syntax_lines.next()
    # Prepend a '/' to the first line so it can be handled in the same way 
    #   as the rest.
    variable_label_line= '/' + variable_label_line
    variable_mappings= dict()
    while variable_label_line != '':
        var_name= variable_label_line.split('/')[1].split(' ')[0]
        var_label= variable_label_line.split('"')[1]
        variable_mappings[var_name]= var_label

        variable_label_line= syntax_lines.next()
    
    test_case.assertIn('\nVALUE LABELS\n', spss_syntax_text, '"VALUE LABELS" line not'
                  + ' found in exported syntax text.')
    while syntax_lines.next() != 'VALUE LABELS':
        # Skip any intermediate lines.
        pass
    
    value_label_line= syntax_lines.next()
    all_value_mappings= dict()
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
            
        all_value_mappings[var_name]= value_mappings
        value_label_line= syntax_lines.next()

    return variable_mappings, all_value_mappings


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
        
        exported_syntax_text= VariableMetadata.export_spss_syntax(variable_metadata_list)
        
        if len(variable_metadata_list) == 0:
            self.assertEquals(exported_syntax_text, '')
            return
        
        exported_variable_mappings, exported_all_value_mappings= parse_spss_syntax(self, exported_syntax_text)
        
        expected_variable_mappings= dict()
        expected_all_value_mappings= dict()
        for var_metadata in variable_metadata_list:
            expected_variable_mappings[var_metadata.name]= var_metadata.label
            
            val_mappings= var_metadata.value_mappings
            # Don't record anything if the variable has no value mappings.
            if val_mappings != None:
                expected_all_value_mappings[var_metadata.name]= var_metadata.value_mappings
        
        self.assertDictEqual(exported_variable_mappings, expected_variable_mappings)
        self.assertDictEqual(exported_all_value_mappings, expected_all_value_mappings)
