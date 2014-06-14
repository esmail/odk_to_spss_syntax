'''
Created on Jun 14, 2014

@author: Esmail Fadae
'''

import unittest
import json

from ..variable_metadata import VariableMetadata

class TestImportJson(unittest.TestCase):
    '''
    Test parsing variable metadata from a JSON form into :py:class:`VariableMetadata` 
    objects.
    '''

    def setUp(self):
        '''Create a JSON form string to test against.'''
        
        self.form_dict= {'type': 'survey'
                         , 'children': [{'name': 'var_name'
                                         , 'label': 'Variable label.'
                                         , 'type': 'select one'
                                         , 'children': [{'name': '0', 'label': 'True'}
                                                        , {'name': '1', 'label': 'Banana'}]
                                         }]
                         }
        self.form_json= json.dumps(self.form_dict)

    def test_import_single_variable(self):
        '''Test importing of a single-variable form.'''
        
        variable_metadata= VariableMetadata.import_json(self.form_json)
        
        var_name= self.form_dict['children'][0]['name']
        self.assertEquals(variable_metadata.name, var_name)
        
        var_label= self.form_dict['children'][0]['label']
        self.assertEquals(variable_metadata.label, var_label)
        
        value_mapping_list= self.form_dict['children'][0]['children']
        value_mappings= dict()
        for mapping in value_mapping_list:
            name= mapping['name']
            label= mapping['label']
            value_mappings[name]= label
        self.assertDictEqual(variable_metadata.value_mappings, value_mappings)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()