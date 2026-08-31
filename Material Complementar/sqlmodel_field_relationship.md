# SQLModel — Referência Completa: `Field` e `Relationship`

> Material de referência técnica para uso com SQLModel + FastAPI.  
> Versão compatível: SQLModel ≥ 0.0.14 / Pydantic v2.

---

## Sumário

1. [Field — Visão Geral](#1-field--visão-geral)
2. [Parâmetros de Coluna do Banco](#2-parâmetros-de-coluna-do-banco)
3. [Parâmetros de Integração com SQLAlchemy](#3-parâmetros-de-integração-com-sqlalchemy)
4. [Parâmetros de Validação Pydantic](#4-parâmetros-de-validação-pydantic)
5. [Mapeamento de Tipos Python → SQLAlchemy](#5-mapeamento-de-tipos-python--sqlalchemy)
6. [Regras de Exclusão Mútua](#6-regras-de-exclusão-mútua)
7. [Relationship — Visão Geral](#7-relationship--visão-geral)
8. [Parâmetros do Relationship](#8-parâmetros-do-relationship)
9. [Padrões de Relacionamento](#9-padrões-de-relacionamento)
10. [Mapeamento SQLModel → SQLAlchemy](#10-mapeamento-sqlmodel--sqlalchemy)
11. [Boas Práticas e Armadilhas Comuns](#11-boas-práticas-e-armadilhas-comuns)

---

## 1. Field — Visão Geral

`Field()` é a função central para definir colunas em um modelo SQLModel. Ela atua como uma ponte entre dois sistemas:

- **Pydantic**: validação e serialização de dados em Python
- **SQLAlchemy**: definição e geração de colunas no banco de dados

Quando o modelo possui `table=True`, cada campo com `Field()` torna-se simultaneamente um atributo Pydantic validado e uma coluna no banco de dados. Em modelos sem `table=True` (data models), `Field()` atua apenas como validador Pydantic.

```python
from sqlmodel import Field, SQLModel
from typing import Optional

class Produto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100, index=True)
    preco: float = Field(gt=0)
    estoque: int = Field(default=0, ge=0)
    categoria_id: int = Field(foreign_key="categoria.id")
```

---

## 2. Parâmetros de Coluna do Banco

Estes parâmetros afetam diretamente a estrutura da tabela gerada no banco de dados.

---

### `default`

**Tipo:** `Any`  
**Padrão:** não definido

Define o valor padrão do campo tanto no Python quanto no banco de dados. O valor é transferido para a coluna SQLAlchemy durante a construção.

```python
# Valor padrão fixo
status: str = Field(default="ativo")

# Campo obrigatório (sem default)
nome: str = Field()

# None explícito — necessário para PKs antes do INSERT
id: int | None = Field(default=None, primary_key=True)
```

> **Por que `default=None` em PKs?** O `id` não existe em memória até o banco gerar o valor após o `commit()`. O tipo `int | None` reflete corretamente esse estado transitório.

---

### `default_factory`

**Tipo:** `Callable[[], Any]`  
**Padrão:** não definido

Função chamada sem argumentos para gerar o valor padrão. Útil para tipos mutáveis como listas, dicionários ou valores dinâmicos como timestamps.

```python
from datetime import datetime

criado_em: datetime = Field(default_factory=datetime.utcnow)
tags: list[str] = Field(default_factory=list)
```

> **Atenção:** Nunca use `default=[]` ou `default={}` — todos os objetos compartilhariam a mesma instância. Use `default_factory=list` / `default_factory=dict`.

---

### `primary_key`

**Tipo:** `bool`  
**Padrão:** `False`

Marca o campo como chave primária da tabela. Chaves primárias nunca são nulas no banco de dados, independente da anotação de tipo.

```python
# Chave primária simples com auto-incremento
id: int | None = Field(default=None, primary_key=True)

# Chave primária UUID
import uuid
id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
```

**Chave primária composta:** múltiplos campos podem ter `primary_key=True`.

```python
class PedidoItem(SQLModel, table=True):
    pedido_id: int = Field(foreign_key="pedido.id", primary_key=True)
    produto_id: int = Field(foreign_key="produto.id", primary_key=True)
    quantidade: int
```

---

### `foreign_key`

**Tipo:** `str`  
**Padrão:** não definido  
**Formato:** `"nome_tabela.nome_coluna"`

Cria uma restrição de chave estrangeira (FOREIGN KEY) no banco. A string deve referenciar o nome real da tabela e coluna no banco (não o nome da classe Python).

```python
# Referência simples
categoria_id: int = Field(foreign_key="categoria.id")

# FK que pode ser nula (relacionamento opcional)
gerente_id: int | None = Field(default=None, foreign_key="funcionario.id")
```

> **Atenção:** O valor da string usa o nome da **tabela no banco**, que por padrão é o nome da classe em `snake_case`. Se a classe usa `__tablename__`, use o valor definido lá.

---

### `ondelete`

**Tipo:** `Literal["CASCADE", "SET NULL", "RESTRICT"]`  
**Padrão:** não definido  
**Requer:** `foreign_key` definido no mesmo campo

Controla o comportamento do banco quando o registro pai é deletado.

| Valor | Comportamento |
|---|---|
| `"CASCADE"` | Deleta automaticamente os registros filhos |
| `"SET NULL"` | Define o campo como `NULL` nos registros filhos |
| `"RESTRICT"` | Impede a deleção se houver registros filhos |

```python
# Deleção em cascata — ao deletar a categoria, deleta os produtos
categoria_id: int = Field(
    foreign_key="categoria.id",
    ondelete="CASCADE"
)

# SET NULL — campo deve aceitar None
categoria_id: int | None = Field(
    default=None,
    foreign_key="categoria.id",
    ondelete="SET NULL"
)
```

> **Regra obrigatória:** Se `ondelete="SET NULL"`, o campo deve ser `int | None` (ou equivalente com `None`). Caso contrário, o banco não conseguirá definir o valor como `NULL`.

---

### `unique`

**Tipo:** `bool`  
**Padrão:** `False`

Cria uma restrição `UNIQUE` na coluna. Tentativas de inserir valores duplicados lançam `IntegrityError`.

```python
email: str = Field(unique=True)
cpf: str = Field(max_length=11, unique=True)
```

> Diferença de `index=True`: `unique` garante unicidade E cria um índice. `index=True` apenas cria o índice sem restrição de unicidade.

---

### `index`

**Tipo:** `bool`  
**Padrão:** não definido

Cria um índice B-tree na coluna, acelerando buscas e filtros (`WHERE`, `ORDER BY`) nesse campo. Não impõe restrição de unicidade.

```python
# Campos frequentemente usados em filtros devem ter índice
nome: str = Field(index=True)
status: str = Field(index=True)
criado_em: datetime = Field(default_factory=datetime.utcnow, index=True)
```

> **Quando usar:** campos usados em cláusulas `WHERE`, `JOIN`, `ORDER BY`. Evite em campos raramente consultados — índices têm custo de escrita.

---

### `nullable`

**Tipo:** `bool`  
**Padrão:** inferido pelo tipo

Controla se a coluna aceita `NULL` no banco. Na maioria dos casos, o SQLModel infere esse valor automaticamente a partir da anotação de tipo:

| Anotação | `nullable` inferido |
|---|---|
| `str` | `False` (NOT NULL) |
| `str \| None` | `True` (NULL permitido) |
| `int` | `False` |
| `int \| None` | `True` |

```python
# Inferido como NOT NULL (str)
nome: str = Field(max_length=100)

# Inferido como NULL (str | None)
apelido: str | None = Field(default=None, max_length=50)

# Override explícito (use com cautela)
codigo: str = Field(nullable=True)  # NOT recomendado — prefira str | None
```

> **Recomendação:** Prefira sempre controlar a nulabilidade pela anotação de tipo (`str | None`) em vez de usar `nullable=True/False` explicitamente. A anotação é a fonte de verdade tanto para o Python quanto para o banco.

---

## 3. Parâmetros de Integração com SQLAlchemy

Estes parâmetros permitem acesso direto à camada SQLAlchemy quando as abstrações do SQLModel não são suficientes.

---

### `sa_type`

**Tipo:** `type[Any]` (tipo SQLAlchemy)

Substitui o tipo SQLAlchemy inferido automaticamente. Útil quando o mapeamento padrão não atende.

```python
from sqlalchemy import Text, JSON
from sqlmodel import Field

# Forçar TEXT em vez de VARCHAR
descricao: str = Field(sa_type=Text)

# Coluna JSON
configuracoes: dict = Field(default_factory=dict, sa_type=JSON)
```

---

### `sa_column`

**Tipo:** `Column` (SQLAlchemy)

Fornece um objeto `Column` completo do SQLAlchemy, sobrescrevendo **todas** as outras configurações de coluna. Oferece controle total sobre a definição da coluna.

```python
from sqlalchemy import Column, String, UniqueConstraint

# Controle total com Column direto
email: str = Field(
    sa_column=Column(String(255), unique=True, nullable=False, index=True)
)
```

> **Atenção:** Ao usar `sa_column`, os parâmetros `primary_key`, `foreign_key`, `unique`, `index`, `nullable`, `sa_type`, `sa_column_args` e `sa_column_kwargs` são **ignorados e proibidos**. O sistema lança `RuntimeError` se combinados.

---

### `sa_column_args`

**Tipo:** `Sequence[Any]`

Argumentos posicionais adicionais passados ao construtor `Column` do SQLAlchemy. Usado para adicionar constraints sem usar `sa_column` completo.

```python
from sqlalchemy import CheckConstraint

preco: float = Field(
    sa_column_args=[CheckConstraint("preco > 0", name="ck_preco_positivo")]
)
```

---

### `sa_column_kwargs`

**Tipo:** `Mapping[str, Any]`

Argumentos nomeados adicionais passados ao construtor `Column`. Permite acessar opções avançadas do SQLAlchemy não expostas diretamente pelo `Field`.

```python
# Comentário na coluna (suportado por alguns bancos)
nome: str = Field(sa_column_kwargs={"comment": "Nome completo do cliente"})
```

---

## 4. Parâmetros de Validação Pydantic

Estes parâmetros atuam apenas na camada Python (Pydantic). Não afetam a estrutura do banco de dados diretamente — exceto `max_length`, que pode influenciar o tamanho de colunas `VARCHAR`.

---

### Restrições de String

```python
nome: str = Field(min_length=2, max_length=100)
codigo: str = Field(pattern=r"^[A-Z]{3}\d{4}$")  # regex
```

| Parâmetro | Efeito |
|---|---|
| `min_length` | Comprimento mínimo da string |
| `max_length` | Comprimento máximo — também define `VARCHAR(n)` no banco |
| `pattern` | Expressão regular que o valor deve satisfazer |

---

### Restrições Numéricas

```python
preco: float = Field(gt=0, le=999999.99)
nota: int = Field(ge=0, le=10)
```

| Parâmetro | Significado | Operador |
|---|---|---|
| `gt` | greater than (maior que) | `>` |
| `ge` | greater or equal (maior ou igual) | `>=` |
| `lt` | less than (menor que) | `<` |
| `le` | less or equal (menor ou igual) | `<=` |

---

### Alias e Documentação

```python
nome_completo: str = Field(
    alias="fullName",              # nome no JSON de entrada
    serialization_alias="name",    # nome no JSON de saída
    title="Nome Completo",         # título no schema OpenAPI
    description="Nome completo do usuário conforme documento"
)
```

| Parâmetro | Uso |
|---|---|
| `alias` | Nome alternativo no JSON de entrada (desserialização) |
| `validation_alias` | Alias apenas para validação de entrada |
| `serialization_alias` | Alias apenas para serialização de saída |
| `title` | Título exibido na documentação OpenAPI |
| `description` | Descrição exibida na documentação OpenAPI |

---

### Controle de Serialização

```python
senha_hash: str = Field(exclude=True)  # nunca aparece na resposta JSON
```

---

## 5. Mapeamento de Tipos Python → SQLAlchemy

O SQLModel converte automaticamente os tipos Python em tipos de coluna SQLAlchemy:

| Tipo Python | Tipo SQLAlchemy | Observação |
|---|---|---|
| `str` | `AutoString` | `VARCHAR(255)` no MySQL, `TEXT` em outros |
| `int` | `Integer` | — |
| `float` | `Float` | — |
| `bool` | `Boolean` | — |
| `datetime` | `DateTime` | — |
| `date` | `Date` | — |
| `time` | `Time` | — |
| `timedelta` | `Interval` | — |
| `Decimal` | `Numeric` | Usa `max_digits` e `decimal_places` |
| `bytes` | `LargeBinary` | — |
| `uuid.UUID` | `Uuid` | — |
| `Enum` subclass | `sa_Enum` | — |
| `EmailStr` | `AutoString` | Tipo Pydantic |

Use `sa_type` para sobrescrever qualquer mapeamento automático.

---

## 6. Regras de Exclusão Mútua

O SQLModel impõe restrições sobre combinações inválidas de parâmetros. Violações lançam `RuntimeError` em tempo de definição da classe.

### Regra 1: `sa_column` é exclusivo

Se `sa_column` for fornecido, nenhum outro parâmetro de coluna SQLModel pode ser usado:

```python
# ❌ RuntimeError — combinação inválida
campo: str = Field(
    sa_column=Column(String(100)),
    unique=True,      # proibido com sa_column
    index=True        # proibido com sa_column
)

# ✅ Correto — tudo dentro do sa_column
campo: str = Field(
    sa_column=Column(String(100), unique=True, index=True)
)
```

### Regra 2: `ondelete` exige `foreign_key`

```python
# ❌ RuntimeError
campo: int = Field(ondelete="CASCADE")  # sem foreign_key

# ✅ Correto
campo: int = Field(foreign_key="tabela.id", ondelete="CASCADE")
```

### Regra 3: `ondelete="SET NULL"` exige tipo nullable

```python
# ❌ Erro no banco — coluna NOT NULL não pode receber NULL
campo: int = Field(foreign_key="tabela.id", ondelete="SET NULL")

# ✅ Correto
campo: int | None = Field(default=None, foreign_key="tabela.id", ondelete="SET NULL")
```

---

## 7. Relationship — Visão Geral

`Relationship()` define atributos de relacionamento entre modelos, fornecendo acesso orientado a objetos a dados relacionados sem a necessidade de escrever JOINs manualmente.

**Importante:** `Relationship` **não cria colunas no banco**. A conexão entre tabelas é feita pelo `Field(foreign_key=...)`. O `Relationship` apenas fornece a interface Python para navegar entre os objetos relacionados.

```python
from sqlmodel import Relationship

class Categoria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    # Um para muitos: uma categoria tem muitos produtos
    produtos: list["Produto"] = Relationship(back_populates="categoria")

class Produto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    categoria_id: int = Field(foreign_key="categoria.id")  # ← coluna real
    # Muitos para um: um produto pertence a uma categoria
    categoria: "Categoria | None" = Relationship(back_populates="produtos")
```

---

## 8. Parâmetros do Relationship

---

### `back_populates`

**Tipo:** `str | None`  
**Padrão:** `None`

Nome do atributo de relacionamento correspondente na classe relacionada. Cria um relacionamento **bidirecional** — modificar um lado atualiza automaticamente o outro na sessão.

```python
class Time(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    # "herois" é o nome do atributo em Heroi
    herois: list["Heroi"] = Relationship(back_populates="time")

class Heroi(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    time_id: int | None = Field(default=None, foreign_key="time.id")
    # "time" é o nome do atributo em Time
    time: "Time | None" = Relationship(back_populates="herois")
```

Efeito em código:

```python
time = Time(nome="Vingadores")
heroi = Heroi(nome="Thor")
heroi.time = time
# time.herois agora contém [heroi] automaticamente
```

---

### `cascade_delete`

**Tipo:** `bool`  
**Padrão:** `False`

Quando `True`, deleta automaticamente os objetos filhos quando o pai é deletado. Traduz para `cascade="all, delete-orphan"` no SQLAlchemy.

```python
class Pedido(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # Ao deletar o pedido, os itens são deletados automaticamente
    itens: list["ItemPedido"] = Relationship(
        back_populates="pedido",
        cascade_delete=True
    )

class ItemPedido(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedido.id")
    pedido: "Pedido | None" = Relationship(back_populates="itens")
```

> **Atenção:** `cascade_delete=True` no `Relationship` controla o comportamento no ORM (Python). Para cascata no banco de dados, use `ondelete="CASCADE"` no `Field` da FK. Para cascata completa, use ambos.

---

### `passive_deletes`

**Tipo:** `bool | Literal["all"]`  
**Padrão:** `False`

Controla como o SQLAlchemy lida com a deleção de objetos relacionados.

| Valor | Comportamento |
|---|---|
| `False` | SQLAlchemy carrega os filhos em memória para processar a deleção |
| `True` | Banco de dados processa a deleção via FK constraint — SQLAlchemy não carrega os filhos |
| `"all"` | Banco cuida de todas as operações de deleção |

```python
# Delegar ao banco — mais eficiente para grandes volumes
itens: list["Item"] = Relationship(
    back_populates="pedido",
    passive_deletes=True
)
```

**Combinação recomendada para deleção eficiente:**

```python
# No lado pai (Relationship):
itens: list["Item"] = Relationship(
    back_populates="pedido",
    passive_deletes=True
)

# No lado filho (Field):
pedido_id: int = Field(
    foreign_key="pedido.id",
    ondelete="CASCADE"
)
```

---

### `link_model`

**Tipo:** `SQLModel` (classe com `table=True`)  
**Padrão:** não definido

Especifica o modelo de tabela intermediária para relacionamentos **muitos-para-muitos**. Traduz para o parâmetro `secondary` do SQLAlchemy.

```python
# Tabela intermediária
class HeroiTime(SQLModel, table=True):
    heroi_id: int | None = Field(
        default=None, foreign_key="heroi.id", primary_key=True
    )
    time_id: int | None = Field(
        default=None, foreign_key="time.id", primary_key=True
    )

class Heroi(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    times: list["Time"] = Relationship(
        back_populates="herois",
        link_model=HeroiTime  # ← tabela intermediária
    )

class Time(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    herois: list["Heroi"] = Relationship(
        back_populates="times",
        link_model=HeroiTime
    )
```

**Requisitos do `link_model`:**
- Deve ter `table=True`
- Deve ter FKs para ambas as tabelas relacionadas
- Normalmente usa chaves primárias compostas

---

### `sa_relationship`

**Tipo:** `RelationshipProperty` (SQLAlchemy)

Fornece um objeto `relationship()` completo do SQLAlchemy, sobrescrevendo toda a configuração do SQLModel. Usado para cenários avançados não suportados pelos parâmetros padrão.

```python
from sqlalchemy.orm import relationship

class Produto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    categorias: list["Categoria"] = Relationship(
        sa_relationship=relationship(
            "Categoria",
            secondary="produto_categoria",
            lazy="selectin",
            order_by="Categoria.nome"
        )
    )
```

> **Atenção:** `sa_relationship` é mutuamente exclusivo com `sa_relationship_args` e `sa_relationship_kwargs`. Usar ambos lança `RuntimeError`.

---

### `sa_relationship_args` e `sa_relationship_kwargs`

Permitem passar argumentos adicionais ao `relationship()` do SQLAlchemy sem precisar construir o objeto completo.

```python
# Controle de carregamento lazy/eager via kwargs
produtos: list["Produto"] = Relationship(
    back_populates="categoria",
    sa_relationship_kwargs={"lazy": "selectin"}
)
```

---

## 9. Padrões de Relacionamento

### Um-para-Muitos (1:N)

```python
class Autor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    livros: list["Livro"] = Relationship(back_populates="autor")

class Livro(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    autor_id: int = Field(foreign_key="autor.id")
    autor: "Autor | None" = Relationship(back_populates="livros")
```

### Um-para-Um (1:1)

```python
class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    perfil: "Perfil | None" = Relationship(back_populates="usuario")

class Perfil(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    bio: str | None = None
    # unique=True garante o 1:1 no banco
    usuario_id: int = Field(foreign_key="usuario.id", unique=True)
    usuario: "Usuario | None" = Relationship(back_populates="perfil")
```

### Muitos-para-Muitos (N:N)

```python
class EstudanteMateria(SQLModel, table=True):
    estudante_id: int | None = Field(
        default=None, foreign_key="estudante.id", primary_key=True
    )
    materia_id: int | None = Field(
        default=None, foreign_key="materia.id", primary_key=True
    )

class Estudante(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    materias: list["Materia"] = Relationship(
        back_populates="estudantes",
        link_model=EstudanteMateria
    )

class Materia(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    estudantes: list["Estudante"] = Relationship(
        back_populates="materias",
        link_model=EstudanteMateria
    )
```

---

## 10. Mapeamento SQLModel → SQLAlchemy

### Field

| Parâmetro SQLModel | Equivalente SQLAlchemy |
|---|---|
| `primary_key=True` | `Column(..., primary_key=True)` |
| `foreign_key="tabela.col"` | `ForeignKey("tabela.col")` |
| `ondelete="CASCADE"` | `ForeignKey(..., ondelete="CASCADE")` |
| `unique=True` | `Column(..., unique=True)` |
| `index=True` | `Column(..., index=True)` |
| `nullable=False` | `Column(..., nullable=False)` |
| `default=valor` | `Column(..., default=valor)` |
| `sa_type=Text` | `Column(Text, ...)` |

### Relationship

| Parâmetro SQLModel | Equivalente SQLAlchemy |
|---|---|
| `back_populates="attr"` | `relationship(..., back_populates="attr")` |
| `cascade_delete=True` | `relationship(..., cascade="all, delete-orphan")` |
| `passive_deletes=True` | `relationship(..., passive_deletes=True)` |
| `link_model=LinkClass` | `relationship(..., secondary=link_table)` |

---

## 11. Boas Práticas e Armadilhas Comuns

### ✅ Prefira anotações de tipo para controlar nulabilidade

```python
# ✅ Claro, consistente, sem parâmetro redundante
campo: str | None = Field(default=None)

# ⚠️ Funciona, mas nullable é frequentemente ignorado no SQLModel
campo: str = Field(nullable=True)
```

### ✅ Use `default_factory` para valores mutáveis

```python
# ✅
criado_em: datetime = Field(default_factory=datetime.utcnow)

# ❌ Todos os objetos compartilham o mesmo datetime
criado_em: datetime = Field(default=datetime.utcnow())
```

### ✅ Sempre use `back_populates` nos dois lados

```python
# ✅ Bidirecional e explícito
class Pai(SQLModel, table=True):
    filhos: list["Filho"] = Relationship(back_populates="pai")

class Filho(SQLModel, table=True):
    pai_id: int = Field(foreign_key="pai.id")
    pai: "Pai | None" = Relationship(back_populates="filhos")
```

### ✅ Combine `cascade_delete` + `ondelete` para deleção completa

```python
# Cascata no ORM (Python)
filhos: list["Filho"] = Relationship(
    back_populates="pai",
    cascade_delete=True
)

# Cascata no banco (SQL)
pai_id: int = Field(foreign_key="pai.id", ondelete="CASCADE")
```

### ⚠️ Forward references com aspas

Quando um modelo referencia outro definido depois no arquivo, use string:

```python
# ✅ Forward reference com aspas
filhos: list["Filho"] = Relationship(back_populates="pai")
filho: "Filho | None" = Relationship(back_populates="pai")
```

### ⚠️ `Relationship` não cria coluna

```python
# ❌ Erro comum — Relationship não cria FK no banco
class Produto(SQLModel, table=True):
    categoria: "Categoria" = Relationship(back_populates="produtos")
    # falta o Field com foreign_key!

# ✅ Correto — FK no Field, navegação no Relationship
class Produto(SQLModel, table=True):
    categoria_id: int = Field(foreign_key="categoria.id")  # coluna real
    categoria: "Categoria | None" = Relationship(back_populates="produtos")
```

### ⚠️ `sa_column` invalida outros parâmetros

```python
# ❌ RuntimeError em tempo de definição
campo: str = Field(sa_column=Column(String(100)), unique=True)

# ✅ Tudo dentro do sa_column
campo: str = Field(sa_column=Column(String(100), unique=True))
```
