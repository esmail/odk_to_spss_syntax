odk_to_spss_syntax [![Build Status](https://travis-ci.org/esmail/odk_to_spss_syntax.svg?branch=master)](https://travis-ci.org/esmail/odk_to_spss_syntax) [![Coverage Status](https://coveralls.io/repos/esmail/odk_to_spss_syntax/badge.png?branch=master)](https://coveralls.io/r/esmail/odk_to_spss_syntax?branch=master)
==================

 A Python 2.7 package for parsing question metadata from [Open Data Kit](http://opendatakit.org/) and compatible (e.g. [KoBo Toolbox](http://www.kobotoolbox.org/))  forms and exporting that metadata to an SPSS ".sps" syntax file.
 
 To install:
```bash
git clone --depth 1 https://github.com/esmail/odk_to_spss_syntax.git
cd odk_to_spss_syntax
make env && source env/bin/activate # If you don't want to install system-wide.
pip install -e .
```
 
 For execution help:
```bash
odk_to_spss_syntax -h
```

 You can also import and use the package from other Python code as follows:
```python
import odk_to_spss_syntax
json_form_text= open('odk_form.json', 'r').read()
syntax_text= odk_to_spss_syntax.from_json(json_form_text)
```

 Documentation [here](https://esmail.github.io/odk_to_spss_syntax/).
