# Exercícios de Modelagem de Objetos e APIs com FastAPI

> **Objetivo:** Modelar classes Python e implementar rotas FastAPI para cada situação descrita.  
> **Para cada exercício:** identifique o(s) objeto(s), defina seus atributos com tipos Python e implemente as rotas indicadas.

---

## Nível 1 — Básico

> Um único objeto com atributos simples. Criar classes, definir atributos e como URLs representam recursos.

---

### Exercício 01 — Ficha de aluno

Você foi contratado para criar o sistema de cadastro de alunos de uma escola. Cada aluno tem nome, número de matrícula, curso e e-mail. O sistema precisa permitir consultar, cadastrar e atualizar essas informações.

**Objeto a modelar:** `Aluno`

**Atributos:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `nome` | `str` |
| `matricula` | `str` |
| `curso` | `str` |
| `email` | `str` |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/alunos` | Lista todos os alunos |
| `GET` | `/alunos/{id}` | Retorna um aluno específico |
| `POST` | `/alunos` | Cadastra um novo aluno |
| `PUT` | `/alunos/{id}` | Atualiza os dados do aluno |

---

### Exercício 02 — Cardápio de lanchonete

Uma lanchonete quer exibir o cardápio na internet. Cada item tem nome, descrição, preço e uma indicação se está disponível hoje ou não. O atendente precisa conseguir marcar itens como indisponíveis quando acabarem.

**Objeto a modelar:** `ItemCardapio`

**Atributos:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `nome` | `str` |
| `descricao` | `str` |
| `preco` | `float` |
| `disponivel` | `bool` |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/cardapio` | Lista todos os itens |
| `GET` | `/cardapio?disponivel=true` | Filtra apenas os disponíveis |
| `POST` | `/cardapio` | Adiciona novo item |
| `PUT` | `/cardapio/{id}/disponibilidade` | Marca como disponível ou não |

---

### Exercício 03 — Agenda de contatos

Você precisa criar uma agenda digital simples. Nela é possível guardar o nome, telefone e e-mail de cada contato. O usuário quer poder buscar contatos pelo nome sem precisar digitar o nome completo.

**Objeto a modelar:** `Contato`

**Atributos:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `nome` | `str` |
| `telefone` | `str` |
| `email` | `str` |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/contatos` | Lista todos os contatos |
| `GET` | `/contatos?nome=Maria` | Busca por nome parcial |
| `POST` | `/contatos` | Adiciona um contato |
| `DELETE` | `/contatos/{id}` | Remove um contato |

---

### Exercício 04 — Catálogo de filmes

Um cineclube quer organizar os filmes que já assistiram coletivamente. Cada filme tem título, diretor, ano de lançamento e gênero. Os membros querem poder filtrar os filmes por gênero para encontrar os de drama, comédia, etc.

**Objeto a modelar:** `Filme`

**Atributos:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `titulo` | `str` |
| `diretor` | `str` |
| `ano` | `int` |
| `genero` | `str` |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/filmes` | Lista todos os filmes |
| `GET` | `/filmes?genero=drama` | Filtra por gênero |
| `GET` | `/filmes/{id}` | Detalhes de um filme |
| `POST` | `/filmes` | Cadastra novo filme |

---

### Exercício 05 — Lista de tarefas

Um aplicativo de produtividade precisa de um backend para gerenciar tarefas. Cada tarefa tem um título, uma descrição e pode estar pendente ou concluída. O usuário quer ver separado o que já fez do que ainda falta.

**Objeto a modelar:** `Tarefa`

**Atributos:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `titulo` | `str` |
| `descricao` | `str` |
| `concluida` | `bool` |
| `criada_em` | `datetime` |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/tarefas` | Lista todas as tarefas |
| `GET` | `/tarefas?concluida=false` | Lista apenas as pendentes |
| `POST` | `/tarefas` | Cria nova tarefa |
| `PUT` | `/tarefas/{id}/concluir` | Marca como concluída |

---

### Exercício 06 — Registro de notas

Um professor precisa de um sistema para lançar as notas dos alunos por disciplina. Cada nota tem o valor (de 0 a 10), o nome da disciplina e a data em que foi lançada. O professor também quer poder consultar apenas as notas de um aluno específico.

**Objeto a modelar:** `Nota`

**Atributos:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `aluno_id` | `int` |
| `disciplina` | `str` |
| `valor` | `float` |
| `data_lancamento` | `date` |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/notas` | Lista todas as notas |
| `GET` | `/notas?aluno_id=5` | Notas de um aluno específico |
| `POST` | `/notas` | Lança nova nota |
| `PUT` | `/notas/{id}` | Corrige uma nota lançada |

---

### Exercício 07 — Acervo de livros

Uma pequena biblioteca comunitária quer catalogar seus livros para que os frequentadores saibam o que está disponível. Cada livro tem título, autor, ISBN e o número de exemplares em estoque. É possível buscar livros por autor.

