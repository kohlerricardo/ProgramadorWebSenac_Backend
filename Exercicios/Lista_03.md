# Exercícios de Modelagem de Objetos para APIs com FastAPI

> **Objetivo:** Modelar classes Python utilizando **Encapsulamento** (atributos protegidos/privados, *getters*, *setters* e *propriedades calculadas*) e implementar rotas FastAPI para cada situação descrita.  

> **Para cada exercício:** analisar as necessidades de proteção de dados e regras de negócio, defina os atributos e propriedades da classe e implemente as rotas indicadas.

---

### Exercício 01 — Ficha de aluno

Você foi contratado para criar o sistema de cadastro de alunos de uma escola. Cada aluno possui nome, matrícula, curso e e-mail.

#### Validações necessárias:
* **E-mail:** O e-mail não pode ser alterado diretamente para qualquer texto; deve passar por uma validação para garantir que possui um formato válido (contendo `@` e domínio).
* **Matrícula:** Trata-se de um identificador imutável gerado na matrícula. Deve ser acessível apenas para leitura.
* **Propriedade Calculada (`dominio_email`):** Uma propriedade que extrai dinamicamente o domínio do e-mail do aluno (ex: `escola.edu.br`).

**Atributos e Propriedades:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `nome` | `str` |  (Não pode ser vazio) |
| `matricula` | `str` | Somente Leitura (Definida na inicialização) |
| `curso` | `str` |  |
| `email` | `str` |  com validação de formato (`@`) |
| `dominio_email` | `str` | **Propriedade Calculada:** Extrai o domínio a partir do e-mail |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/alunos` | Lista todos os alunos |
| `GET` | `/alunos/{id}` | Retorna um aluno específico |
| `POST` | `/alunos` | Cadastra um novo aluno |
| `PUT` | `/alunos/{id}` | Atualiza os dados do aluno |

---

### Exercício 02 — Cardápio de lanchonete

Uma lanchonete quer exibir o cardápio na internet. Cada item tem nome, descrição, preço e status de disponibilidade.

#### Validações necessárias:
* **Preço:** Não pode ser negativo nem igual a zero. Alterações de preço devem ser validadas.
* **Propriedade Calculada (`preco_formatado`):** Retorna o preço formatado em moeda local (ex: `"R$ 25,50"`).
* **Disponibilidade:** Alterar a disponibilidade deve validar se o item possui preço válido antes de ser ativado.

**Atributos e Propriedades:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `nome` | `str` |  |
| `descricao` | `str` |  |
| `preco` | `float` |  (Validação valor $> 0$) |
| `disponivel` | `bool` |  |
| `preco_formatado` | `str` | **Propriedade Calculada:** Retorna string formatada como `R$ X,XX` |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/cardapio` | Lista todos os itens |
| `GET` | `/cardapio?disponivel=true` | Filtra apenas os disponíveis |
| `POST` | `/cardapio` | Adiciona novo item |
| `PUT` | `/cardapio/{id}/disponibilidade` | Marca como disponível ou não |

---

### Exercício 03 — Agenda de contatos

Você precisa criar uma agenda digital simples com nome, telefone e e-mail de cada contato.

#### Validações necessárias:
* **Telefone:** Deve ser sanitizado e validado, aceitando apenas dígitos e garantindo o tamanho padrão.
* **Propriedade Calculada (`inicial_nome`):** Retorna a letra inicial do nome em maiúsculo para fins de ordenação/agrupamento na interface.

**Atributos e Propriedades:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `nome` | `str` |  (Capitaliza automaticamente) |
| `telefone` | `str` |  (Filtra apenas números e valida tamanho) |
| `email` | `str` |  |
| `inicial_nome` | `str` | **Propriedade Calculada:** Retorna a primeira letra do nome |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/contatos` | Lista todos os contatos |
| `GET` | `/contatos?nome=Maria` | Busca por nome parcial |
| `POST` | `/contatos` | Adiciona um contato |
| `DELETE` | `/contatos/{id}` | Remove um contato |

---

### Exercício 04 — Catálogo de filmes

Um cineclube quer organizar os filmes que assistiram, armazenando título, diretor, ano de lançamento e gênero.

#### Validações necessárias:
* **Ano de Lançamento:** Não pode ser no futuro nem anterior à invenção do cinema (ex: 1888).
* **Propriedade Calculada (`idade_filme`):** Calcula quantos anos o filme possui com base no ano atual.

**Atributos e Propriedades:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `titulo` | `str` |  |
| `diretor` | `str` |  |
| `ano` | `int` |  (Valida faixa $1888 \le ano \le ano\_atual$) |
| `genero` | `str` |  |
| `idade_filme` | `int` | **Propriedade Calculada:** Anos desde o lançamento |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/filmes` | Lista todos os filmes |
| `GET` | `/filmes?genero=drama` | Filtra por gênero |
| `GET` | `/filmes/{id}` | Detalhes de um filme |
| `POST` | `/filmes` | Cadastra novo filme |

