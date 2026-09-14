# Atividade Avaliativa 02
___
**SENAC Videira**
**Professor:** Ricardo Köhler
**E-mail:** ricardo.kohler@prof.sc.senac.br
### **Data de entrega: 28/09/2026**
### **Horário Limite: 23:59:59**
___


> Considere o cenário da "Operação Cadê o Equipamento?" e a modelagem realizada para a atividade avaliatica 01. Sabendo que o objetivo da avaliação é manipular os dados oriundos de um frontend, sua tarefa é proporcionar a integração com a base de dados modelada e realizar corretamente as operações **Create**, **Retrieve**, **Update** e **Delete** para cada entidade modelada.
---


## **Avaliação Prática 2: Operação "Cadê o Equipamento?" — O Desafio do CRUD**
Vocês já entenderam o problema do almoxarifado, definiram as regras do jogo e modelaram as tabelas do banco de dados. O alicerce está pronto. Agora, a direção da instituição exige que o sistema comece a funcionar de verdade. De nada adianta um banco de dados perfeitamente desenhado se os gestores e alunos não conseguem interagir com ele.

Nesta segunda avaliação, a missão da sua euquipe é construir o motor de dados do sistema: implementar todas as operações CRUD (Create, Read, Update, Delete) para as entidades modeladas .

O sistema precisa ser blindado contra erros bobos e organizado para não virar um caos de manutenção no futuro.

#### 1. **O Que Deve Ser Entregue (Requisitos Técnicos)**
Para cada entidade fundamental do domínio que vocês modelaram (ex: Equipamento, CategoriaEquipamento, Usuario, etc.), o backend deve apresentar obrigatoriamente:

**As Quatro Operações Básicas**: Endpoints funcionais cobrindo os verbos HTTP corretos (POST para cadastrar, GET para listar todos e buscar por ID, PUT para atualizar e DELETE para remover).

**Modelagem de Dados (Schemas/Modelos)**: Modelos de entrada e saída de dados. O sistema não pode aceitar um equipamento sem número de patrimônio e não deve vazar informações internas sensíveis nas respostas.

**Divisão de Tarefas (Arquitetura)**: O arquivo de rotas (routers) deve apenas receber a requisição e devolver a resposta. A inteligência, a comunicação com o banco de dados e as validações pesadas devem ocorrer dentro dos controllers.

**Persistência Real**: Os dados não podem sumir se o servidor reiniciar. Toda operação deve manipular as informações diretamente no banco de dados configurado.

#### **2. Regras de Negócio Obrigatórias**
Um CRUD de nível profissional não permite que o usuário faça o que quiser e quebre o banco. O código de vocês deve garantir que:

**Integridade de Dados Protegida:** Se um usuário tentar deletar uma Categoria que já possui Equipamentos cadastrados nela, a API não pode "estourar" com um erro feio do banco de dados (Status 500). O Controller deve capturar essa falha e devolver um aviso claro (ex: Status 400 ou 409) informando que a ação foi bloqueada.

**Buscas Precisas:** Se o frontend solicitar os detalhes do equipamento ID 999 e ele não existir, o sistema deve retornar um erro HTTP 404 (Not Found) formatado de forma elegante.

**Atualização Limpa:** O verbo PUT deve atualizar os registros corretamente, garantindo que regras básicas (como checar se a nova categoria informada realmente existe) sejam aplicadas antes de salvar a alteração.

#### **3. Critérios de Avaliação**
**Operacionalidade**: O fluxo completo funciona ponta a ponta? (Cadastrar, visualizar, alterar e deletar funcionam via Swagger/HTTPForge ou outra ferramenta de requisições sem erros).

**Arquitetura e Organização**: As camadas estão respeitadas? (Schemas validando, Routers respondendo HTTP e Controllers resolvendo a lógica de banco).

**Tratamento de Exceções**: Os erros e falhas de negócio estão sendo capturados com blocos try/except e traduzidos para códigos HTTP semânticos (400, 404, 409)?

**Código Limpo**: Variáveis com nomes claros, TypeHint quando necessário e ausência de "código zumbi" (linhas comentadas que não fazem nada).

---

> Lembrem-se de consultar o repositório da disciplina. Nele estão disponíveis modelos para a implementação das operações CRUD e da separação de camadas.