**Objeto a modelar:** `Livro`

**Atributos:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `titulo` | `str` |
| `autor` | `str` |
| `isbn` | `str` |
| `exemplares` | `int` |

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

Um viveiro de plantas quer publicar seu catálogo online. Cada planta tem nome popular, nome científico, tipo (árvore, arbusto, suculenta…), preço e se está em estoque. O cliente quer filtrar por tipo e por disponibilidade.

**Objeto a modelar:** `Planta`

**Atributos:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `nome_popular` | `str` |
| `nome_cientifico` | `str` |
| `tipo` | `str` |
| `preco` | `float` |
| `em_estoque` | `bool` |

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

Um abrigo de animais precisa de um sistema para registrar os animais resgatados. Cada animal tem nome, espécie, raça, idade aproximada e se já foi adotado. O funcionário quer listar apenas os disponíveis para adoção.

**Objeto a modelar:** `Animal`

**Atributos:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `nome` | `str` |
| `especie` | `str` |
| `raca` | `str` |
| `idade` | `int` |
| `adotado` | `bool` |

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

Uma plataforma de cursos online precisa de um backend para listar seus cursos. Cada curso tem título, instrutor, carga horária, nível (iniciante, intermediário, avançado) e preço. O aluno quer filtrar por nível.

**Objeto a modelar:** `Curso`

**Atributos:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `titulo` | `str` |
| `instrutor` | `str` |
| `carga_horaria` | `int` |
| `nivel` | `str` |
| `preco` | `float` |

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

O setor de TI de uma empresa precisa controlar seus equipamentos: notebooks, monitores, teclados etc. Cada item tem número de patrimônio, descrição, localização e situação (ativo, em manutenção, descartado). Eles querem filtrar por situação.

**Objeto a modelar:** `Equipamento`

**Atributos:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `patrimonio` | `str` |
| `descricao` | `str` |
| `localizacao` | `str` |
| `situacao` | `str` |

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

Uma pessoa quer registrar os livros que está lendo ou já leu. Para cada leitura ela anota o título do livro, o autor, a data em que começou, a data em que terminou (pode estar em branco se ainda estiver lendo) e uma avaliação de 1 a 5 estrelas.

**Objeto a modelar:** `Leitura`

**Atributos:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `titulo` | `str` |
| `autor` | `str` |
| `data_inicio` | `date` |
| `data_fim` | `date` ou `None` |
| `avaliacao` | `int` ou `None` |

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

Uma nutricionista quer publicar opções de refeições para seus pacientes. Cada refeição tem nome, tipo (café da manhã, almoço, jantar, lanche), quantidade de calorias e uma lista dos ingredientes principais. Os pacientes filtram por tipo de refeição e por limite de calorias.

**Objeto a modelar:** `Refeicao`

**Atributos:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `nome` | `str` |
| `tipo` | `str` |
| `calorias` | `int` |
| `ingredientes` | `list[str]` |

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

> Dois ou mais objetos relacionados entre si. O sistema precisa verificar regras que envolvem mais de um objeto ao mesmo tempo.

---

### Exercício 14 — Sistema de reserva de mesas

Um restaurante precisa controlar suas mesas e reservas. Cada mesa tem um número e uma capacidade máxima de pessoas. Uma reserva vincula uma mesa a um cliente em uma data e horário específicos, com o número de pessoas do grupo. Antes de aceitar uma reserva, o sistema deve checar se a mesa existe e se a quantidade de pessoas não excede a capacidade.

**Objetos a modelar:** `Mesa` e `Reserva`

**Atributos — Mesa:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `numero` | `int` |
| `capacidade` | `int` |

**Atributos — Reserva:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `mesa_id` | `int` |
| `cliente_nome` | `str` |
| `data` | `date` |
| `horario` | `str` |
| `pessoas` | `int` |

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

Uma biblioteca registra livros e permite que leitores os emprestem. Um livro tem título, autor e um indicador de disponibilidade. Um empréstimo registra qual livro saiu, para qual leitor, quando foi retirado e qual a data prevista de devolução. O sistema só deve aceitar o empréstimo se o livro estiver disponível.

**Objetos a modelar:** `Livro` e `Emprestimo`

**Atributos — Livro:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `titulo` | `str` |
| `autor` | `str` |
| `disponivel` | `bool` |

**Atributos — Emprestimo:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `livro_id` | `int` |
| `leitor_nome` | `str` |
| `data_emprestimo` | `date` |
| `data_prevista` | `date` |

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

Uma empresa precisa registrar a entrada e saída de cada funcionário. O funcionário tem nome, cargo e departamento. Cada registro de ponto guarda o horário de entrada e de saída. O sistema calcula automaticamente as horas trabalhadas ao registrar a saída. O gestor pode consultar o ponto de um funcionário em uma data específica.

