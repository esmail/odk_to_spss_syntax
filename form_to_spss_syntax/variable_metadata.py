'''
Created on Jun 13, 2014

@author: Esmail Fadae
'''

from collections import namedtuple
import json

class VariableMetadata(namedtuple('_VariableMetadata', 'name, label, value_mappings')):
    '''
    A :py:class:`VariableMetadata` object contains the metadata about an 
    individual form variable. The class inherits from a semi-anonymous 
    :py:func:`namedtuple` (:py:class:`_VariableMetadata`) that handles object 
    construction and the creation of immutable attribute accessors.
    
    :param str name: The encoded name of the variable (e.g. "a01")
    :param str label: The variable's readable label (e.g. "What is your sex?")
    :param dict value_mappings: A dictionary that maps encoded value names (e.g.  
    "0", "1") to value labels (e.g. "Female", "Male")
    '''

    def _export_spss_syntax(self):
        '''
        Export the SPSS ".sps" syntax file formatted variable label line and 
        value label line (if any) that correspond to this :py:class:`VariableMetadata` 
        object.
        
        :rtype: tuple(str, str)
        '''
                
        variable_label_line= '/' + self.name + ' "' + self.label + '"'
        
        # There aren't always value labels to report.
        if self.value_mappings == None:
            value_label_line= None
        else:        
            value_label_line= '/' + self.name
            for value_name, value_label in self.value_mappings.iteritems():
                value_label_line+= ' ' + value_name + ' "' + value_label + '"'
        
        return variable_label_line, value_label_line

    
    @classmethod
    def export_spss_syntax(cls, variable_metadata_list):
        '''
        Export a list of :py:class:`VariableMetadata` objects to the SPSS ".sps" 
        syntax file format.
        
        :param list(:py:class:`VariableMetadata`) variable_metadata_list:
        :rtype: str
        '''
        
        if len(variable_metadata_list) == 0:
            return ''
        
        
        variable_label_lines= list()
        value_label_lines= list()
        for var_metadata in variable_metadata_list:
            var_label_line,  val_label_line= var_metadata._export_spss_syntax()
            variable_label_lines.append(var_label_line)
            if val_label_line != None:
                value_label_lines.append(val_label_line)
        
        # Remove the prepending "/" from the first variable label line.
        variable_label_lines[0]= variable_label_lines[0].split('/')[1]
        
        syntax_string= 'VARIABLE LABELS\n'
        for var_label_line in variable_label_lines:
            syntax_string+= var_label_line + '\n'
        
        # There aren't always value labels to report.
        if len(value_label_lines) != 0:
            syntax_string+= '\nVALUE LABELS\n'
            for val_label_line in value_label_lines:
                syntax_string+= val_label_line + '\n'
        
        
        return syntax_string
    
    @classmethod
    def import_json(cls, form_json):
        '''
        Create :py:class:`VariableMetadata` objects from a simple JSON form (no 
        groups).
        
        :param str form_json: The JSON-formatted text of the form being imported.
        :rtype: list(:py:class:`VariableMetadata`) 
        '''
        
        form_dict= json.loads(form_json)
        form_variables= form_dict['children']
        variable_metadata_list= list()
        for form_var in form_variables:
            var_name= form_var['name']
            var_label= form_var['label']
            
            # TODO: Find out multi-select "type" (e.g. "select multiple")
            if form_var['type'] in ['select one']:
                value_mappings_list= form_var['children']
                value_mappings= dict()
                for mapping in value_mappings_list:
                    val_name= mapping['name']
                    val_label= mapping['label']
                    value_mappings[val_name]= val_label
            else:
                value_mappings= None
            
            variable_metadata= cls(var_name, var_label, value_mappings)
            variable_metadata_list.append(variable_metadata)
        
        return variable_metadata_list
            

        