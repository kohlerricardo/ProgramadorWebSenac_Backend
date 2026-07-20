# Lista de Exercícios: Lógica para APIs e Transferência Web (JSON)

Familiarização com o fluxo da web, substituindo a interação de terminal (entrada do usuário e impressão na tela) pelo modelo de Parâmetros e Resposta (Request/Response).

## Parte 1: Operações Básicas e Fórmulas

*Os dados de entrada (input) devem ser enviados via Query Params ou Path Params e os resultados (print) são devolvidos pela API na resposta.*

1. **Calculadora de Soma:** Crie um endpoint `GET /api/calculadora/soma`.
    * **Parâmetros:** `{"numero1": 5, "numero2": 10}`
    * **Resposta:** `{"resultado": 15}`

2. **Área do Retângulo:** Crie um endpoint `GET /api/geometria/retangulo`.
    * **Parâmetros:** `{"base": 10, "altura": 5}`
    * **Resposta:** `{"area": 50}`

3. **Conversor de Temperatura:** Crie um endpoint `GET /api/conversores/temperatura`.
    * **Parâmetros:** `{"celsius": 30}`
    * **Resposta:** `{"fahrenheit": 86.0}`

4. **Cálculo de Média:** Crie um endpoint `GET /api/escola/media-simples`.
    * **Parâmetros:** `{"nota1": 7, "nota2": 8, "nota3": 6}`
    * **Resposta:** `{"media_aritmetica": 7.0}`

5. **Juros Simples:** Crie um endpoint `GET /api/financas/juros-simples`.
    * **Parâmetros:** `{"capital": 1000, "taxa_mensal": 0.05, "meses": 12}`
    * **Resposta:** `{"valor_juros": 600}`

6. **Calculadora de IMC:** Crie um endpoint `GET /api/saude/imc`.
    * **Parâmetros:** `{"peso_kg": 70, "altura_m": 1.75}`
    * **Resposta:** `{"imc": 22.86}`

7. **Conversor de Minutos:** Crie um endpoint `GET /api/conversores/tempo-horas`.
    * **Parâmetros:** `{"minutos_totais": 130}`
    * **Resposta:** `{"horas": 2, "minutos_restantes": 10}`

8. **Cálculo de Desconto:** Crie um endpoint `GET /api/loja/aplicar-desconto`.
    * **Parâmetros:** `{"valor_produto": 100, "porcentagem_desconto": 15}`
    * **Resposta:** `{"valor_com_desconto": 85.0}`

9. **Perímetro do Círculo:** Crie um endpoint `GET /api/geometria/circulo/perimetro`.
    * **Parâmetros:** `{"raio": 5}`
    * **Resposta:** `{"perimetro": 31.41}`

10. **Consumo de Veículo:** Crie um endpoint `GET /api/veiculos/consumo-medio`.
    * **Parâmetros:** `{"distancia_km": 500, "litros_combustivel": 50}`
    * **Resposta:** `{"km_por_litro": 10.0}`

11. **Conversor de Moeda:** Crie um endpoint `GET /api/financas/cambio`.
    * **Parâmetros:** `{"valor_real": 100, "cotacao_dolar": 5.20}`
    * **Resposta:** `{"valor_convertido_dolar": 19.23}`

12. **Idade em Dias:** Crie um endpoint `GET /api/pessoa/idade-dias`.
    * **Parâmetros:** `{"idade_anos": 20}`
    * **Resposta:** `{"dias_vividos_estimados": 7300}`

13. **Área do Triângulo:** Crie um endpoint `GET /api/geometria/triangulo/area`.
    * **Parâmetros:** `{"base": 10, "altura": 5}`
    * **Resposta:** `{"area": 25.0}`

14. **Calculadora de Gorjeta:** Crie um endpoint `GET /api/restaurante/conta`.
    * **Parâmetros:** `{"valor_consumo": 100.0, "porcentagem_gorjeta": 10}`
    * **Resposta:** `{"valor_gorjeta": 10.0, "total_a_pagar": 110.0}`

