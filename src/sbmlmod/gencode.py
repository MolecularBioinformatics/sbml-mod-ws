# SBMLmod Web Service
# Copyright (C) 2016 Computational Biology Unit, University of Bergen and
#               Molecular Bioinformatics, UiT The Arctic University of Norway
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os, warnings

import ZSI.generate.commands

from pyserver.config import SERVER_CODE_DIR, WSDL


warnings.filterwarnings('ignore', category=DeprecationWarning)



def generate_server_code():
    args = ["-o", SERVER_CODE_DIR, "-b", WSDL]
    ZSI.generate.commands.wsdl2py(args)
    # args = ["-f", WSDL_FILE, "-o", SERVER_CODE_DIR]
    # ZSI.generate.commands.wsdl2dispatch(args)

if __name__ == '__main__':
    generate_server_code()
