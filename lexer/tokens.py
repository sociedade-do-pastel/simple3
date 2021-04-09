"""
Definição de regex e tokens da linguagem
"""

tokens = {
    # Palavra-chave que representa o tipo de valor booleano
    # Utilização:
    #     tof tst = tru;
    "tof": "keyword",

    # Palavra-chave que representa o início de um controle de fluxo do tipo if
    # Utilização:
    #     ifi tst == fls {...
    "ifi": "keyword",

    # Palavra-chave que representa o início de um controle de fluxo do tipo
    # else
    # Utilização:
    #     els {...
    "els": "keyword",

    # Palavra-chave que representa o início de um controle de fluxo do tipo
    # else if
    # Utilização:
    #     elf tst == tru {...
    "elf": "keyword",

    # Palavra-chave que representa o início de um laço do tipo while
    # Utilização:
    #     whl tst == tru {...
    "whl": "keyword",

    # Palavra-chave que representa o início de um laço do tipo for
    # Utilização:
    #     for tst = 0:10 {...
    "for": "keyword",

    # Palavra chave que representa o tipo string
    # Utilização:
    #     str tst = "eu sou uma string";
    "str": "type",

    # Palavra-chave que representa o tipo primitivo numérico
    # (int, float, double etc)
    # Utilização:
    #     num tst = 3.1415;
    "num": "type",

    # Palavra-chave que representa o comando break, que encerra um laço de
    # repetição
    # Utilização:
    #     for tst = 0:10 {...
    #         ...
    #         brk;
    #     }
    "brk": "keyword",

    # Palavra-chave que representa o comando continue, que salta para a próxima
    # iteração em um laço de repetição
    # Utilização:
    #     for tst = 0:10 {...
    #         ...
    #         jmp;
    #     }
    "jmp": "keyword",

    # Palavra-chave que representa o comando return, utilizado para transmitir
    # alguma informação como saída de uma função
    # Utilização:
    #     {
    #         ...
    #         ret tru;
    #     }
    "ret": "keyword",

    # Palavra-chave que representa a declaração de um vetor
    # Utilização:
    #     vec<num> tst = [1, 3.14, 22];
    "vec\\<(num|str)\\>": "keyword",

    # identifiers

    # Regex para definição de nomes de variáveis
    # Possuindo caracteres entre 65 e 122 da tabela ASCII
    # com no máximo 3 caracteres (case sensitive)
    # Total de combinações: 57^3 = 185193
    # (keywords não contabilizadas)
    "[A-z]{3}": "var",

    # Regex para definição do tipo num
    # Tipo genérico para qualquer numeral, incluindo int, float e double
    "[0-9]+(\\.[0-9]+)?": "num",

    # Regex para definição de funções
    # Assinatura:
    #     tipo nome_da_funcao(tipo parametro, ...)
    "(num|str|emp) [A-z]{3}\\(((num|str) [A-z]{3}, *)*(((num|str) [A-z]{3}){1})?\\)": "func",

    # Regex para chamada de funções
    # nome_da_funcao(argumento1, argumento2 ..., argumenton)
    "[A-z]{3}\\((.*, *)*((.*){1})?\\)": "func_call",

    # Identificador de vazio
    # Utilizado para verificar a inexistência de valor ou tamanho
    "emp": "emp",

    # Regex para definição de string
    # Qualquer caracter entre duas aspas duplas (""), excluso aspas internas
    "\"[^\"]*\"": "str",

    # Regex para definição de comentários
    # Assinatura:
    #     /3...\n
    # Observações:
    #     Há somente comentários de linha completa
    "^(\\/3).*(\n)$": "comment",

    # Identificador de início de escopo
    # Assinatura:
    #     {...
    "{": "scope_init",

    # Identificador de fim de escopo
    # Assinatura:
    #     ...}
    "}": "scope_end",

    # Identificador do tipo booleano tru (true)
    "tru": "booleanT",

    # Identificador do tipo booleano fls (false)
    "fls": "booleanF",

    # Identificador de fim de sentença (end of statement)
    # Assinatura:
    #     ...;
    ";": "eos",

    # operators

    # Operador binário para soma algébrica entre dois números (num)
    # Utilização:
    #          4 + 4
    #            --> 8
    "\\+": "operator",

    # Operador binário para subtração algébrica entre dois números (num)
    # Utilização:
    #          4 - 4
    #            --> 0
    "\\-": "operator",

    # Operador binário para multiplicação algébrica entre dois números (num)
    # Utilização:
    #          4 * 4
    #            --> 16
    "\\*": "operator",

    # Operador binário para divisão algébrica entre dois números (num)
    # Utilização:
    #          4 / 4
    #            --> 1
    "\\/": "operator",

    # Operador binário para exponenciação de um número qualquer x (num)
    # elevado a um número y (num)
    # Utilização:
    #          4^4
    #            --> 256
    "\\^": "operator",

    # Operador binário para comparação entre dois operandos
    # (esquerdo e direito), retorna tru se
    # o operando esquerdo for numericamente maior que o direito,
    # fls caso contrário
    # Utilização:
    #          4 > 3
    #            --> tru
    "\\>": "operator",

    # Operador binário para comparação entre dois operandos
    # (esquerdo e direito), retorna tru se
    # o operando esquerdo for numericamente maior ou igual ao direito,
    # fls caso contrário
    # Utilização:
    #          4 >= 3
    #            --> tru
    "\\>\\=": "operator",

    # Operador binário para comparação entre dois operandos
    # (esquerdo e direito), retorna tru se
    # o operando esquerdo for numericamente menor, fls caso contrário
    # Utilização:
    #          4 < 3
    #            --> fls
    "\\<": "operator",

    # Operador binário para comparação entre dois operandos
    # (esquerdo e direito), retorna tru se
    # o operando esquerdo for numericamente menor ou igual ao direito,
    # fls caso contrário:
    #          4 <= 3
    #            --> fls
    "\\<\\=": "operator",

    # Operador binário para atribuição de um valor numérico (num),
    # string (str), nulo (emp) ou booleano (tof)
    # à uma variável nomeada
    # Utilização:
    #       num jaj = 4
    "\\=": "operator",

    # Operador binário para comparação de igualdade entre dois operandos
    # (esquerdo e direito),
    # retorna tru se o operando esquerdo for numericamente igual ao direito,
    # fls caso contrário
    # Utilização:
    #         4 == 4
    #           --> tru
    "\\=\\=": "operator",

    # Operador unário booleano/buliano para a negação do valor de uma
    # variável ou operando booleano (tof)
    # Utilização:
    #          !tru
    #                 --> fls
    "\\!": "operator",

    # Operador binário booleano *ou*. Retorna tru caso um dos operandos
    # resultem em valores tru, fls caso contrário
    # Utilização:
    #          tru orr fls
    #              --> tru
    "orr": "operator",

    # Operador binário booleano *e*. Retorna tru caso ambos resultem em
    # valores tru, fls caso contrário
    # Utilização:
    #          tru and fls
    #              --> fls
    "and": "operator",

    # Operador binário para definicao de ranges. Recebe dois *num* e define
    # um range
    # Utilização:
    #          0:1
    #           --> range de zero a um
    ":": "operator"
}