15. **Conversor de Segundos:** Crie um endpoint `GET /api/conversores/tempo-completo`.
    * **Parâmetros:** `{"segundos_totais": 3665}`
    * **Resposta:** `{"horas": 1, "minutos": 1, "segundos": 5}`

---

## Parte 2: Arrays e Laços de Repetição (Listas JSON)

*Trabalhando com envio e recebimento de conjuntos de dados (listas no formato JSON).*

16. **Soma de Array:** Crie um endpoint `GET /api/listas/somar`.
    * **Parâmetros:** `{"valores": [1, 2, 3, 4, 5]}`
    * **Resposta:** `{"soma_total": 15}`

17. **Média de Múltiplas Notas:** Crie um endpoint `GET /api/escola/media-turma`.
    * **Parâmetros:** `{"notas": [7.5, 8.0, 6.5, 9.0]}`
    * **Resposta:** `{"media_final": 7.75}`

18. **Gerador de Tabuada:** Crie um endpoint `GET /api/matematica/tabuada/`.
    * **Parâmetros:** `{numero e limite}`
    * **Resposta:** `{"tabuada": [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]}`

19. **Buscador do Maior Número:** Crie um endpoint `GET /api/listas/maior-valor`.
    * **Parâmetros:** `{"numeros": [45, 12, 99, 3, 88]}`
    * **Resposta:** `{"maior_numero_encontrado": 99}`

20. **Lista de Cumprimentos:** Crie um endpoint `GET /api/social/saudacoes`.
    * **Parâmetros:** `{"nomes": ["Ana", "Bruno", "Carlos"]}`
    * **Resposta:** `{"mensagens": ["Olá, Ana!", "Olá, Bruno!", "Olá, Carlos!"]}`

21. **Ordem Inversa da Lista:** Crie um endpoint `GET /api/listas/inverter`.
    * **Parâmetros:** `{"dados": [10, 20, 30, 40]}`
    * **Resposta:** `{"dados_invertidos": [40, 30, 20, 10]}`

22. **Combinação de Nomes:** Crie um endpoint `GET /api/pessoas/formatar-nomes`.
    * **Parâmetros:** `{"nomes": ["Ana", "Bruno"], "sobrenomes": ["Silva", "Gomes"]}`
    * **Resposta:** `{"nomes_completos": ["Ana Silva", "Bruno Gomes"]}`

23. **Inversão de String:** Crie um endpoint `GET /api/texto/inverter`.
    * **Parâmetros:** `{"palavra": "developer"}`
    * **Resposta:** `{"palavra_invertida": "repoleved"}`

24. **Cálculo de Matriz 3x3:** Crie um endpoint `GET /api/matematica/matriz/diagonal`.
    * **Parâmetros:** `{"matriz": [[1,2,3], [4,5,6], [7,8,9]]}`
    * **Resposta:** `{"soma_diagonal_principal": 15}`

25. **Contador de Palavras:** Crie um endpoint `GET /api/texto/frequencia`.
    * **Parâmetros:** `{"palavras": ["sol", "chuva", "sol", "nuvem"]}`
    * **Resposta:** `{"frequencia": {"sol": 2, "chuva": 1, "nuvem": 1}}`

26. **Contagem de Pares e Ímpares:** Crie um endpoint `GET /api/matematica/paridade`.
    * **Parâmetros:** `{"numeros": [1, 2, 3, 4, 5, 6]}`
    * **Resposta:** `{"total_pares": 3, "total_impares": 3}`

27. **Mecanismo de Busca Simples:** Crie um endpoint `GET /api/listas/buscar-item`.
    * **Parâmetros:** `{"estoque": ["Maçã", "Banana", "Morango"], "termo_busca": "Morango"}`
    * **Resposta:** `{"encontrado": true, "mensagem": "Morango encontrado!"}`
