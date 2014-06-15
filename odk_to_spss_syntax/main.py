#!/usr/local/bin/python2.7
# encoding: utf-8
'''
odk_to_spss_syntax.main -- Export a SPSS syntax file that corresponds to an ODK form.

odk_to_spss_syntax.main is a Python package for parsing question metadata from an Open Data Kit form and exporting that metadata to an SPSS ".sps" syntax file

@author:     Esmail Fadae

@copyright:  2014 Esmail Fadae. All rights reserved.

@license:    GPL v3

@contact:    efadae@hotmail.com
@deffield    updated: 2014-06-15
'''

import sys
import os
import argparse

from variable_metadata import VariableMetadata
from __init__ import __version__


__all__ = []
# __version__ = __version__
__date__ = '2014-06-15'
__updated__ = '2014-06-15'


def from_json(json_text):
    '''
    Create an SPSS ".sps" syntax file based on form variable metadata from the 
    provided JSON-formatted ODK Collect form.
    
    :param str json_text:
    '''
    
    variable_metadata_list= VariableMetadata.import_json(json_text)
    spss_syntax_string= VariableMetadata.export_spss_syntax(variable_metadata_list)
    
    return spss_syntax_string


def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    # FIXME: Hideous.
    module_path= os.path.realpath(__file__)
    module_dir= os.path.dirname(module_path)
    module_name= os.path.splitext(os.path.basename(module_path))[0]
    sys.path.insert(0, os.path.abspath(module_dir))
    program_shortdesc = __import__(module_name).__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2014 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

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