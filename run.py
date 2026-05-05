# -----------------------------------------------------------------------------------
# Author: Eduardo Camargo da Silva
# Created: November 2024
# -----------------------------------------------------------------------------------

from app.src import RumbaClient
from app.config import Logger
from pathlib import Path

log = Logger('run', Path('logs'))

# Exemplo de código
if __name__ == '__main__':
    cics = RumbaClient('D')
    cics.logon_and_go_to_SCOM_A()
    cics.copy_string_to_ps(3, 13, '23825903')
    cics.send_key('ENTER')