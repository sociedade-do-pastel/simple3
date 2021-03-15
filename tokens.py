# Leon Ferreira Bellini    | 22.218.002-8
# Felipe Maciel de Sousa   | 22.218.042-4
# Pedro Freitas Barbosa    | 22.218.013-5
# Guilherme Ormond Sampaio | 22.218.007-7

tokens = {
    """
        Palavra-chave que representa o tipo de valor booleano
        Utilização:
            tof tst = tru;
    """
    "tof" : "keyword",

    """
        Palavra-chave que representa o início de um controle de fluxo do tipo if
        Utilização:
            if tst == fls {...
    """
    "ifi" : "keyword",
    
    """
        Palavra-chave que representa o início de um controle de fluxo do tipo else
        Utilização:
            else {...
    """
    "els" : "keyword",

    """
        Palavra-chave que representa o início de um controle de fluxo do tipo else if
        Utilização:
            elf tst == tru {...
    """
    "elf" : "keyword",

    """
        Palavra-chave que representa o início de um laço do tipo while
        Utilização:
            whl tst == tru {...
    """
    "whl" : "keyword",

    """
        Palavra-chave que representa o início de um laço do tipo for
        Utilização:
            for tst = 0:10 {...
    """
    "for" : "keyword",

    """
        Palavra chave que representa o tipo string
        Utilização:
            str tst = "eu sou uma string";
    """
    "str" : "type",

    """
        Palavra-chave que representa o tipo primitivo numérico (int, float, double etc)
        Utilização:
            num tst = 3.1415;
    """
    "num" : "type",

    """
        Palavra-chave que representa o comando break, que encerra um laço de repetição
        Utilização:
            for tst = 0:10 {...
                ...
                brk;
            }
    """
    "brk" : "keyword",

    """
        Palavra-chave que representa o comando continue, que salta para a próxima 
        iteração em um laço de repetição
        Utilização:
            for tst = 0:10 {...
                ...
                jmp;
            }
    """
    "jmp" : "keyword",

    """
        Palavra-chave que representa o comando return, utilizado para transmitir 
        alguma informação como saída de uma função
        Utilização:
            {
                ...
                ret tru;
            } 
    """
    "ret" : "keyword",

    """
        Palavra-chave que representa a declaração de um vetor
        Utilização:
            vec<num> tst = [1, 3.14, 22];
    """
    "vec\<(num|str)\>" : "keyword",
                       
    # identifiers
    "[A-z]{3}" : "var",             # 3 caracteres max, entre A-z
    "[0-9]+(\.[0-9]+)?" : "num",
    "([A-z]{3}|[0-9]+(\.[0-9]+)?){1} [A-z]{3}\((((([A-z]{3}|[0-9]+(\.[0-9]+)?){1} [A-z]{3}),[ ]*)*(([A-z]{3}|[0-9]+(\.[0-9]+)?){1} [A-z]{3}){1})?\)" : "func", 
    "\"[^\"]*\"" : "str",
    "^(\/3).*(\n)$" : "comment",
    "\{" : "scope_init",
    "\}" : "scope_end",
    "tru" : "booleanT",             # True
    "fls" : "booleanF",             # False
    ";" : "eos",                    # end of statement
    # operator    
    "\+"  : "+",
    "\-"  : "-",
    "\*"  : "*",
    "\/"  : "/",
    "\^"  : "^",
    "\>"  : ">",
    "\>\=" : ">=",
    "\<"  : "<",
    "\<\=" : "<=",
    "\="  : "=",
    "\=\=" : "==",
    "\!"  : "!",
    "orr" : "or",
    "and" : "and"
}

