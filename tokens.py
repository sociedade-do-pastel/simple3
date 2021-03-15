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
    """
	Operador binário para soma algébrica entre dois números (num)
	Utilização:
		 4 + 4 
		   --> 8
    """
    "\+"  : "+",
    """
	Operador binário para subtração algébrica entre dois números (num)
	Utilização:   
		 4 - 4
		   --> 0
    """
    "\-"  : "-",
    """
	Operador binário para multiplicação algébrica entre dois números (num)
	Utilização:
		 4 * 4 
		   --> 16
    """
    "\*"  : "*",
    """
	Operador binário para divisão algébrica entre dois números (num)
	Utilização:
		 4 / 4  
		   --> 1
    """
    "\/"  : "/",
    """
	Operador binário para exponenciação de um número qualquer x (num) 
        elevado a um número y (num)
	Utilização:
		 4^4
		   --> 64
    """
    "\^"  : "^",
    """
	Operador binário para comparação entre dois operandos 
        (esquerdo e direito), retorna tru se
	o operando esquerdo for numericamente maior que o direito, 
        fls caso contrário
	Utilização:
		 4 > 3
		   --> tru
    """
    "\>"  : ">",
    """
	Operador binário para comparação entre dois operandos 
        (esquerdo e direito), retorna tru se
	o operando esquerdo for numericamente maior ou igual ao direito, 
        fls caso contrário
	Utilização:
		 4 >= 3
		   --> tru
    """
    "\>\=" : ">=",
    """
	Operador binário para comparação entre dois operandos 
        (esquerdo e direito), retorna tru se
	o operando esquerdo for numericamente menor, fls caso contrário
	Utilização:
		 4 < 3
		   --> fls
    """
    "\<"  : "<",
    """
	Operador binário para comparação entre dois operandos
        (esquerdo e direito), retorna tru se
	o operando esquerdo for numericamente menor ou igual ao direito, 
        fls caso contrário:
		 4 <= 3
		   --> fls

    """    
    "\<\=" : "<=",
    """
	Operador binário para atribuição de um valor numérico (num), 
        string (str), nulo (emp) ou booleano (tof) 
	à uma variável nomeada
	Utilização:
	      num jaj = 4
    """
    "\="  : "=",
    """
	Operador binário para comparação de igualdade entre dois operandos 
        (esquerdo e direito),
	retorna tru se o operando esquerdo for numericamente igual ao direito, 
        fls caso contrário
	Utilização:
		4 == 4
		  --> tru
    """
    "\=\=" : "==",
    """
	Operador unário booleano/buliano para a negação do valor de uma variável
        ou operando booleano (tof)
	Utilização:
		 !tru
			--> fls
    """
    "\!"  : "!",
    """
	Operador binário booleano *ou*. Retorna tru caso um dos operandos 
        resultem em valores tru, fls caso contrário
	Utilização:
		 tru orr fls
		     --> tru
    """
    "orr" : "or",
    """
	Operador binário booleano *e*. Retorna tru caso ambos resultem em 
        valores tru, fls caso contrário
	Utilização:
		 tru and fls
		     --> fls

    """
    "and" : "and"
}

