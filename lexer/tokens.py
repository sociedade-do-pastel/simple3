"""
Definição de regex e tokens da linguagem
"""

tokens = {
    # Palavra-chave para tipo booleano tru (true)
    "tru": "tru",

    # Palavra-chave para tipo booleano fls (false)
    "fls": "fls",
    
    # Palavra-chave que representa o tipo de valor booleano
    # Utilização:
    #     tof tst = tru;
    "tof": "tof",

    # Palavra-chave que representa o início de um controle de fluxo do tipo if
    # Utilização:
    #     ifi tst == fls {...
    "ifi": "ifi",

    # Palavra-chave que representa o início de um controle de fluxo do tipo
    # else
    # Utilização:
    #     els {...
    "els": "els",

    # Palavra-chave que representa o início de um controle de fluxo do tipo
    # else if
    # Utilização:
    #     elf tst == tru {...
    "elf": "elf",

    # Palavra-chave que representa o início de um laço do tipo while
    # Utilização:
    #     whl tst == tru {...
    "whl": "whl",

    # Palavra-chave que representa o início de um laço do tipo for
    # Utilização:
    #     for tst = 0:10 {...
    "for": "for",

    # Palavra chave que representa o tipo string
    # Utilização:
    #     str tst = "eu sou uma string";
    "str": "str",

    # Palavra-chave que representa o tipo primitivo numérico
    # (int, float, double etc)
    # Utilização:
    #     num tst = 3.1415;
    "num": "num",

    # Palavra-chave que representa o comando break, que encerra um laço de
    # repetição
    # Utilização:
    #     for tst = 0:10 {...
    #         ...
    #         brk;
    #     }
    "brk": "brk",

    # Palavra-chave que representa o comando continue, que salta para a próxima
    # iteração em um laço de repetição
    # Utilização:
    #     for tst = 0:10 {...
    #         ...
    #         jmp;
    #     }
    "jmp": "jmp",

    # Palavra-chave que representa o comando return, utilizado para transmitir
    # alguma informação como saída de uma função
    # Utilização:
    #     {
    #         ...
    #         ret tru;
    #     }
    "ret": "ret",

    # Caractere de início de escopo
    # Assinatura:
    #     {...
    "{": "scope_init",

    # Caractere de fim de escopo
    # Assinatura:
    #     ...}
    "}": "scope_end",

    # Caractere para delimitação de chamada ou definição de função
    # Assinatura:
    #     {...
    "(": "(",

    # Caractere para delimitação de chamada ou definição de função
    # Assinatura:
    #     ...}
    ")": ")",

    # Caractere para definição ou acesso a vetor
    # Assinatura:
    #     {...
    "[": "[",

    # Caractere para definição ou acesso a vetor
    # Assinatura:
    #     ...}
    "]": "]",
    
    # Caractere de fim de sentença (end of statement)
    # Assinatura:
    #     ...;
    ";": "eos",

    # identifiers

    # Regex para definição de nomes de variáveis
    # Possuindo caracteres entre 65 e 122 da tabela ASCII
    # com no máximo 3 caracteres (case sensitive)
    # Total de combinações: 57^3 = 185193
    # (keywords não contabilizadas)
    "[A-z]{3}": "var",

    # literals
    
    # Regex para definição do tipo num
    # Tipo genérico para qualquer numeral, incluindo int, float e double
    "[0-9]+(\\.[0-9]+)?": "num",
  
    # Identificador de vazio
    # Utilizado para verificar a inexistência de valor ou tamanho
    "emp": "emp",

    # Regex para definição de string
    # Qualquer caracter entre duas aspas duplas (""), excluso aspas internas
    "\"[^\"]*\"": "str",

    # Regex para definição de comentários
    # Assinatura:
    #     /3...
    # Observações:
    #     Há somente comentários de linha completa
    "^(\\/3).*$": "comment",
    
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
    # um range. Obs: este não retorna "operator" devido à dificuldade
    # de diferenciação entre operadores na análise sintática 
    # Utilização:
    #          0:1
    #           --> range de zero a um
    ":": ":"
}