---

### Exercício 05 — Lista de tarefas

Um aplicativo de produtividade precisa gerenciar tarefas com título, descrição, status e data de criação.

#### Validações necessárias:
* **Status Concluída:** A transição de status deve registrar internamente a data de conclusão.
* **Propriedade Calculada (`status_texto`):** Retorna `"Concluída"` ou `"Pendente"`.
* **Propriedade Calculada (`dias_em_aberto`):** Calcula quantos dias a tarefa está aberta caso não tenha sido concluída.

**Atributos e Propriedades:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `titulo` | `str` |  |
| `descricao` | `str` |  |
| `concluida` | `bool` |  (Modificar para `True` ajusta `data_conclusao`) |
| `criada_em` | `datetime` | Somente Leitura |
| `status_texto` | `str` | **Propriedade Calculada:** Retorna rótulo amigável |
| `dias_em_aberto` | `int` | **Propriedade Calculada:** Dias decorridos desde a criação |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/tarefas` | Lista todas as tarefas |
| `GET` | `/tarefas?concluida=false` | Lista apenas as pendentes |
| `POST` | `/tarefas` | Cria nova tarefa |
| `PUT` | `/tarefas/{id}/concluir` | Marca como concluída |

---

### Exercício 06 — Registro de notas

Um professor precisa de um sistema para lançar notas de alunos por disciplina.

#### Validações necessárias:
* **Valor da Nota:** Deve estar estritamente entre `0.0` e `10.0`. Lançamentos fora dessa faixa devem ser rejeitados.
* **Propriedade Calculada (`situacao`):** Retorna `"Aprovado"` se a nota for $\ge 7.0$, `"Recuperação"` entre $5.0$ e $6.9$, e `"Reprovado"` se $< 5.0$.

**Atributos e Propriedades:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `aluno_id` | `int` | Somente Leitura |
| `disciplina` | `str` |  |
| `valor` | `float` |  (Valida intervalo entre $0.0$ e $10.0$) |
| `data_lancamento` | `date` | Somente Leitura |
| `situacao` | `str` | **Propriedade Calculada:** Avalia situação com base na nota |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/notas` | Lista todas as notas |
| `GET` | `/notas?aluno_id=5` | Notas de um aluno específico |
| `POST` | `/notas` | Lança nova nota |
| `PUT` | `/notas/{id}` | Corrige uma nota lançada |

---

### Exercício 07 — Acervo de livros

Uma biblioteca comunitária quer catalogar seus livros (título, autor, ISBN e exemplares em estoque).

#### Validações necessárias:
* **ISBN:** Deve passar por validação de formato (apenas números e hífens com tamanho válido).
* **Exemplares:** Não pode ter valor negativo.
* **Propriedade Calculada (`em_estoque`):** Propriedade booleana calculada que retorna `True` se `exemplares > 0`.

**Atributos e Propriedades:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `titulo` | `str` |  |
| `autor` | `str` |  |
| `isbn` | `str` |  (Valida formato ISBN) |
| `exemplares` | `int` |  (Valida valor $\ge 0$) |
| `em_estoque` | `bool` | **Propriedade Calculada:** Retorna `exemplares > 0` |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/livros` | Lista todo o acervo |
| `GET` | `/livros?autor=Machado` | Busca por autor |
| `GET` | `/livros/{id}` | Detalhes de um livro |
| `POST` | `/livros` | Adiciona livro ao acervo |
| `PUT` | `/livros/{id}` | Atualiza informações do livro |

---

### Exercício 08 — Catálogo de plantas

Um viveiro publica seu catálogo online com plantas, preços e dados de cultivo.

#### Validações necessárias:
* **Nome Científico:** Deve ser automaticamente formatado em itálico/capitalizado apropriadamente.
* **Preço:** Deve ser maior que zero.
* **Propriedade Calculada (`categoria_porte`):** Classificação baseada no tipo de planta.

**Atributos e Propriedades:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `nome_popular` | `str` |  |
| `nome_cientifico` | `str` |  (Formatação padronizada) |
| `tipo` | `str` |  |
| `preco` | `float` |  (Valida preço $> 0$) |
| `em_estoque` | `bool` |  |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/plantas` | Lista todas as plantas |
| `GET` | `/plantas?tipo=suculenta` | Filtra por tipo |
| `GET` | `/plantas?em_estoque=true` | Apenas disponíveis |
| `POST` | `/plantas` | Cadastra nova planta |
| `PUT` | `/plantas/{id}` | Atualiza dados da planta |

