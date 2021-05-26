from abc import ABC, abstractmethod
from . import sym_table as syt

var_table = syt.SymbolsTable()


def erro(err):
    raise Exception(err)


class Node(ABC):
    """
    Classe abstrata representante de cada nó da árvore,
    seus métodos obrigatórios a serem implementados são:

    solve -- soluciona a expressão válida na gramática através do Python.
    __str__ -- apresenta a expressão baseada na estrutura dos nós filhos
    na sintaxe da linguagem Python.
    """

    @abstractmethod
    def solve(self):
        """Função abstrata para validar operações."""
        pass

    @abstractmethod
    def __str__(self):
        """Função abstrata para gerar código."""
        pass


class BinOp(Node):
    """
    Essa classe representa uma operação binária na linguagem e herda de Node;

    Uma operação binária pode ser do tipo
    "+", "-", "*", "/", ":", "^", ":",
    ">=", "<=", "==", "<" e ">".
    """

    def __init__(self, left, operator, right):
        """
        Construtor padrão da classe.

        Argumentos:

        left  -- nó esquerdo da opearção
        right -- nó direito da operação
        token -- token o qual contém o operador
        """
        self.left = left
        self.right = right
        self.operator = operator

    def solve(self):
        esquerda = self.left.solve()
        direita = self.right.solve()

        if self.operator in ("+", "-", "*", "/", "^",
                             ":", ">=", "<=", ">", "<"):
            if not isinstance(esquerda, Num) or not isinstance(direita, Num):
                erro(f"Erro semântico: operação {self.operator} só pode ser feitas com dois números")
            return Num(0)
        elif self.operator == "==":
            if isinstance(esquerda, Var) or isinstance(direita, Var):
                if isinstance(esquerda.value, type(direita.value)):
                    return esquerda
            elif isinstance(esquerda, type(direita)):
                return esquerda

            erro(f"Erro semântico: operação {self.operator} só pode ser feitas com dois tipos iguais")

    def __str__(self):
        if self.operator == ":":
            return f"range({self.left}, {self.right})"
        elif self.operator == "^":
            return f"( {self.left} ** {self.right} )"
        else:
            return f"( {self.left} {self.operator} {self.right} )"


class UnOP(Node):
    """
    Essa classe cria um nó da árvore representando uma operação unária.

    Uma operação unária pode ser do tipo
    "!" (negação).
    """

    def __init__(self, operator, operand):
        """
        Toda operação unária apresenta um único nó filho.

        Argumentos:

        token -- token representando a operação (! apenas até o momento)
        operand -- operando da operação

        """
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
    """
    Podendo ser um float ou int da linguagem Python, o num é um nó que pode
    assumir esse valor e somente esse valor.
    """

    def __init__(self, value):
        """
        Construtor padrão de um nó numérico.

        Argumentos:

        value -- Valor numérico da variável
        """
        self.value = value

    def solve(self):
        return self

    def __str__(self):
        return self.value


class Str(Node):
    """
    Representa uma string da linguagem.
    """

    def __init__(self, value):
        """
        Construtor padrão de um nó de string.

        Argumentos:

        value -- Valor da string da variável, pode ter qualquer tamanho que
        o Python possa aceitar.
        """
        self.value = value

    def solve(self):
        return self

    def __str__(self):
        return self.value


class Bool(Node):
    """
    Nó o qual representa um booleano da linguagem.
    """

    def __init__(self, value):
        """
        Construtor padrão de um nó de um booleano.

        Argumentos:

        value -- tru (true/t) ou fls (false/nil)
        """
        self.value = value

    def solve(self):
        return self

    def __str__(self):
        if self.value == "tru":
            return "True"
        elif self.value =="fls":
            return "Falseh"


class Emp(Node):
    """
    Vazio/undefined/nullptr da linguagem, o token assume o mesmo nome que
    o nó.
    """

    def __init__(self, value):
        """
        Construtor padrão de um nó de um booleano.

        Argumentos:

        value -- emp
        """
        self.value = value

    def solve(self):
        return self

    def __str__(self):
        return self.value
# Type
# durante a declaração de variável nesta linguagem fracamente tipada,
# uma variável pode assumir o tipo Str, num ou tof


class Type(Node):
    """
    Tipo da variável a ser declarada.
    """

    def __init__(self, value):
        """
        Construtor padrão de um nó de um tipo.

        Argumentos:

        value -- literalmente as palavras num, str ou tof
        """
        self.value = value

    def solve(self):
        return self

    def __str__(self):
        return self.value

# Var
# Ou também identificador/identifier, recebe uma string de três letras
# para identificar uma variável.


class Var(Node):
    """
    Identificador para a variável, podendo receber três letras.
    """

    def __init__(self, value):
        """
        Construtor padrão de um nó de um identificador de variável.

        Argumentos:

        value -- string de 3 letras que nomeia uma variável a ser declarada
        """
        self.value = value

    def solve(self):
        var_in_table = var_table.lookup(self.value)
        if not var_in_table:
            erro(f"Erro semântico: variável {self.value} usada mas não declarada")
        else:
            dic_temp = {"num": Num(0), "str": Str(""), "tof": Bool("tru")}
            return dic_temp[var_in_table["type"]]

    def __str__(self):
        return self.value

# Estruturas relacionadas a controle de fluxo


class Control(Node):
    """
    As estruturas de repetição da linguagem (for e whl) podem ser controladas
    ambas com brk (break) ou jmp (continue). Esse nó pode assumir um desses
    possíveis valores.
    """

    def __init__(self, value):
        """
        Construtor padrão de um nó o qual representa a parada ou não
        de um laço de repetição

        Argumentos:

        value -- pode assumir os valores brk ou jmp
        """
        self.value = value
        self.inside_loop = False
        self.scope = 0

    def solve(self):
        if not self.inside_loop:
            erro(f"Erro semântico: uso de {self.value} fora de uma estrutura de repetição")

    def __str__(self):
        if self.value == "brk":
            return "break"
        elif self.value == "jmp":
            return "continue"


