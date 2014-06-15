odk_to_spss_syntax [![Build Status](https://travis-ci.org/esmail/odk_to_spss_syntax.svg?branch=master)](https://travis-ci.org/esmail/odk_to_spss_syntax) [![Coverage Status](https://coveralls.io/repos/esmail/odk_to_spss_syntax/badge.png?branch=master)](https://coveralls.io/r/esmail/odk_to_spss_syntax?branch=master)
==================

 A Python package for parsing question metadata from Open Data Kit forms and exporting that metadata to an SPSS ".sps" syntax file.
 
 To install:
```bash
git clone --depth 1 https://github.com/esmail/odk_to_spss_syntax.git
cd odk_to_spss_syntax
make env && source env/bin/activate # If you don't want to install system-wide.
pip install -e .
```
 
 For execution help:
```
odk_to_spss_syntax -h
```

 Documentation [here](https://esmail.github.io/odk_to_spss_syntax/).