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
    "emp" : "keyword",              # None, nil, null, similares
    "brk" : "keyword",              # break
    "jmp" : "keyword",              # continue
    "ret" : "keyword",              # return
    "vec\<(num|str)\>" : "keyword", # vector "vec\<(num|str)\>"                       
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

