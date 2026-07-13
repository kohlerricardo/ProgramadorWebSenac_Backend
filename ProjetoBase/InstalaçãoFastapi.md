# Tutorial: Instalação da Stack FastAPI

## Índice

- [Tutorial: Instalação da Stack FastAPI](#tutorial-instalação-da-stack-fastapi)
  - [Índice](#índice)
  - [Pré-requisitos](#pré-requisitos)
  - [Criando o ambiente virtual](#criando-o-ambiente-virtual)
    - [Windows (PowerShell)](#windows-powershell)
  - [Instalando o FastAPI e dependências](#instalando-o-fastapi-e-dependências)
    - [Instalação básica](#instalação-básica)
    - [Verificando a instalação](#verificando-a-instalação)
    - [Gerando o arquivo de dependências](#gerando-o-arquivo-de-dependências)
  - [Testando a aplicação](#testando-a-aplicação)
    - [Crie o arquivo main](#crie-o-arquivo-main)
  - [Executando a aplicação](#executando-a-aplicação)
    - [Especificando host e porta](#especificando-host-e-porta)
  - [Testando a API](#testando-a-api)
    - [Ferramenta HttpForge](#ferramenta-httpforge)
    - [Parâmetros úteis do Uvicorn](#parâmetros-úteis-do-uvicorn)
    - [Documentação automática da API (Swagger UI)](#documentação-automática-da-api-swagger-ui)
    - [Documentação alternativa da API (ReDoc)](#documentação-alternativa-da-api-redoc)

---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

- **Python 3.8+** — verifique com `python --version` ou `python3 --version`
- **pip** — gerenciador de pacotes do Python
- **Git** (opcional, mas recomendado)

> **Nota:** É altamente recomendado utilizar um ambiente virtual para isolar as dependências do projeto.

---

## Criando o ambiente virtual

```cmd
mkdir meu-projeto-fastapi
cd meu-projeto-fastapi

python -m venv app

app\Scripts\activate
```

### Windows (PowerShell)

```powershell
mkdir meu-projeto-fastapi
cd meu-projeto-fastapi

python -m venv app

.\app\Scripts\Activate.ps1
```

Quando o ambiente estiver ativo, você verá o nome `(venv)` no início da linha do terminal.

---

## Instalando o FastAPI e dependências

### Instalação básica

```cmd
pip install fastapi[standard]
```
Será instalado a biblioteca FastAPI e suas dependências, em especial o Uvicorn e Pydantic.

O **Uvicorn** é um servidor ASGI utilizado para rodar aplicações FastAPI em desenvolvimento e produção.

O **Pydantic** é uma biblioteca utilizada para validação de dados.

### Verificando a instalação

```cmd
pip show fastapi
pip show uvicorn
```

### Gerando o arquivo de dependências

```cmd
pip freeze > requirements.txt
```

Para instalar as dependências a partir do arquivo gerado em outro ambiente:

```cmd
pip install -r requirements.txt
```

---

## Testando a aplicação

### Crie o arquivo main 

Crie o arquivo `app/main.py` com o seguinte conteúdo:

```python
from fastapi import FastAPI

app = FastAPI(
    title="Minha API",
    description="API de exemplo com FastAPI",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"mensagem": "Olá, FastAPI!"}

```
## Executando a aplicação

```cmd
fastapi dev
```
Isto irá inicializar o servidor de desenvolvimento. Caso prefira especificar servidor e porta, use o comando abaixo.
### Especificando host e porta

```cmd
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```
## Testando a API
Abra o navegador e insira na barra de navegação o endereço:
```http
127.0.0.1
```
Isso irá retornar dados da aplicação na tela do navegador, simples mas funcional para verificar se a API está respondendo as requisições.

Se preferir, instale uma ferramenta de teste de APIs mais robusta

###  Ferramenta HttpForge
É uma ferramenta mais robusta para teste de APIs, permite múltiplas requisições e configuração mais detalhada

1. Crie um novo projeto  
   1. Insira um nome sugestivo - (Minha primeira API, Estudos, etc)
2. Clique em Nova requisição
   1. Insira a URL do recurso
   2. Caso necessário, adicione os parâmetros
   3. Clique em Send
   4. A API responde é é possível analisar o resultado
---

### Parâmetros úteis do Uvicorn

| Parâmetro        | Descrição                                      |
|------------------|------------------------------------------------|
| `--reload`       | Reinicia o servidor ao detectar mudanças       |
| `--host`         | Endereço de escuta (padrão: `127.0.0.1`)       |
| `--port`         | Porta de escuta (padrão: `8000`)               |
| `--workers`      | Número de processos workers (produção)         |
| `--log-level`    | Nível de log: `debug`, `info`, `warning`, etc. |

Após iniciar, o servidor estará disponível em:

```
http://127.0.0.1:8000
```

---



### Documentação automática da API (Swagger UI)

Acesse no navegador:

```
http://127.0.0.1:8000/docs
```

### Documentação alternativa da API (ReDoc)

```
http://127.0.0.1:8000/redoc
```