---

### Exercício 09 — Registro de animais do abrigo

Um abrigo de animais registra os pets resgatados.

#### Validações necessárias:
* **Idade:** Não pode ser negativa.
* **Status Adoção:** Uma vez marcado como adotado, impede que certos dados do animal sejam alterados sem reabertura de processo.
* **Propriedade Calculada (`fase_vida`):** Retorna `"Filhote"`, `"Adulto"` ou `"Idoso"` com base na idade e espécie.

**Atributos e Propriedades:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `nome` | `str` |  |
| `especie` | `str` |  |
| `raca` | `str` |  |
| `idade` | `int` |  (Valida idade $\ge 0$) |
| `adotado` | `bool` |  |
| `fase_vida` | `str` | **Propriedade Calculada:** Derivada da idade e espécie |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/animais` | Lista todos os animais |
| `GET` | `/animais?adotado=false` | Apenas disponíveis para adoção |
| `GET` | `/animais/{id}` | Detalhes de um animal |
| `POST` | `/animais` | Registra novo animal resgatado |
| `PUT` | `/animais/{id}/adotar` | Marca animal como adotado |

---

### Exercício 10 — Catálogo de cursos online

Plataforma de cursos online gerencia disciplinas, carga horária e valores.

#### Validações necessárias:
* **Carga Horária:** Deve ser um número inteiro positivo (mínimo de 1 hora).
* **Nível:** Deve aceitar apenas os valores restritos: `"iniciante"`, `"intermediario"`, `"avancado"`.
* **Propriedade Calculada (`valor_por_hora`):** Retorna o custo por hora do curso (`preco / carga_horaria`).

**Atributos e Propriedades:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `titulo` | `str` |  |
| `instrutor` | `str` |  |
| `carga_horaria` | `int` |  (Valida valor $> 0$) |
| `nivel` | `str` |  (Valida valores permitidos) |
| `preco` | `float` |  (Valida valor $\ge 0$) |
| `valor_por_hora` | `float` | **Propriedade Calculada:** `preco / carga_horaria` |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/cursos` | Lista todos os cursos |
| `GET` | `/cursos?nivel=iniciante` | Filtra por nível |
| `GET` | `/cursos/{id}` | Detalhes do curso |
| `POST` | `/cursos` | Cadastra novo curso |
| `DELETE` | `/cursos/{id}` | Remove um curso do catálogo |

---

### Exercício 11 — Inventário de equipamentos de TI

O setor de TI controla o patrimônio de hardware da empresa.

#### Validações necessárias:
* **Patrimônio:** Código imutável com padrão alfanumérico específico.
* **Situação:** Permitir apenas transições válidas de estado (`"ativo"`, `"em manutenção"`, `"descartado"`).
* **Propriedade Calculada (`necessita_substituicao`):** Retorna `True` se a situação for `"descartado"` ou se estiver em manutenção por mais de um período crítico.

