# -*- encoding: UTF-8 -*-
from setuptools import setup, find_packages

version = '0.1.5'

setup(name='sbmledit',
      version=version,
      description="Python Web Service Template",
      author=["Siv Hollup and Anne-Kristin Stavrum"],
      author_email=["annes@ii.uib.no"],
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      install_requires=['ZSI==2.1-a4','suds==0.3.9'],
      entry_points="""
          [console_scripts]
          gencode = sbmledit.gencode:generate_server_code
          serverd = pyserver.serverd:serverd
          client = pyclient.SBMLEditClient:main
      """,
      )