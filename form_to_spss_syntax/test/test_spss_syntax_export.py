import unittest

class TestSpssSyntaxExport(unittest.TestCase):
    '''Test exporting SPSS ".sps" syntax files from `VariableMetadata` objects'''
    
    def setUp(self):
        '''Create a `VariableMetadata` object to test against.'''
        
        self.variable= VariableMetadata(name='var_name', label='Variable label.' 
                                      , value_dict={'0':'True', '1':'Banana'})
      
    def test_export_one_variable(self):
        '''Test exporting a single variable's metadata.'''
        
        syntax_text= spss_syntax_export(self.variable)
        syntax_lines= (line for line in syntax_text.splitlines()) # Generator.
        
        # Default error message would print the entire syntax file...
        self.assertIn('VARIABLE LABELS', syntax_text, 'Text "VARIABLE LABELS"'
                      + ' not found in exported syntax text.')
        while syntax_lines.next() != 'VARIABLE LABELS':
            # Skip any preceding lines.
            pass  
        
        self.assertIn(self.variable.name, syntax_text, 'Variable name'
                      + ' "%(self.variable.name)s not found in exported syntax'
                      + ' text.')
        
        variable_label= self.variable.name + ' "' + self.variable.label + '"'
        self.assertEqual(syntax_lines.next(), variable_label
                         , 'Variable label line "%(variable_label)"' % locals()
                         + ' was not found following the "VARIABLE LABELS" line.')
        
        self.assertIn('VALUE LABELS', syntax_text, 'Text "VALUE LABELS" not'
                      + ' found in exported syntax text.')
        while syntax_lines.next() != 'VALUE LABELS':
            # Skip any intermediate lines.
            pass
        
        line= syntax_lines.next()
        
        var_name= line.split('/')[1].split(' ')[0]
        self.assertEqual(var_name, self.variable.name)
        
        value_mappings_string= line.split(var_name)[1].strip()
        value_dict= dict()
        while value_mappings_string != '':
            val_name= value_mappings_string.split(' ')[0]
            val_label= value_mappings_string.split('"')[1]
            value_dict[val_name]= val_label
            # Cut off the portion just processed.
            value_mappings_string= value_mappings_string.split(val_label+'"')[1].strip()
        
        self.assertDictEqual(value_dict, self.variable.value_dict)    