**Atributos e Propriedades:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `patrimonio` | `str` | Somente Leitura (Definido no cadastro) |
| `descricao` | `str` |  |
| `localizacao` | `str` |  |
| `situacao` | `str` |  (Valida valores válidos de estado) |
| `necessita_substituicao`| `bool` | **Propriedade Calculada:** Avalia status de descarte/manutenção |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/equipamentos` | Lista todos os equipamentos |
| `GET` | `/equipamentos?situacao=ativo` | Filtra por situação |
| `GET` | `/equipamentos/{id}` | Detalhe do equipamento |
| `POST` | `/equipamentos` | Cadastra novo equipamento |
| `PUT` | `/equipamentos/{id}/situacao` | Atualiza a situação |

---

### Exercício 12 — Diário de leituras

Registro pessoal de livros lidos e em andamento.

#### Validações necessárias:
* **Avaliação:** Só pode ser atribuída se a leitura foi concluída (`data_fim` preenchida) e o valor deve estar entre 1 e 5.
* **Data Fim:** Não pode ser anterior à `data_inicio`.
* **Propriedade Calculada (`concluida`):** Retorna `True` se `data_fim` não for nula.
* **Propriedade Calculada (`dias_de_leitura`):** Duração total da leitura em dias.

**Atributos e Propriedades:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `titulo` | `str` |  |
| `autor` | `str` |  |
| `data_inicio` | `date` |  |
| `data_fim` | `date` ou `None` |  (Valida $\ge data\_inicio$) |
| `avaliacao` | `int` ou `None` |  (Exige `data_fim` e valida $1 \le nota \le 5$) |
| `concluida` | `bool` | **Propriedade Calculada:** Check de preenchimento da `data_fim` |
| `dias_de_leitura` | `int` | **Propriedade Calculada:** Diferença em dias entre início e fim/hoje |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/leituras` | Lista todas as leituras |
| `GET` | `/leituras?concluida=true` | Apenas leituras finalizadas |
| `GET` | `/leituras/{id}` | Detalhes de uma leitura |
| `POST` | `/leituras` | Registra nova leitura |
| `PUT` | `/leituras/{id}/concluir` | Marca como concluída com data e avaliação |

---

### Exercício 13 — Cardápio nutricional

Publicação de opções de refeições para acompanhamento nutricional.

#### Validações necessárias:
* **Calorias:** Valor obrigatoriamente positivo.
* **Ingredientes:** A lista de ingredientes deve ser protegida contra modificações diretas (retornar cópia no getter).
* **Propriedade Calculada (`densidade_calorica`):** Classificação da refeição (`"Leve"`, `"Moderada"`, `"Hipercalórica"`).

**Atributos e Propriedades:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `nome` | `str` |  |
| `tipo` | `str` |  |
| `calorias` | `int` |  (Valida valor $> 0$) |
| `ingredientes` | `list[str]` |  (Retorna cópia para evitar mutação indevida) |
| `densidade_calorica` | `str` | **Propriedade Calculada:** Retorna nível calórico |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/refeicoes` | Lista todas as refeições |
| `GET` | `/refeicoes?tipo=almoco` | Filtra por tipo |
| `GET` | `/refeicoes?max_calorias=500` | Filtra por limite calórico |
| `POST` | `/refeicoes` | Cadastra nova refeição |
| `DELETE` | `/refeicoes/{id}` | Remove uma refeição |

---

## Nível 2 — Intermediário

> Objetos relacionados com regras de integridade e cálculos que combinam atributos.

---

### Exercício 14 — Sistema de reserva de mesas

Controle de mesas e agendamentos em um restaurante.

#### Validações necessárias:
* **Reserva -> Pessoas:** A quantidade de pessoas da reserva não pode ultrapassar a capacidade da mesa vinculada.
* **Mesa -> Capacidade:** Deve ser maior que zero.
* **Propriedade Calculada (`mesa_ocupada`):** Verifica dinamicamente se a mesa possui reservas confirmadas na data/horário atual.

**Atributos e Propriedades — Mesa:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `numero` | `int` |  |
| `capacidade` | `int` |  (Valida valor $> 0$) |

**Atributos e Propriedades — Reserva:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `mesa_id` | `int` | Somente Leitura |
| `cliente_nome` | `str` |  |
| `data` | `date` |  (Não permite datas passadas) |
| `horario` | `str` |  |
| `pessoas` | `int` |  (Valida $\le$ capacidade da mesa) |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/mesas` | Lista todas as mesas |
| `GET` | `/mesas/disponiveis?data=2024-08-10` | Mesas disponíveis em uma data |
| `POST` | `/reservas` | Realiza uma reserva |
| `DELETE` | `/reservas/{id}` | Cancela uma reserva |
| `GET` | `/mesas/{id}/reservas` | Reservas de uma mesa específica |

---

### Exercício 15 — Biblioteca com empréstimos

Empréstimo de livros para leitores cadastrados.

#### Validações necessárias:
* **Empréstimo -> Status do Livro:** O empréstimo só pode ser efetuado se o livro estiver marcado como `disponivel == True`. Ao emprestar, a disponibilidade do livro deve ser alterada internamente.
* **Propriedade Calculada (`em_atraso`):** Verifica se a data atual é posterior à `data_prevista` sem ter havido devolução.

