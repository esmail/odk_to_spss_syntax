import unittest
from ..variable_metadata import VariableMetadata

class TestSpssSyntaxExport(unittest.TestCase):
    '''
    Test exporting SPSS ".sps" syntax files from :py:class:`VariableMetadata` 
    objects
    '''
    
    def setUp(self):
        '''Create a :py:class:`VariableMetadata` object to test against.'''
        
        self.variable_metadata= VariableMetadata(name='var_name', label='Variable label.'
                                      , value_mappings={'0':'True', '1':'Banana'})
      
    def test_export_one_variable(self):
        '''Test exporting a single variable's metadata.'''
        
        syntax_text= self.variable_metadata.export_spss_syntax()
        syntax_lines= (line for line in syntax_text.splitlines()) # Generator.
        
        # Default error message would print the entire `syntax_text`...
        self.assertIn('VARIABLE LABELS', syntax_text, 'Text "VARIABLE LABELS"'
                      + ' not found in exported syntax text.')
        while syntax_lines.next() != 'VARIABLE LABELS':
            # Skip any preceding lines.
            pass  
        
        self.assertIn(self.variable_metadata.name, syntax_text, 'Variable name'
                      + ' "{}"'.format(self.variable_metadata.name)
                      + ' not found in exported syntax text.')
        
        variable_label= self.variable_metadata.name + ' "' + self.variable_metadata.label + '"'
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
        self.assertEqual(var_name, self.variable_metadata.name)
        
        value_mappings_string= line.split(var_name)[1].strip()
        value_mappings= dict()
        while value_mappings_string != '':
            val_name= value_mappings_string.split(' ')[0]
            val_label= value_mappings_string.split('"')[1]
            value_mappings[val_name]= val_label
            # Cut off the portion just processed.
            value_mappings_string= value_mappings_string.split(val_label+'"')[1].strip()
        
        self.assertDictEqual(value_mappings, self.variable_metadata.value_mappings)    