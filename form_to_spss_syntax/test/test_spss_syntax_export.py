'''
Created on Jun 14, 2014

@author: Esmail Fadae
'''

import unittest

from ..variable_metadata import VariableMetadata

class TestSpssSyntaxExport(unittest.TestCase):
    '''
    Test exporting SPSS ".sps" syntax files from :py:class:`VariableMetadata` 
    objects.
    '''
    
    def setUp(self):
        '''
        Create a :py:class:`VariableMetadata` object for all tests to operate on.
        '''
        
        self.single_variable_metadata= VariableMetadata(name='var_name', label='Variable label.'
                                      , value_mappings={'0':'True', '1':'Banana'})
              
    def test_export_single_variable(self):
        '''Test exporting a single variable's metadata.'''
        
        syntax_text, _, _= self.single_variable_metadata._export_spss_syntax()
        syntax_lines= (line for line in syntax_text.splitlines()) # Generator.
        
        # Default error message would print the entire `syntax_text`...
        self.assertIn('VARIABLE LABELS', syntax_text, 'Text "VARIABLE LABELS"'
                      + ' not found in exported syntax text.')
        while syntax_lines.next() != 'VARIABLE LABELS':
            # Skip any preceding lines.
            pass  
        
        self.assertIn(self.single_variable_metadata.name, syntax_text, 'Variable name'
                      + ' "{}"'.format(self.single_variable_metadata.name)
                      + ' not found in exported syntax text.')
        
        variable_label= self.single_variable_metadata.name + ' "' \
                        + self.single_variable_metadata.label + '"'
        self.assertEqual(syntax_lines.next(), variable_label
                         , 'Variable label line "%(variable_label)s"' % locals()
                         + ' was not found following the "VARIABLE LABELS" line.')
        
        self.assertIn('VALUE LABELS', syntax_text, 'Text "VALUE LABELS" not'
                      + ' found in exported syntax text.')
        while syntax_lines.next() != 'VALUE LABELS':
            # Skip any intermediate lines.
            pass
        
        line= syntax_lines.next()
        var_name= line.split('/')[1].split(' ')[0]
        self.assertEqual(var_name, self.single_variable_metadata.name)
        
        value_mappings_string= line.split(var_name)[1].strip()
        value_mappings= dict()
        while value_mappings_string != '':
            val_name= value_mappings_string.split(' ')[0]
            val_label= value_mappings_string.split('"')[1]
            value_mappings[val_name]= val_label
            # Cut off the portion just processed.
            value_mappings_string= value_mappings_string.split(val_label+'"')[1].strip()
        
        self.assertDictEqual(value_mappings, self.single_variable_metadata.value_mappings)
    
    
    def test_export_multiple_variables(self):
        '''Test exporting the metadata of multiple variables.'''
        another_variable_metadata= VariableMetadata(name='var2', label='Way cool label.'
                                                    , value_mappings={'you say':'yes', 'i say':'no'})
        variable_metadata_list= [self.single_variable_metadata, another_variable_metadata]
        
        syntax_text= VariableMetadata.export_spss_syntax(variable_metadata_list)
        syntax_lines= (line for line in syntax_text.splitlines()) # Generator.
        
        # Default error message would print the entire `syntax_text`...
        self.assertIn('\nVARIABLE LABELS\n', syntax_text, '"VARIABLE LABELS"'
                      + ' line not found in exported syntax text.')
        while syntax_lines.next() != 'VARIABLE LABELS':
            # Skip any preceding lines.
            pass  
        
        expected_variable_label_lines= list()
        for var_metadata in variable_metadata_list:
            variable_label= var_metadata.name + ' "' + var_metadata.label + '"'
            expected_variable_label_lines.append(variable_label)
        
        variable_label_line= syntax_lines.next()
        # Prepend a '/' to the first line so it can be handled in the same way 
        #   as the rest.
        variable_label_line= '/' + variable_label_line
        exported_variable_label_lines= list()
        while variable_label_line != '\n':
            exported_variable_label_lines.append(variable_label_line)
        
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
            expected_all_value_mappings[var_metadata.name]= var_metadata.value_mappings
        
        value_label_line= syntax_lines.next()
        exported_all_value_mappings= dict()
        while value_label_line != '\n':
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
        
        self.assertDictEqual(exported_all_value_mappings, expected_all_value_mappings)
        