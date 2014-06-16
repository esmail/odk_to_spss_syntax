#!/usr/bin/env python2.7
# encoding: utf-8
'''
Created on Jun 13, 2014

Provides the outward interface of the package for ingesting input and producing 
output.

.. moduleauthor:: Esmail Fadae <efadae@hotmail.com>
'''

import sys
import os
import argparse

from variable_metadata import VariableMetadata


__all__ = []
# __version__ = __version__
__date__ = '2014-06-15'
__updated__ = '2014-06-15'


def from_json(json_text):
    '''
    Extract the question metadata 
    
    :param str json_text:
    '''
    
    variable_metadata_list= VariableMetadata.import_json(json_text)
    spss_syntax_string= VariableMetadata.export_spss_syntax(variable_metadata_list)
    
    return spss_syntax_string


def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    from odk_to_spss_syntax import __version__
    
    if argv is None:
        # Strip off the program name.
        argv = sys.argv[1:]
        
    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('odk_to_spss_syntax').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Esmail Fadae on %s.
  Copyright 2014 Esmail Fadae. All rights reserved.

  Licensed under the GPL v3
  http://www.gnu.org/copyleft/gpl.html

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    # Setup argument parser
    parser = argparse.ArgumentParser(description=program_license
                                     , formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', type=argparse.FileType('r'), help='The ODK form file to parse.')
    parser.add_argument('outfile', type=argparse.FileType('w'), help='The SPSS syntax file to output.')
    group= parser.add_mutually_exclusive_group()
    group.add_argument('--json', action='store_true', default=True
                       , help='Treat the input file as a JSON-formatted ODK form [implicit default].')
#     # TODO
#     group.add_argument('--xml', action='store_true'
#                        , help='Treat the input file as XML-formatted.')
#     group.add_argument('--xls', action='store_true'
#                        , help='Treat the input file as XLS-formatted.')
    parser.add_argument('-V', '--version', action='version', version=program_version_message)

    # Process arguments
    args = parser.parse_args(argv)
    
    json_form_text= args.infile.read()
    args.infile.close()
    
    spss_syntax_text= from_json(json_form_text)
    args.outfile.write(spss_syntax_text)
    args.outfile.close()


if __name__ == "__main__":
    sys.exit(main())