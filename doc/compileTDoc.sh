#!/bin/bash
#
# DESRCIPTION: 
# - simple bash script to compile the technical documentation into html and pdf format
# - tested on Kubuntu 16.04
# PRE: xsltproc installed
# - viewer and wkhtmltotox is shipped
BASE_STR="techDocumentation"
xsltproc ~/software/wsdl-viewer_3-1-02/wsdl-viewer.xsl ../src/sbmlmod/SBMLmod.wsdl > $BASE_STR.html
./wkhtmltox/bin/wkhtmltopdf $BASE_STR.html $BASE_STR.pdf