**Atributos e Propriedades — Livro:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `titulo` | `str` |  |
| `autor` | `str` |  |
| `disponivel` | `bool` |  (Acesso controlado por operações de empréstimo) |

**Atributos e Propriedades — Emprestimo:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `livro_id` | `int` | Somente Leitura |
| `leitor_nome` | `str` |  |
| `data_emprestimo` | `date` | Somente Leitura |
| `data_prevista` | `date` |  (Deve ser pós data de empréstimo) |
| `em_atraso` | `bool` | **Propriedade Calculada:** Comparação de `data_prevista` com a data atual |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/livros` | Lista o acervo |
| `GET` | `/livros?disponivel=true` | Apenas disponíveis |
| `POST` | `/emprestimos` | Realiza empréstimo |
| `PUT` | `/emprestimos/{id}/devolver` | Registra devolução |
| `GET` | `/livros/{id}/historico` | Histórico de empréstimos do livro |

---

### Exercício 16 — Controle de ponto de funcionários

Registro de horários de trabalho de funcionários.

#### Validações necessárias:
* **Horário de Saída:** A saída deve ser obrigatoriamente posterior ao horário de entrada.
* **Propriedade Calculada (`horas_trabalhadas`):** Propriedade derivada do cálculo `(saida - entrada)` convertida para horas decimais.
* **Propriedade Calculada (`ponto_aberto`):** Retorna `True` se houver entrada registrada sem saída equivalente.

**Atributos e Propriedades — Funcionario:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `nome` | `str` |  |
| `cargo` | `str` |  |
| `departamento` | `str` |  |

**Atributos e Propriedades — RegistroPonto:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `funcionario_id` | `int` | Somente Leitura |
| `entrada` | `datetime` | Somente Leitura |
| `saida` | `datetime` ou `None` |  (Valida se $> entrada$) |
| `horas_trabalhadas` | `float` ou `None` | **Propriedade Calculada:** Diferença calculada entre entrada e saída |
| `ponto_aberto` | `bool` | **Propriedade Calculada:** Retorna `True` se `saida is None` |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/funcionarios` | Lista funcionários |
| `POST` | `/funcionarios/{id}/entrada` | Registra horário de entrada |
| `PUT` | `/funcionarios/{id}/saida` | Registra saída e calcula horas |
| `GET` | `/funcionarios/{id}/ponto?data=2024-08-10` | Ponto de um dia específico |

---

### Exercício 17 — Pedidos de uma loja virtual

Gerenciamento de vendas, estoque de produtos e cálculo de itens.

#### Validações necessárias:
* **ItemPedido -> Estoque:** Adicionar um item valida se o produto possui quantidade suficiente em estoque.
* **Propriedade Calculada (`subtotal` em ItemPedido):** Calculado como `quantidade * preco_unitario`.
* **Propriedade Calculada (`total` em Pedido):** Soma automatizada dos subtotais de todos os itens vinculados ao pedido.

**Atributos e Propriedades — Produto:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `nome` | `str` |  |
| `preco` | `float` |  (Valida valor $> 0$) |
| `estoque` | `int` |  (Valida valor $\ge 0$) |

**Atributos e Propriedades — ItemPedido:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `pedido_id` | `int` | Somente Leitura |
| `produto_id` | `int` | Somente Leitura |
| `quantidade` | `int` |  (Valida se $\le$ estoque) |
| `subtotal` | `float` | **Propriedade Calculada:** `quantidade * preco_produto` |

**Atributos e Propriedades — Pedido:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `cliente` | `str` |  |
| `status` | `str` |  (Valida transição: pendente -> pago -> enviado) |
| `total` | `float` | **Propriedade Calculada:** Soma de todos os `subtotal` dos itens |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `POST` | `/pedidos` | Abre novo pedido |
| `POST` | `/pedidos/{id}/itens` | Adiciona item ao pedido |
| `GET` | `/pedidos/{id}` | Detalhe do pedido com itens e total |
| `PUT` | `/pedidos/{id}/pagar` | Confirma pagamento |
| `GET` | `/pedidos?status=pendente` | Pedidos filtrados por status |

---

### Exercício 18 — Clínica veterinária

Cadastro de tutores, pets e consultas médicas veterinárias.