**Objetos a modelar:** `Funcionario` e `RegistroPonto`

**Atributos — Funcionario:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `nome` | `str` |
| `cargo` | `str` |
| `departamento` | `str` |

**Atributos — RegistroPonto:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `funcionario_id` | `int` |
| `entrada` | `datetime` |
| `saida` | `datetime` ou `None` |
| `horas_trabalhadas` | `float` ou `None` |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/funcionarios` | Lista funcionários |
| `POST` | `/funcionarios/{id}/entrada` | Registra horário de entrada |
| `PUT` | `/funcionarios/{id}/saida` | Registra saída e calcula horas |
| `GET` | `/funcionarios/{id}/ponto?data=2024-08-10` | Ponto de um dia específico |

---

### Exercício 17 — Pedidos de uma loja virtual

Uma loja virtual precisa registrar pedidos. Um pedido pertence a um cliente e pode conter vários itens, cada um com um produto e uma quantidade. O total do pedido deve ser calculado automaticamente. Pedidos passam por estados: pendente, pago e enviado.

**Objetos a modelar:** `Produto`, `Pedido` e `ItemPedido`

**Atributos — Produto:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `nome` | `str` |
| `preco` | `float` |
| `estoque` | `int` |

**Atributos — Pedido:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `cliente` | `str` |
| `status` | `str` |
| `total` | `float` |

**Atributos — ItemPedido:**

| Atributo | Tipo |
|---|---|
| `pedido_id` | `int` |
| `produto_id` | `int` |
| `quantidade` | `int` |
| `subtotal` | `float` |

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

Uma clínica veterinária atende pets e seus donos. Um dono pode ter vários pets. Cada pet tem nome, espécie e data de nascimento. As consultas registram qual pet foi atendido, qual veterinário atendeu, a data e o diagnóstico. O sistema deve permitir consultar o histórico de consultas de um pet.

**Objetos a modelar:** `Dono`, `Pet` e `Consulta`

**Atributos — Dono:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `nome` | `str` |
| `telefone` | `str` |

**Atributos — Pet:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `dono_id` | `int` |
| `nome` | `str` |
| `especie` | `str` |
| `nascimento` | `date` |

**Atributos — Consulta:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `pet_id` | `int` |
| `veterinario` | `str` |
| `data` | `date` |
| `diagnostico` | `str` |

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

Um estacionamento tem vagas numeradas. Quando um veículo entra, um ticket é gerado com a placa e o horário de entrada. Quando o veículo sai, o ticket é encerrado e o sistema calcula o valor a pagar (R$ 5,00 por hora, frações cobradas como hora cheia). O gestor quer ver quais vagas estão ocupadas no momento.

**Objetos a modelar:** `Vaga` e `Ticket`

**Atributos — Vaga:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `numero` | `int` |
| `tipo` | `str` |
| `ocupada` | `bool` |

**Atributos — Ticket:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `vaga_id` | `int` |
| `placa` | `str` |
| `entrada` | `datetime` |
| `saida` | `datetime` ou `None` |
| `valor` | `float` ou `None` |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/vagas/disponiveis` | Vagas livres no momento |
| `POST` | `/tickets` | Registra entrada do veículo |
| `PUT` | `/tickets/{id}/saida` | Registra saída e calcula valor |
| `GET` | `/vagas/{id}/status` | Situação atual da vaga |

---

### Exercício 20 — Controle de medicamentos hospitalares

Um hospital precisa controlar o estoque de medicamentos. Cada medicamento tem nome, quantidade em estoque e um estoque mínimo de segurança. Quando um medicamento é dispensado para um paciente, a quantidade em estoque diminui. O sistema deve impedir a dispensação se não houver estoque suficiente e alertar quando um medicamento estiver abaixo do mínimo.

**Objetos a modelar:** `Medicamento` e `Dispensacao`

**Atributos — Medicamento:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `nome` | `str` |
| `estoque_atual` | `int` |
| `estoque_minimo` | `int` |

**Atributos — Dispensacao:**

| Atributo | Tipo |
|---|---|
| `id` | `int` |
| `medicamento_id` | `int` |
| `paciente` | `str` |
| `quantidade` | `int` |
| `data` | `datetime` |

**Rotas a implementar:**

| Método | URL | O que faz |
|---|---|---|
| `GET` | `/medicamentos` | Lista medicamentos |
| `GET` | `/medicamentos/estoque-critico` | Abaixo do estoque mínimo |
| `POST` | `/dispensacoes` | Registra dispensação e desconta estoque |
| `GET` | `/medicamentos/{id}/dispensacoes` | Histórico de dispensações |

---

*20 exercícios · 13 de nível 1 · 7 de nível 2 · Python 3.12+ · FastAPI · Pydantic v2*