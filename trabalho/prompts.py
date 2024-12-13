CODER1 = """
Você vai receber um dataframe pandas e deve tratar a coluna "Name". Você deve se atentar a diversos pontos, como:

- Limpeza Básica de Caracteres Especiais:
Ex.: ["João   Silva", "Maria#Oliveira!", "Carlos--Santos"] -> ["João Silva", "Maria Oliveira", "Carlos Santos"]

- Formatação com Capitalização Correta
Ex.: ["joão silva", "MARIA oliveira", "cArLoS SaNtOs"] -> ["João Silva", "Maria Oliveira", "Carlos Santos"]

- Correção de Erros Ortográficos
Ex.: ["Joåo Sllva", "Mar1a Olive1ra", "Karlos Santos"] -> ["João Silva", "Maria Oliveira", "Carlos Santos"]

Não invente regras, apenas siga as instruções acima. Seja o mais claro e objetivo possível.
"""

CODER2 = """
Você vai receber um dataframe pandas e deve tratar a coluna "Name". Você deve se atentar a diversos pontos, como:

- Limpeza Básica de Caracteres Especiais:
Ex.: ["João   Silva", "Maria#Oliveira!", "Carlos--Santos"] -> ["João Silva", "Maria Oliveira", "Carlos Santos"]

- Formatação com Capitalização Correta
Ex.: ["joão silva", "MARIA oliveira", "cArLoS SaNtOs"] -> ["João Silva", "Maria Oliveira", "Carlos Santos"]

- Correção de Erros Ortográficos
Ex.: ["Joåo Sllva", "Mar1a Olive1ra", "Karlos Santos"] -> ["João Silva", "Maria Oliveira", "Carlos Santos"]

Não invente regras, apenas siga as instruções acima. Seja o mais claro e objetivo possível.
"""

REVIEWER = """
Você vai receber um dataframe pandas (que deveria passar por uma limpeza de dados na coluna "Name"), um código gerado
por um LLM codificador para executar essa tarefa e um score. Esse score é qualidade do código feito pelo codificador.
Esse score é uma nota de 0 a 10, quanto maior, melhor a qualidade do código, sendo 10 a nota máxima. Quanto maior for
a nota, menos sugesso você deve dar ao codificador. Caso a nota seja pequena, maior a quantidade de sugestões você deve
dar ao agente.

Seu trabalho é analisar o código e o resultado do codificador e gerar um novo prompt para que o codificador possa
melhorar sua performance. Seja o mais claro e objetivo possível.
"""

REPORT = """
Você vai receber os prompts de dois LLMs codificadores que tinham como trabalho fazer a limpeza da coluna "Name" de um
dataframe pandas. Também vai receber a pontuação do código, que visava limpar os nomes.
Por fim, vai receber o código que cada um dos codificadores gerou para fazer realizar a limpeza dos dados.

Sua tarefa é avaliar os prompts e a pontuação dos códigos e produzir um relatório avaliando o trabalho dos codificadores.
Seja bem descritivo e objetivo.

Abaixo estão as seções que devem ser abordadas no relatório:

Descrição do Problema:
    Clareza: A descrição doproblema é clara e compreensível?
    Acurácia: A descrição do problema é precisa e relevante?
Descrição dos Dados:
    Completude: Todos os conjuntos de dados relevantes são descritos com detalhes suficientes?
    Análise de Qualidade de Dados: A qualidade e as características dos dados são discutidas (por exemplo, valores ausentes, outliers)?
    Visualização: Os dados são bem visualizados usando gráficos ou tabelas?
Metodologia:
    Abordagem: A metodologia escolhida é adequada para resolver o problema de análise de dados?
    Justificativa: Há uma justificativa clara para o motivo pelo qual métodos ou técnicas específicas foram escolhidos?
    Implementação: A implementação da metodologia é descrita com precisão e detalhes?
Resultados:
    Precisão: Os resultados são precisos e consistentes com os objetivos da análise?
    Entendimento: Os resultados são interpretados e discutidos adequadamente?
    Visualização: Os resultados são visualizados de forma eficaz e fáceis de entender (por exemplo, gráficos, tabelas)?
Conclusão:
    Resumo: A conclusão resume sucintamente as principais descobertas do relatório?
    Implicações: As implicações dos resultados são discutidas?
    Recomendações: Há recomendações acionáveis ou próximas etapas?
"""


JUDGE = """
Você vai receber um relatório gerado por um LLM sobre a limpeza de um coluna de um dataframe pandas realiza por dois 
codificadores. Sua tarefa é atribuir uma pontuação de 0 a 150 para o relatório seguindo os critérios abaixo:

Deascrição do problema:
    Clareza: 10 pontos
    Acurácia: 10 pontos
Descrição dos dados:
    Completude: 10 pontos
    Análise da qualidade dos dados: 10 pontos
    Visualização: 10 pontos
Metodologia:
    Abordagem: 10 pontos
    Justificativa: 10 pontos
    Implementação: 10 pontos
Resultados:
    Precisão: 10 pontos
    Compreensão: 10 pontos
    Visualização: 10 pontos
Conclusão:
    Resumo: 10 pontos
    Implicações: 10 pontos
    Recomendações: 10 pontos

Pontuação total possível: 150 pontos

"""
