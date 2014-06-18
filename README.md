SBMLmod web service
===================

Setup/install
-------------

From within the pywstemplate directory (where the bootstrap.py file is located) run:

`> python bootstrap.py`

`> ./bin/buildout`

To generate web service stub code:

`> ./bin/gencode`

Configure service (if needed) by editing pyserver.cfg. Note that the port in pyserver.cfg must correspond to the one defined in the WSDL file.

Running web service
-------------------

The web service can be started by:

`> ./bin/serverd start`

For serverd parameters:

`> ./bin/serverd --help`
