# Author: M.L. Souza

"""
This is a command line implementation of SIFTER.
"""

import sys
from UserInterface.cli import PySifterCli

if __name__ == '__main__':
    sifter_instance = PySifterCli()
    sifter_instance.cli_run(sys.argv[1:])