## Autor

- **Autor:** Eduardo Camargo da Silva
- **Criação:** Novembro de 2024

## Visão geral

Este projeto automatiza interações com terminais RUMBA utilizando a classe `RumbaClient`.

A automação depende de comunicação com o RUMBA por meio da DLL `ehlapi32.Dll`, localizada em:

```text
C:/Program Files (x86)/Micro Focus/RUMBA/system/ehlapi32.Dll
```

Como essa DLL é 32-bit, o ambiente que acessa diretamente o RUMBA precisa usar **Python 32-bit**.


## Terminais suportados

O código suporta três tipos de terminais, definidos pelo parâmetro `terminal_type` ao instanciar `RumbaClient`.

| Terminal | Exemplo de uso | Uso principal |
|---|---|---|
| `A` | `RumbaClient(terminal_type='A')` | Usado majoritariamente em automações no sistema **RHELP do C1**. |
| `D` | `RumbaClient(terminal_type='D')` | Usado para acesso ao **CICS**. |
| `Z` | `RumbaClient(terminal_type='Z')` | Também usado para acesso ao **CICS**. |

Exemplo:

```python
from app.src import RumbaClient

cics = RumbaClient(terminal_type='D')
```


## Estrutura esperada do projeto

Uma estrutura mínima recomendada é:

```text
projeto/
├─ app/
│  ├─ __init__.py
│  ├─ src.py
│  └─ config.py
├─ logs/
├─ config.ini
├─ run.py
└─ .venv/
```

O arquivo `config.ini` deve ficar na raiz do projeto, ao lado do `run.py`, salvo se o módulo `app.config` estiver configurado para buscar esse arquivo em outro local.

---

## Arquivo `config.ini`

O projeto precisa de um arquivo `config.ini` para centralizar configurações do ambiente, caminhos e parâmetros usados pela automação.

Como o conteúdo exato depende da implementação de `app.config`, abaixo está um modelo sugerido. Ajuste os nomes das seções e chaves conforme o que estiver definido em `app/config.py`.

```ini
[cics]
id = your_id
password = your_password

[rhelp]
id = your_id
password = your_password

[32bit_python]
path = C:/Users/seu_id/AppData/Local/Programs/Python/Python313-32/python.exe
```

---

## Necessidade de duas versões de Python

O projeto deve trabalhar com duas arquiteturas de Python:

| Ambiente | Arquitetura | Uso recomendado |
|---|---:|---|
| Python global 32-bit | 32-bit | Acesso ao RUMBA via `ehlapi32.Dll` e automações que dependem de `pywin32`. |
| Python com `.venv` | 64-bit | Execução do restante do projeto, manipulação de dados e desenvolvimento geral. |

Motivo principal:

- A DLL `ehlapi32.Dll` é 32-bit.
- Bibliotecas Python carregadas no mesmo processo precisam ter arquitetura compatível com o interpretador Python.
- Portanto, o acesso direto ao RUMBA deve ocorrer em Python 32-bit.
- O ambiente 64-bit pode ser usado para rotinas auxiliares, processamento de arquivos e execução geral do projeto.

---

## Verificar versões de Python instaladas

No Windows, use:

```bat
py -0p
```

Esse comando lista as versões de Python disponíveis e seus respectivos caminhos.

Para confirmar a arquitetura de uma versão específica:

```bat
py -3.13-32 -c "import platform; print(platform.architecture())"
py -3.13-64 -c "import platform; print(platform.architecture())"
```

Substitua `3.13` pela versão instalada na máquina, se necessário.

---

## Bibliotecas necessárias

### Instalação das bibliotecas no Python 32-bit global

Use o terminal apontando para a versão 32-bit.  
OBS: troque "a464187" por seu id de usuário.

```bat
C:/Users/a464187/AppData/Local/Programs/Python/Python313-32/python.exe -m pip install --upgrade pip
C:/Users/a464187/AppData/Local/Programs/Python/Python313-32/python.exe -m pip install pywin32 pythoncom
```

### Criar o `.venv` no projeto Python 64-bit

Acesse a pasta do projeto 64-bit:

```bat
cd C:\Caminho\Para\Projeto
```

Crie o ambiente virtual:

```bat
py -m venv .venv
```

Ative o ambiente virtual:

```bat
.venv\Scripts\activate
```

Atualize o `pip`:

```bat
python -m pip install --upgrade pip
```

Instale as bibliotecas necessárias:

```bat
python -m pip install pandas openpyxl pyarrow pyodbc numpy
```
