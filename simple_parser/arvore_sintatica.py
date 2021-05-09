from abc import ABC, abstractmethod


class Node(ABC):
    '''
    Classe abstrata representante de cada nó da árvore,
    seus métodos obrigatórios a serem implementados são:

    solve -- soluciona a expressão válida na gramática através do Python.
    __str__ -- apresenta a expressão baseada na estrutura dos nós filhos
    na sintaxe da linguagem Python.
    '''
    @abstractmethod
    def solve(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class BinOp(Node):
    '''
    Essa classe representa uma operação binária na linguagem e herda de Node;

    Uma operação binária pode ser do tipo
    "+", "-", "*", "/", ":", "and", "orr",
    ">=", "<=", "==", "<", ">", "^" e ":".
    '''

    def __init__(self, left, operator, right):
        '''
        Construtor padrão da classe.

        Argumentos:

        left  -- nó esquerdo da opearção
        right -- nó direito da operação
        token -- token o qual contém o operador
        '''
        self.left = left
        self.right = right
        self.operator = operator

    def solve(self):
        pass

    def __str__(self):
        if self.operator == ":":
            return f"range({self.left}, {self.right})"
        elif self.operator == "^":
            return f"( {self.left} ** {self.right} )"
        else:
            return f"( {self.left} {self.operator} {self.right} )"


class UnOP(Node):
    '''
    Essa classe cria um nó da árvore representando uma operação unária.

    Uma operação unária pode ser do tipo
    "!" (negação).
    '''

    def __init__(self, operator, operand):
        '''
        Toda operação unária apresenta um único nó filho:

        Argumentos:

        token -- token representando a operação (! apenas até o momento)
        operand -- operando da operação

        '''
        self.operator = operator
        self.operand = operand

    def solve(self):
        pass

    def __str__(self):
        pass

# Tokens literais (símbolos não terminais)
# Os nós a seguir simbolizam os não terminais literais da gramática:
# str (qualquer string), num (int ou float) e bool (tru ou fls)


class Num(Node):
    '''
    Podendo ser um float ou int da linguagem Python, o num é um nó que pode
    assumir esse valor e somente esse valor.
    '''

    def __init__(self, value):
        '''
        Construtor padrão de um nó numérico.

        Argumentos:

        value -- Valor numérico da variável
        '''
        self.value = value

    def solve(self):
        pass

    def __str__(self):
        return self.value


class Str(Node):
    '''
    Representa uma string da linguagem.
    '''

    def __init__(self, value):
        '''
        Construtor padrão de um nó de string.

        Argumentos:

        value -- Valor da string da variável, pode ter qualquer tamanho que
        o Python possa aceitar.
        '''
        self.value = value

    def solve(self):
        pass

    def __str__(self):
        return self.value


class Bool(Node):
    '''
    Nó o qual representa um booleano da linguagem.
    '''

    def __init__(self, value):
        '''
        Construtor padrão de um nó de um booleano.

        Argumentos:

        value -- tru (true/t) ou fls (false/nil)
        '''
        self.value = value

    def solve(self):
        pass

    def __str__(self):
        return self.value


class Emp(Node):
    '''
    Vazio/undefined/nullptr da linguagem, o token assume o mesmo nome que
    o nó.
    '''

    def __init__(self, value):
        '''
        Construtor padrão de um nó de um booleano.

        Argumentos:

        value -- emp
        '''
        self.value = value

    def solve(self):
        pass

    def __str__(self):
        return self.value
# Type
# durante a declaração de variável nesta linguagem fracamente tipada,
# uma variável pode assumir o tipo Str, num ou tof


class Type(Node):
    '''
    Tipo da variável a ser declarada.
    '''

    def __init__(self, value):
        '''
        Construtor padrão de um nó de um tipo.

        Argumentos:

        value -- literalmente as palavras num, str ou tof
        '''
        self.value = value

    def solve(self):
        pass

    def __str__(self):
        return self.value

# Var
# Ou também identificador/identifier, recebe uma string de três letras
# para identificar uma variável.


class Var(Node):
    '''
    Identificador para a variável, podendo receber três letras.
    '''

    def __init__(self, value):
        '''
        Construtor padrão de um nó de um identificador de variável.

        Argumentos:

        value -- string de 3 letras que nomeia uma variável a ser declarada
        '''
        self.value = value

    def solve(self):
        pass

    def __str__(self):
        return self.value

# Estruturas relacionadas a controle de fluxo


class Control(Node):
    '''
    As estruturas de repetição da linguagem (for e whl) podem ser controladas
    ambas com brk (break) ou jmp (continue). Esse nó pode assumir um desses
    possíveis valores.
    '''

    def __init__(self, value):
        '''
        Construtor padrão de um nó o qual representa a parada ou não
        de um laço de repetição

        Argumentos:

        value -- pode assumir os valores brk ou jmp
        '''
        self.value = value

    def solve(self):
        pass

    def __str__(self):
        return self.value


class Decvar(Node):
    def __init__(self, var_type, var, literal):
        '''
            Construtor padrão de um nó o qual representa a declaração
            de uma variável

            Argumentos:

            var_type -- recebe uma instância da classe Type
            var -- recebe uma instância da classe Var
            literal -- recebe uma instância da classe Num, Str ou Bool
        '''
        self.var_type = var_type
        self.var = var
        self.literal = literal

    def solve(self):
        pass

    def __str__(self):
        return f"{self.var} = {self.literal}"


class Whl(Node):
    '''
    Nó o qual representa uma estrutura de repetição whl (while/do).
    Seu nó filho pode conter todas as estruturas do programa (S).
    '''

    def __init__(self, expr, s):
        '''
        Argumentos:

        expr -- expressão teste que induza a execução do laço
        s -- não terminal inicial representando todas as partes da linguagem
        '''
        self.expr = expr
        self.s = s
        self.tab = ""

    def tabify(self):
        self.tab += "\t"

    def solve(self):
        pass

    def __str__(self):
        result = ""
        for line in self.s:
            if isinstance(line, (Whl, For, Ifi)):
                line.tabify()
            result += f"{self.tab}\t{line}\n"
        return f"{self.tab}while {self.expr}:\n{result}"


class For(Node):
    '''
    Semelhante ao whl, um laço for geralmente tem fim defindo (range).
    Este nó representa essa estrutura.
    '''

    def __init__(self, typo, var, rang, s):
        self.typo = typo
        self.var = var
        self.rang = rang
        self.s = s
        self.tab = ""

    def tabify(self):
        self.tab += "\t"

    def solve(self):
        pass

    def __str__(self):
        result = ""
        for line in self.s:
            if isinstance(line, (Whl, For, Ifi)):
                line.tabify()
            result += f"{self.tab}\t{line}\n"
        return f"for {self.var} in {self.rang}:\n{result}"


class Ifi(Node):
    def __init__(self, expr, s, els):
        self.expr = expr
        self.s = s
        self.els = els
        self.tab = ""

    def tabify(self):
        self.tab += "\t"

    def solve(self):
        pass

    def __str__(self):
        result = ""
        if self.els is None:
            els = ""
        else:
            self.els.tabify()
            els = str(self.els)

        for line in self.s:
            if isinstance(line, (Whl, For, Ifi, Els)):
                line.tabify()
            result += f"{self.tab}\t{line}\n"
        return f"if {self.expr}:\n{result}{els}"


class Els(Node):
    def __init__(self, s):
        self.s = s
        self.tab = ""

    def tabify(self):
        self.tab += "\t"

    def solve(self):
        pass

    def __str__(self):
        result = ""

        for line in self.s:
            if isinstance(line, (Whl, For, Ifi)):
                line.tabify()
            result += f"{self.tab}\t{line}\n"
        return f"{self.tab}else:\n{result}"
