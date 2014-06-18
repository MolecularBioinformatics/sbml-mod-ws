import os, warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

import ZSI.generate.commands
from pyserver.config import SERVER_CODE_DIR, WSDL


def generate_server_code():
    args = ["-o", SERVER_CODE_DIR, "-b", WSDL]
    ZSI.generate.commands.wsdl2py(args)
    #args = ["-f", WSDL_FILE, "-o", SERVER_CODE_DIR]
    #ZSI.generate.commands.wsdl2dispatch(args)

if __name__ == '__main__':
    generate_server_code()