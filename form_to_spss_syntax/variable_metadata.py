'''

Created on Jun 13, 2014

@author: Esmail Fadae
'''
from collections import namedtuple

class VariableMetadata(namedtuple('_VariableMetadata', 'name, label, value_mappings')):
    '''
    A :py:class:`VariableMetadata` object contains the metadata about an 
    individual form variable. The class inherits from a semi-anonymous 
    :py:func:`namedtuple` (:py:func:`_VariableMetadata`) that handles object 
    construction and the creation of immutable attribute accessors.
    
    :param str name: The encoded name of the variable (e.g. "a01")
    :param str label: The variable's readable label (e.g. "What is your sex?")
    :param dict value_mappings: A dictionary that maps encoded value names (e.g.  
    "0", "1") to value labels (e.g. "Female", "Male")
    '''

    def export_spss_syntax(self):
        '''
        Export the metadata for a single variable to the SPSS ".sps" syntax file 
        format.
        
        :returns: The syntax specification text.
        :rtype: str
        '''
        
        syntax_string= 'VARIABLE LABELS\n'
        
        variable_label_line= self.name + ' "' + self.label + '"'
        syntax_string+= variable_label_line + '\n'
        
        syntax_string+= '\n'
        syntax_string+= 'VALUE LABELS\n'
        
        value_label_line= '/' + self.name
        for value_name, value_label in self.value_mappings.iteritems():
            value_label_line+= ' ' + value_name + ' "' + value_label + '"'
        syntax_string+= value_label_line
        
        return syntax_string
