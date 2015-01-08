'''
Created on Jun 13, 2014

.. moduleauthor:: Esmail Fadae <efadae@hotmail.com>
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
    :param dict value_mappings: A dictionary that maps encoded value names (e.g. "0", "1") to value labels (e.g. "Female", "Male")
    '''

    def _to_spss_syntax(self):
        '''
        Output the syntax file lines that correspond to this object. 

        :returns: SPSS-syntax-file-formatted strings for use in a syntax file's "VARIABLE LABELS" and (possibly) "VALUE LABELS" sections.
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
        Export the supplied :py:class:`VariableMetadata` objects to a string for 
        use in an SPSS syntax file.

        :param variable_metadata_list: The metadata to export.
        :type variable_metadata_list: list(:py:class:`VariableMetadata`)
        :returns: An SPSS-syntax-file-formatted string.
        :rtype: :py:class:`String`
        '''

        if len(variable_metadata_list) == 0:
            return ''

        variable_label_lines= list()
        value_label_lines= list()
        for var_metadata in variable_metadata_list:
            var_label_line,  val_label_line= var_metadata._to_spss_syntax()
            if var_label_line != None:
                variable_label_lines.append(var_label_line)
            if val_label_line != None:
                value_label_lines.append(val_label_line)

        # Remove the prepending "/" from the first variable label and value label (if any) lines.
        variable_label_lines[0]= variable_label_lines[0].split('/')[1]
        if value_label_lines:
            value_label_lines[0]= value_label_lines[0].split('/')[1]

        syntax_string= 'VARIABLE LABELS'
        for var_label_line in variable_label_lines:
            syntax_string+= '\n' + var_label_line
        syntax_string+= '.\n'

        # There aren't always value labels to report.
        if len(value_label_lines) != 0:
            syntax_string+= '\nVALUE LABELS'
            for val_label_line in value_label_lines:
                syntax_string+= '\n' + val_label_line
            syntax_string+= '.\n'

        return syntax_string


    @classmethod
    def import_dicts(cls, variable_labels_dict, value_labels_dict):
        variable_metadata_list= list()
        
        # TODO: This doesn't address the (rare) cases of labeled values whose corresponding variable lacks a label.
        for variable_name, variable_label in variable_labels_dict.iteritems():
            value_mappings= value_labels_dict.get(variable_name)
            variable_metadata_list.append(cls(variable_name, variable_label, value_mappings))
        
        return variable_metadata_list


    @classmethod
    def import_json(cls, odk_json_text):
        '''
        Parse question metadata (e.g. names, labels, value mappings) from the 
        supplied JSON-formatted ODK form text.
        
        :param str odk_json_text: The JSON-formatted text of the form being imported.
        :returns: :py:class:`VariableMetadata` objects that correspond to the JSON form's questions.
        :rtype: list(:py:class:`VariableMetadata`) 
        '''
        
        form_dict= json.loads(odk_json_text)
        return cls._import(form_dict)


    @classmethod
    def _import(cls, odk_form_dict):
        '''
        Where the actual importing work occurs. Takes an ODK form pre-parsed 
        into :py:class:`dict` and generates the appropriate metadata.
        returns the appropriate :py:class:`VariableMetadata` objects.
        
        :param dict odk_form_dict: The ODK form parsed into a :py:class:`dict`.
        :returns: :py:class:`VariableMetadata` objects that correspond to the form's questions.
        :rtype: list(:py:class:`VariableMetadata`)
        '''
        
        form_variables= odk_form_dict['children']
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
