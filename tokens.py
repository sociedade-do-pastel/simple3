# Leon Ferreira Bellini    | 22.218.002-8
# Felipe Maciel de Sousa   | 22.218.042-4
# Pedro Freitas Barbosa    | 22.218.013-5
# Guilherme Ormond Sampaio | 22.218.007-7

tokens = {
    # keywords
    "dcl" : "keyword",          # def (declare)
    "ifi" : "keyword",          # if
    "els" : "keyword",          # else
    "elf" : "keyword",          # elif
    "whl" : "keyword",          # while
    "for" : "keyword",          # for
    "str" : "keyword",          # str
    "num" : "keyword",          # numeric type (int, float, double)
    "tru" : "keyword",          # True
    "fls" : "keyword",          # False
    "emp" : "keyword",          # None, nil, null, similares
    "brk" : "keyword",          # break
    "jmp" : "keyword",          # jump
    "ret" : "keyword",          # return
    "vec" : "keyword",          # vector "vec\<(num|str)\>"                       
    # identifiers
    "[A-z]{3}" : "var",         # 3 caracteres max, entre A-z
    "" : "func",                    
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
    "\!"  : "!"
}
