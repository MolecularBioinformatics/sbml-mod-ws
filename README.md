SBMLmod web service
===================

Dependencies
------------
 - Python > 2.6 (no Python 3 support)
 - [zc.buildout](http://www.buildout.org) `pip install zc.buildout`
 - [Setuptools](https://bitbucket.org/pypa/setuptools/raw/0.8/ez_setup.py) `pip install setuptools`
 - [libSBML](http://sbml.org/Software/libSBML/docs/python-api/libsbml-installation.html) `pip install python-libsbml`


Setup/install
-------------

From within the `sbml_mod_ws` directory (where the `bootstrap.py` file is located) run:

```bash
python bootstrap.py

./bin/buildout

./bin/gencode
```

Configure service (if needed) by editing `parts/etc/pyserver.cfg`. Note that the port in `parts/etc/pyserver.cfg` must correspond to the one defined in the WSDL file `src/sbmlmod/SBMLmod.wsdl`.

To run tests, type `./bin/test`.

Running web service
-------------------

The web service can be started by `./bin/serverd start` or `./bin/serverd debug`. For more serverd parameters, run `./bin/serverd`.

If the service should stop unexpectedly (e.g. by shutting down the computer), you need to clean up the server by running `./bin/serverd stop` before starting it again (with `./bin/serverd start`).

Access service
--------------

The webservice provides an WSDL file (`src/sbmlmod/SBMLmod.wsdl`) that must be made available via some webserver (e.g. Apache or nginx). The file contains a description of the service in an XML format. The service itself can be accessed via SOAP. An example client with further information is provided here `src/testClient`.