class Decvar(Node):
    def __init__(self, var_type, var, literal):
        """
            Construtor padrão de um nó o qual representa a declaração
            de uma variável

            Argumentos:

            var_type -- recebe uma instância da classe Type
            var -- recebe uma instância da classe Var
            literal -- recebe uma instância da classe Num, Str ou Bool
        """
        self.var_type = var_type
        self.var = var
        self.literal = literal
        self.scope = 0

    def solve(self):
        var_in_table = var_table.lookup(self.var.value)

        if var_in_table and var_in_table["type"] != self.var_type.value:
            erro(f"Erro semântico: {self.var} declarado anteriormente com tipo {var_in_table['type']} ao invés de {self.var_type}")

        literal_temp = self.literal
        if isinstance(self.literal, (BinOp, Var)):
            literal_temp = self.literal.solve()

        if self.var_type.value == "num" and not isinstance(literal_temp, Num):
            erro(f"Erro semântico: {self.literal} não pode ser declarado como num")
        elif self.var_type.value == "str" and not isinstance(literal_temp, Str):
            erro(f"Erro semântico: {self.literal} não pode ser declarado como str")
        elif self.var_type.value == "tof" and not isinstance(literal_temp, Bool):
            erro(f"Erro semântico: {self.literal} não pode ser declarado como tof")

        var_table.insert(self.var.value, self.var_type.value, self.scope)

    def __str__(self):
        tabs = "\t" * self.scope
        return f"{tabs}{self.var} = {self.literal}"


class Whl(Node):
    """
    Nó o qual representa uma estrutura de repetição whl (while/do).
    Seu nó filho pode conter todas as estruturas do programa (S).
    """

    def __init__(self, expr, s):
        """
        Argumentos:

        expr -- expressão teste que induza a execução do laço
        s -- não terminal inicial representando todas as partes da linguagem
        """
        self.expr = expr
        self.s = s
        self.tab = ""
        self.scope = 0

    def solve(self):
        r = self.expr.solve()
        if isinstance(r, Str):
            erro("Erro semântico: Expressão de whl não pode ser str")
        for line in self.s:
            if isinstance(line, Control):
                line.inside_loop = True
            line.scope = self.scope + 1
            line.solve()

        var_table.remove_by_scope(self.scope+1)

    def __str__(self):
        result = ""
        eol = "\n"

        self.tab = "\t" * self.scope

        for line in self.s:
            if line == self.s[-1]:
                eol = ""
            result += f"{line}{eol}"
        return f"{self.tab}while {self.expr}:\n{result}"


class For(Node):
    """
    Semelhante ao whl, um laço for geralmente tem fim defindo (range).
    Este nó representa essa estrutura.
    """

    def __init__(self, typo, var, rang, s):
        self.typo = typo
        self.var = var
        self.rang = rang
        self.s = s
        self.tab = ""
        self.scope = 0

    def solve(self):
        var_in_table = var_table.lookup(self.var.value)

        if self.typo and var_in_table:
            erro(f"Erro semântico: {self.var} já foi declarado anteriormente")
        elif self.typo and not var_in_table:
            if self.typo != "num":
                erro(f"Erro semântico: {self.var} declarado como {self.typo} para operador range")
            else:
                var_table.insert(self.var.value, self.typo, self.scope)
        elif not self.typo and not var_in_table:
            erro(f"Erro semântico: {self.var} usado mas não declarado")
        elif not self.typo and var_in_table and var_in_table["type"] != "num":
            erro(f"Erro semântico: variável {self.var} é {var_in_table['type']}, deve ser num")

        self.rang.solve()

        for line in self.s:
            if isinstance(line, Control):
                line.inside_loop = True
            line.scope = self.scope + 1
            line.solve()

        var_table.remove_by_scope(self.scope+1)

    def __str__(self):
        result = ""
        eol = "\n"

        self.tab = "\t" * self.scope

        for line in self.s:
            if line == self.s[-1]:
                eol = ""
            result += f"{line}{eol}"
        return f"{self.tab}for {self.var} in {self.rang}:\n{result}"


class Ifi(Node):
    def __init__(self, expr, s, els):
        self.expr = expr
        self.s = s
        self.els = els
        self.tab = ""
        self.scope = 0

    def solve(self):
        self.expr.solve()

        for line in self.s:
            line.scope = self.scope + 1
            line.solve()

        var_table.remove_by_scope(self.scope+1)

        if self.els:
            self.els.scope = self.scope
            self.els.solve()

    def __str__(self):
        result = ""
        els = ""
        eol = "\n"

        self.tab = "\t"*self.scope

        if self.els:
            els = str(self.els)

        for line in self.s:
            if line == self.s[-1] and not self.els:
                eol = ""
            result += f"{line}{eol}"
        return f"{self.tab}if {self.expr}:\n{result}{els}"

class Els(Node):
    def __init__(self, s):
        self.s = s
        self.tab = ""
        self.scope = 0

    def solve(self):
        for line in self.s:
            line.scope = self.scope + 1
            line.solve()
        var_table.remove_by_scope(self.scope+1)

    def __str__(self):
        result = ""
        eol = "\n"

        self.tab = "\t" * self.scope

        for line in self.s:
            if line == self.s[-1]:
                eol = ""
            result += f"{line}{eol}"
        return f"{self.tab}else:\n{result}"
