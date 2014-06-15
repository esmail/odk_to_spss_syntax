'''
Created on Jun 13, 2014

@author: Esmail Fadae
'''

from collections import namedtuple
import json
import re

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
        
        # TODO: Should labels be truncated to 116 characters?
        
        # Variable labels aren't always specified.
        variable_label_line= '/' + self.name + ' "'
        if self.label == None:
            variable_label_line+= self.name + '"'
        else:
            variable_label_line+= self.label + '"'
        
        # There aren't always value labels to report.
        if self.value_mappings == None:
            value_label_line= None
        else:        
            value_label_line= '/' + self.name
            sorted_value_names= self.value_mappings.keys()
            sorted_value_names.sort()
            for value_name in sorted_value_names:
                value_label= self.value_mappings[value_name]
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
            if var_label_line != None:
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
        return cls._import(form_dict)
    
    @classmethod
    def _import(cls, form_dict):
        '''
        Where the actual importing work occurs. Takes a form as a dictionary and 
        returns the appropriate :py:class:`VariableMetadata` objects.
        
        :param dict form_dict: The ODK Collect form parsed into a :py:class:`dict`.
        :rtype: list(:py:class:`VariableMetadata`)
        '''
        
        form_variables= form_dict['children']
        variable_metadata_list= list()
        for form_var in form_variables:
            if form_var['type'] == 'group':
                # Recursively import groups.
                group_variable_metadata_list= cls._import(form_var)
                variable_metadata_list.extend(group_variable_metadata_list)
                continue
        
            var_name= form_var['name'].encode('utf-8')
            if 'label' not in form_var.keys():
                var_label= None
            else:
                var_label= form_var['label'].encode('utf-8')
            
            # TODO: Find out multi-select "type" (e.g. "select multiple")
            if form_var['type'] in ['select one']:
                value_mappings_list= form_var['children']
                value_mappings= dict()
                for mapping in value_mappings_list:
                    val_name= mapping['name'].encode('utf-8')
                    val_label= mapping['label'].encode('utf-8')
                    value_mappings[val_name]= val_label
            else:
                value_mappings= None
            
            variable_metadata= cls(var_name, var_label, value_mappings)
            variable_metadata_list.append(variable_metadata)
            
            # TODO: Not really knowing the "calculate" syntax, this is likely very brittle.
            if form_var['type'] == 'calculate':
                calculation_string= form_var['bind']['calculate']
                # Find the first substring of the form "'matched substring:"
                calculated_var_name= re.match(r'''^.+'(.+):''', calculation_string).groups()[0].encode('utf-8')
                calculated_variable_metadata= cls(calculated_var_name, calculated_var_name, None)
                variable_metadata_list.append(calculated_variable_metadata)

        return variable_metadata_list
    