#### Validações necessárias:
* **Data de Nascimento (Pet):** Não pode ser no futuro.
* **Propriedade Calculada (`idade_anos` em Pet):** Calcula a idade exata com base na data de nascimento e no dia atual.
* **Consulta:** Exige vínculo válido com pet cadastrado.

**Atributos e Propriedades — Dono:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `nome` | `str` |  |
| `telefone` | `str` |  (Validação numérica) |

**Atributos e Propriedades — Pet:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `dono_id` | `int` | Somente Leitura |
| `nome` | `str` |  |
| `especie` | `str` |  |
| `nascimento` | `date` |  (Valida data $\le$ hoje) |
| `idade_anos` | `int` | **Propriedade Calculada:** Idade baseada no nascimento |

**Atributos e Propriedades — Consulta:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `pet_id` | `int` | Somente Leitura |
| `veterinario` | `str` |  |
| `data` | `date` |  |
| `diagnostico` | `str` |  |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `POST` | `/donos` | Cadastra dono |
| `POST` | `/donos/{id}/pets` | Cadastra pet vinculado ao dono |
| `GET` | `/donos/{id}/pets` | Lista pets de um dono |
| `POST` | `/consultas` | Agenda e registra consulta |
| `GET` | `/pets/{id}/historico` | Histórico de consultas do pet |

---

### Exercício 19 — Estacionamento com vagas

Gestão de ocupação e tarifação de veículos.

#### Validações necessárias:
* **Ticket -> Horário de Saída:** Deve ser maior que o horário de entrada.
* **Propriedade Calculada (`duracao_horas`):** Calcula a quantidade total de horas (arredondado para cima para frações).
* **Propriedade Calculada (`valor_total`):** Calcula a taxa cobrada multiplicando a `duracao_horas` pela tarifa vigente (R$ 5,00/hora).

**Atributos e Propriedades — Vaga:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `numero` | `int` |  |
| `tipo` | `str` |  |
| `ocupada` | `bool` |  (Atualizado com base nos tickets ativos) |

**Atributos e Propriedades — Ticket:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `vaga_id` | `int` | Somente Leitura |
| `placa` | `str` |  (Valida formato de placa) |
| `entrada` | `datetime` | Somente Leitura |
| `saida` | `datetime` ou `None` |  (Valida se $> entrada$) |
| `duracao_horas` | `int` | **Propriedade Calculada:** Horas cobradas (teto de frações) |
| `valor_total` | `float` | **Propriedade Calculada:** `duracao_horas * 5.0` |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/vagas/disponiveis` | Vagas livres no momento |
| `POST` | `/tickets` | Registra entrada do veículo |
| `PUT` | `/tickets/{id}/saida` | Registra saída e calcula valor |
| `GET` | `/vagas/{id}/status` | Situação atual da vaga |

---

### Exercício 20 — Controle de medicamentos hospitalares

Controle estrito de estoque hospitalar e alertas de reposição.

#### Validações necessárias:
* **Estoque Atual:** Impedir diretamente valores negativos. Qualquer dispensação que exceda o estoque atual deve ser bloqueada.
* **Propriedade Calculada (`abaixo_do_minimo`):** Retorna `True` se `estoque_atual < estoque_minimo`.
* **Dispensação -> Quantidade:** Deve ser maior que zero e menor ou igual ao estoque do medicamento associado.

**Atributos e Propriedades — Medicamento:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `nome` | `str` |  |
| `estoque_atual` | `int` |  (Garante valor $\ge 0$) |
| `estoque_minimo` | `int` |  (Garante valor $> 0$) |
| `abaixo_do_minimo` | `bool` | **Propriedade Calculada:** `estoque_atual < estoque_minimo` |

**Atributos e Propriedades — Dispensacao:**

| Atributo / Propriedade | Tipo |Regras de validação|
|---|---|---|
| `id` | `int` | Somente Leitura |
| `medicamento_id` | `int` | Somente Leitura |
| `paciente` | `str` |  |
| `quantidade` | `int` |  (Valida se $> 0$ e $\le$ estoque) |
| `data` | `datetime` | Somente Leitura |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/medicamentos` | Lista medicamentos |
| `GET` | `/medicamentos/estoque-critico` | Abaixo do estoque mínimo |
| `POST` | `/dispensacoes` | Registra dispensação e desconta estoque |
| `GET` | `/medicamentos/{id}/dispensacoes` | Histórico de dispensações |

---