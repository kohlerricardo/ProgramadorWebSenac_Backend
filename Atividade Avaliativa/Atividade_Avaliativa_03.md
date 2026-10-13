# Atividade Avaliativa 03
___
**SENAC Videira**
**Professor:** Ricardo Köhler

**E-mail:** ricardo.kohler@prof.sc.senac.br

### **Data de entrega: 19/10/2026**
### **Horário Limite: 23:59:59**
#### **Formato de entrega**: Link de repositório no GitHub.
___


> Considere o cenário da "Operação Cadê o Equipamento?" e as atividades avaliativas 01 e 02. Sabendo que somente é possível autorizar um empréstimo de equipamento sendo gestor, e somente é possível cadastrar um equipamento sendo administrador, o objetivo da avaliação é protejer as rotas conforme as regras do sistema.
---


## **Avaliação Prática 3: Operação "Cadê o Equipamento?" — Proteção Total**
Vocês já entenderam o problema do almoxarifado, definiram as regras do jogo em salvam os dados no banco de dados. O alicerce está pronto. Finalmente é hora de aparar as arestas e tornar o sistema plenamente funcional.

Nesta terceira avaliação, a missão da sua euquipe é proteger o que deve ser protegido. Cadastros de equipamentos, autorizações e devoluções de empréstimos, solicitações... Cada qual com o usuário e o papel atribuído a ele.


#### 1. **O Que Deve Ser Entregue (Requisitos Técnicos)**
Deve ser realizado o login do usuário, e este usuário deve conseguir executar as operações a ele atribuídas, conforme permissões:
- Usuário comum: Solicitar empréstimos
- Usuário Gestor: Aprovar empréstimos e registrar devoluções
- Usuário Administrador: Cadastrar equipamentos
  
Devem estar modeladas as entidades usuários, equipamentos e empréstimos.


#### **2. Critérios de Avaliação**
**Operacionalidade**: Usuários comuns não podem ter acesso as rotas de aprovação e cadastro. 
Usuário gestor não pode ter permissão para cadastro de itens.


**Tratamento de Exceções**: Falhas de permissão devem gerar excessões, e estas excessões devem ser tratadas e traduzidos para códigos HTTP semânticos.

---

> Lembrem-se de consultar o repositório da disciplina. Nele estão disponíveis modelos para a implementação da autenticação e autorização.