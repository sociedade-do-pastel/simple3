# Leon Ferreira Bellini    | 22.218.002-8
# Felipe Maciel de Sousa   | 22.218.042-4
# Pedro Freitas Barbosa    | 22.218.013-5
# Guilherme Ormond Sampaio | 22.218.007-7

tokens = {
    # keywords
    "dcl" : "keyword",              # def (declare)
    "tof" : "keyword",              # boolean, true or false
    "ifi" : "keyword",              # if
    "els" : "keyword",              # else
    "elf" : "keyword",              # elif
    "whl" : "keyword",              # while
    "for" : "keyword",              # for
    "str" : "type",                 # str
    "num" : "type",                 # numeric type (int, float, double)
    "brk" : "keyword",              # break
    "jmp" : "keyword",              # continue
    "ret" : "keyword",              # return
    "vec\<(num|str)\>" : "keyword", # vector "vec\<(num|str)\>"                       
    # identifiers

    """
        Regex para definição de nomes de variáveis
        Possuindo caracteres entre 65 e 122 da tabela ASCII
        com no máximo 3 caracteres (case sensitive)
        Total de combinações: 3^57 = 1570042899082081611640534563 
        (keywords não contabilizadas)
    """
    
    "[A-z]{3}" : "var",

    
    """
        Regex para definição do tipo num
        Tipo genérico para qualquer numeral, incluindo int, float e double
    """
    
    "[0-9]+(\.[0-9]+)?" : "num",

    
    """
        Regex para definição de funções
        Assinatura:
            tipo nome_da_funcao(tipo parametro, ...)
    """
    
    "([A-z]{3}|[0-9]+(\.[0-9]+)?){1} [A-z]{3}\((((([A-z]{3}|[0-9]+(\.[0-9]+)?){1} [A-z]{3}),[ ]*)*(([A-z]{3}|[0-9]+(\.[0-9]+)?){1} [A-z]{3}){1})?\)" : "func",

    
    """
        Identificador de vazio
        Utilizado para verificar a inexistência de valor ou tamanho
    """
    
    "emp" : "emp",

    
    """
        Regex para definição de string
        Qualquer caracter entre duas aspas duplas (""), excluso aspas internas
    """
    
    "\"[^\"]*\"" : "str",


    """
        Regex para definição de comentários
        Assinatura:
            /3...\n
        Observações:
            Há somente comentários de linha completa
    """
    
    "^(\/3).*(\n)$" : "comment",


    """
        Identificador de início de escopo
        Assinatura:
            {...
    """
    
    "\{" : "scope_init",


    """
        Identificador de fim de escopo
        Assinatura:
            ...}
    """
    
    "\}" : "scope_end",


    """
        Identificador do tipo booleano tru (true)
    """
    
    "tru" : "booleanT",


    """
        Identificador do tipo booleano fls (false)
    """
    
    "fls" : "booleanF",


    """
        Identificador de fim de sentença (end of statement)
        Assinatura:
            ...;
    """
    
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

