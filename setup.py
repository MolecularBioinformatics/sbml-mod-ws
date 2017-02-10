# -*- encoding: UTF-8 -*-
from setuptools import setup, find_packages


version = '1.2.0'

setup(name='sbmlmod',
      version=version,
      description="SBMLmod Web Service",
      author=["Anne-Kristin Stavrum, Sascha Schäuble, Mathias Bockwoldt, Pål Puntervoll, Ines Heiland"],
      author_email=["ines.heiland@uit.no"],
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      install_requires=['ZSI==2.1-a4', 'suds==0.3.9'],
      entry_points="""
          [console_scripts]
          gencode = sbmlmod.gencode:generate_server_code
          serverd = pyserver.serverd:serverd
          test = testsbmlmod.all_tests:main
      """,
      )
