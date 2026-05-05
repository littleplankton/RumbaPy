# -----------------------------------------------------------------------------------
# Author: Eduardo Camargo da Silva
# Created: November 2024
# Requirements:
#   - Python 32-bit
#   - Dependencies: pywin32 (pip install pywin32)
#   - Standard DLL path: C:/Program Files (x86)/Micro Focus/RUMBA/system/ehlapi32.Dll
# -----------------------------------------------------------------------------------

from app.src import RumbaClient
from app.config import Logger
from pathlib import Path
import pandas as pd
import sys

"""
O código suporta 3 diferentes tipos de terminais:
    A: RumbaClient(terminal_type='A')
    D: RumbaClient(terminal_type='D')
    Z: RumbaClient(terminal_type='Z')

O terminal A é usado majoritariamente em altomações
no sistema RHELP do C1. Equanto D e Z são terminais
usados para o CICS.
"""

log = Logger('rumba_operations', Path('logs'))

# Função de exemplo de código, deletar depois.
def custo_std(working_file: Path) -> pd.DataFrame:
    df = pd.read_csv(working_file, sep=';', dtype=str)
    df = df.loc[df['PN'].notna()]

    cics = RumbaClient(terminal_type='D')

    cics.logon_cics()
    cics.copy_string_to_ps(1, 2, 'SPRE')
    cics.send_key('ENTER')
    cics.screen_load(y=1, x=2, text='VOLVO')
    cics.copy_string_to_ps(22, 10, 'P')
    cics.send_key('ENTER')
    cics.screen_load(y=1, x=74, text='SP3114T')

    res_df = pd.DataFrame(columns=[
        'PN', 'MSG_MAIN', 'MSG_DETAIL', 'STATUS'
    ])

    for idx, row in df.iterrows():
        pn = str(row['PN'])
        status = ""
        msg = ""
        msg1 = ""
        try:
            cics.send_key('F10')
            cics.copy_string_to_ps(3, 14, pn)
            cics.send_key('ENTER')

            cics.copy_string_to_ps(14, 45, row['CUSTO_STD'].rjust(16, ' '))
            cics.send_key('ENTER')
            msg = cics.copy_ps_to_string(23, 7, 74).strip()
            cics.send_key('F6')

            cics.copy_string_to_ps(6,  26, row['EMBALAGEM'].rjust(10, ' '))
            cics.copy_string_to_ps(7,  26, row['FRETE'].rjust(10, ' '))
            cics.copy_string_to_ps(8,  26, row['GARANTIA'].rjust(10, ' '))
            cics.copy_string_to_ps(9,  26, row['C_DPTO_COM'].rjust(10, ' '))
            cics.copy_string_to_ps(10, 26, row['MAO_DE_OBRA'].rjust(10, ' '))
            cics.copy_string_to_ps(11, 26, row['MAT_DIRETO'].rjust(10, ' '))

            cics.send_key('ENTER')
            msg1 = cics.copy_ps_to_string(23, 7, 74).strip()

            cics.send_key('F11')
            status = "Sucesso"
        except Exception as e:
            status = f'Falha ao processar o PN {pn} erro: {e}'

        res_df.loc[len(res_df)] = {
            'PN': pn,
            'MSG_MAIN': msg,
            'MSG_DETAIL': msg1,
            'STATUS': status
        }
    return res_df
