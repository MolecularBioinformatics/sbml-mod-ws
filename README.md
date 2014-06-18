SBMLmod web service
===================

Dependencies
------------
 - Python > 2.6
 - [Setuptools](https://bitbucket.org/pypa/setuptools/raw/0.8/ez_setup.py)
 - [libSBML](http://sbml.org/Software/libSBML/docs/python-api/libsbml-installation.html)


Setup/install
-------------

From within the pywstemplate directory (where the bootstrap.py file is located) run:

`python bootstrap.py`

`./bin/buildout`

To generate web service stub code:

`./bin/gencode`

Configure service (if needed) by editing pyserver.cfg. Note that the port in pyserver.cfg must correspond to the one defined in the WSDL file.

Running web service
-------------------

The web service can be started by:

`./bin/serverd start`

or:

`./bin/serverd debug`

For serverd parameters:

`./bin/serverd --help`
