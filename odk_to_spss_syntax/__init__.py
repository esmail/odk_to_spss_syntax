#!/usr/bin/env python2.7
# encoding: utf-8
'''
odk_to_spss_syntax -- Produce a SPSS syntax file that corresponds to the provided ODK form.

odk_to_spss_syntax is a Python package for extracting metadata about the questions contained in an Open Data Kit form and exporting that metadata to an SPSS ".sps" syntax file.

.. moduleauthor:: Esmail Fadae <efadae@hotmail.com>

@copyright:  2014 Esmail Fadae. All rights reserved.

@license:    GPL v3

@deffield    updated: 2014-06-15
'''

from main import from_json
from main import from_dicts


__version__= '0.1'


if __name__ == '__main__':
    from main import main
    from sys import exit
    exit(main())