# Estudo de Caso: Operação "Cadê o Equipamento?"

## O Cenário
Imagine a seguinte situação: você faz parte de uma instituição de ensino super movimentada. O almoxarifado de tecnologia é o coração do lugar. É de lá que saem os projetores para as aulas teóricas, as câmeras para os projetos de audiovisual e os notebooks que a galera de infraestrutura vive pegando emprestado para testar ferramentas Linux, rodar scripts em Bash e configurar servidores de laboratório. 

Tudo parece ótimo na teoria, mas na prática... é um caos. 

## O Problema
Atualmente, o controle de quem pegou o quê é feito em uma planilha do Excel (que vive travando) e em um caderno de arame que já teve café derramado umas três vezes. 

O resultado? 
* Ninguém sabe com quem está a câmera principal.
* Um aluno novato acidentalmente apagou as linhas da planilha, e agora o sistema "esqueceu" que três notebooks não foram devolvidos.
* O coordenador comprou cinco projetores novos, mas qualquer pessoa consegue ir na planilha e cadastrar, alterar ou excluir equipamentos sem permissão nenhuma. 

A instituição percebeu que não dá mais para viver de planilhas. Eles precisam de um sistema de verdade, seguro e inteligente. É aqui que você e sua equipe entram.

## Os Personagens do Nosso Sistema
Para acabar com a bagunça, a direção definiu que o novo sistema terá regras de acesso estritas (o que chamamos de RBAC - *Role-Based Access Control*, ou Controle de Acesso Baseado em Papéis). O sistema terá três perfis principais:

1. **O Discente (Aluno/Usuário Comum):** 
   * **O que ele quer:** Precisa de um equipamento para um projeto. 
   * **O que ele pode fazer:** Pode fazer login, ver o que está disponível no catálogo e solicitar um empréstimo. Só isso. Ele não pode aprovar o próprio pedido.

2. **O Gestor (A pessoa do Almoxarifado):**
   * **O que ele quer:** Manter a ordem e saber exatamente onde está cada item.
   * **O que ele pode fazer:** Quando um aluno solicita um equipamento, o Gestor avalia e **autoriza** (ou nega) o empréstimo. Quando o aluno devolve o item, é o Gestor quem registra a **devolução** no sistema, liberando o equipamento para a próxima pessoa.

3. **O Administrador (A Coordenação de TI):**
   * **O que ele quer:** Gerenciar o patrimônio da escola.
   * **O que ele pode fazer:** Além de ter os mesmos poderes do Gestor, o Administrador é a **única** pessoa que pode cadastrar um equipamento novo que acabou de ser comprado ou remover do sistema um equipamento que quebrou de vez.

## O Seu Desafio
Sua missão é construir o "cérebro" (a API / o Backend) desse sistema. 

Você não precisa se preocupar com a tela bonita do aplicativo agora, mas precisa garantir que a lógica por trás funcione perfeitamente. O seu sistema deve ser capaz de:
* Exigir que todo mundo faça login antes de tentar pegar qualquer coisa.
* Identificar "quem é quem" (se o Joãozinho tentar cadastrar um projetor novo, o sistema deve barrá-lo, pois ele é apenas um aluno).
* Registrar toda a jornada de um equipamento: de "Disponível" para "Emprestado" (com a bênção de um gestor) e, finalmente, de volta para "Disponível" após a devolução.

E aí, como você organizaria os dados e as rotas para garantir que nenhum notebook desapareça novamente? Por onde começamos a construir essa solução?