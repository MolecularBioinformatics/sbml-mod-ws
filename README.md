SBMLmod web service
===================

Dependencies
------------
 - Python > 2.6
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

Run tests
---------

`./bin/test`

Running web service
-------------------

The web service can be started by:

`./bin/serverd start`

or:

`./bin/serverd debug`

For serverd parameters:

`./bin/serverd --help`
