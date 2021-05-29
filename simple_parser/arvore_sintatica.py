#############################################################################################
# Árvore sintática abstrata cujo cada nó representa um elemento ou                          #
# operação da linguagem, os nós terminais sendo os /tokens/ definidos na GLC.               #
#############################################################################################

from abc import ABC, abstractmethod
from . import sym_table as syt
# símbolos serão importantes durante a análise semântica
var_table = syt.SymbolsTable()


def erro(err):
    """
    Função a qual representa um erro genérico ``levantado'' durante a análise.

    Argumentos:

    err - Mensagem relevante que informe a exception atual
    """
    raise Exception(err)


class Node(ABC):
    """
    Classe abstrata representante de cada nó da árvore.

    Seus métodos obrigatórios a serem implementados são:

    solve -- soluciona a expressão válida na gramática através do Python.
    __str__ -- apresenta a expressão baseada na estrutura dos nós filhos
    na sintaxe da linguagem Python.
    """

    @abstractmethod
    def solve(self):
        """Função abstrata para validar operações e varrer a árvore."""
        pass

    @abstractmethod
    def __str__(self):
        """Função abstrata para gerar código."""
        pass


class BinOp(Node):
    """
    Essa classe representa uma operação binária na linguagem e herda de Node.

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
        """Aqui são tratados os operadores possíveis em operações binárias."""
        esquerda = self.left.solve()
        direita = self.right.solve()

        if self.operator in ("+", "-", "*", "/", "^",
                             ":", ">=", "<=", ">", "<"):
            if not isinstance(esquerda, Num) or not isinstance(direita, Num):
                erro(f"Erro semântico: operação {self.operator} só pode ser feitas com dois números")
            return Num(0)
        elif self.operator in ("==", "!="):
            if isinstance(esquerda, Var) or isinstance(direita, Var):
                if isinstance(esquerda.value, type(direita.value)):
                    return esquerda
            elif isinstance(esquerda, type(direita)):
                return esquerda

            erro(f"Erro semântico: operação {self.operator} só pode ser feitas com dois tipos iguais")

    def __str__(self):
        """
        Transformação de código do operador binário.

        Este podendo gerar as seguintes ``strings'':

        expr1 ** expr2 - expr1 elevado ao expr2
        range(expr1, expr2) - intervalo fechado-aberto, [expr1, expr2[
        expr1 operator expr2 - expr (+ ou - ou / ou * ou ^ ...)
        """
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
        """Tratamentos necessários de tipo serão realizados para expr."""
        expr = self.operand.solve()
        if isinstance(expr, Str):
            erro(f"Erro semântico: operador unário {self.operator} não é possível com str")
        else:
            return expr

    def __str__(self):
        """Gerado código do tipo not (expr) (parens necessários!)."""
        if self.operator == "!":
            return f"not ({self.operand})"

# Tokens literais (símbolos não terminais)
# Os nós a seguir simbolizam os não terminais literais da gramática:
# str (qualquer string), num (int ou float) e bool (tru ou fls)


class Num(Node):
    """
    Podendo ser um float ou int da linguagem Python.

    O num é um nó que pode assumir esse valor e somente esse valor.
    """

    def __init__(self, value):
        """
        Construtor padrão de um nó numérico.

        Argumentos:

        value -- Valor numérico da variável
        """
        self.value = value

    def solve(self):
        """Retornado o objeto para tratamentos de igualdade (isinstance)."""
        return self

    def __str__(self):
        """Tal número ``resulta'' em seu próprio valor."""
        return self.value


class Str(Node):
    """Representa uma string da linguagem."""

    def __init__(self, value):
        """
        Construtor padrão de um nó de string.

        Argumentos:

        value -- Valor da string da variável, pode ter qualquer tamanho que
        o Python possa aceitar.
        """
        self.value = value

    def solve(self):
        """Retornado instância para tratamentos em métodos de igualdade."""
        return self

    def __str__(self):
        """Toda String ``resulta'' em si mesma."""
        return self.value


class Bool(Node):
    """Nó o qual representa um booleano da linguagem."""

    def __init__(self, value):
        """
        Construtor padrão de um nó de um booleano.

        Argumentos:

        value -- tru (true/t) ou fls (false/nil)
        """
        self.value = value

    def solve(self):
        """Retornada instância para tratamentos de igualdade (isinstance)."""
        return self

    def __str__(self):
        """Valor a ser retornado depende do valor resultante."""
        if self.value == "tru":
            return "True"
        elif self.value == "fls":
            return "False"


class Emp(Node):
    """Vazio/nil da linguagem, o token assume o mesmo nome que o nó."""

    def __init__(self, value):
        """
        Construtor padrão de um nó de um booleano.

        Argumentos:

        value -- emp
        """
        self.value = value

    def solve(self):
        """Emp resulta na instância de si mesmo."""
        return self.value

    def __str__(self):
        """Emp = None na linguagem Python."""
        return "None"
# Type
# durante a declaração de variável nesta linguagem fracamente tipada,
# uma variável pode assumir o tipo Str, num ou tof


class Type(Node):
    """Tipo da variável a ser declarada."""

    def __init__(self, value):
        """
        Construtor padrão de um nó de um tipo.

        Argumentos:

        value -- literalmente as palavras num, str ou tof
        """
        self.value = value

    def solve(self):
        """Instância é retornada para checagens de equalidade."""
        return self

    def __str__(self):
        """Tipo de um identificador é o próprio tipo."""
        return self.value

# Var
# Ou também identificador/identifier, recebe uma string de três letras
# para identificar uma variável.


class Var(Node):
    """Identificador para a variável, podendo receber três letras."""

    def __init__(self, value):
        """
        Construtor padrão de um nó de um identificador de variável.

        Argumentos:

        value -- string de 3 letras que nomeia uma variável a ser declarada
        """
        self.value = value

    def solve(self):
        """Deve ser checado se o identificador fora declarado anteriormente."""
        var_in_table = var_table.lookup(self.value)
        if not var_in_table:
            erro(f"Erro semântico: variável {self.value} usada mas não declarada")
        else:
            dic_temp = {"num": Num(0), "str": Str(""), "tof": Bool("tru")}
            return dic_temp[var_in_table["type"]]

    def __str__(self):
        """Valor de um identificador é o próprio identificador."""
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
        Construtor padrão de um nó que representa a parada ou não de um laço.

        Argumentos:

        value -- pode assumir os valores brk ou jmp
        """
        self.value = value
        self.inside_loop = False
        self.scope = 0

    def solve(self):
        """Checado se break ou continue não foram utilizados fora de loops."""
        if not self.inside_loop and self.value != "emp":
            erro(f"Erro semântico: uso de {self.value} fora de uma estrutura de repetição")

    def __str__(self):
        """Quebra (ou continuação) genérica de laços."""
        tab = "\t"*self.scope

        if self.value == "brk":
            return f"{tab}break"
        elif self.value == "jmp":
            return f"{tab}continue"
        elif self.value == "emp":
            return f"{tab}pass"


class Decvar(Node):
    """Declaração de variáveis da linguagem, também serve de reatribuição."""

    def __init__(self, var_type, var, literal):
        """
        Construtor padrão de um nó o qual representa a declaração.

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
        """
        Decvar é totalmente dependente da corretude dos tipos definidos.

        Todas as checagens por erros e inconsistências semânticas devem
        ocorrer de forma que um número seja declarado como número e redifinido
        como número, por exemplo.
        """
        var_in_table = var_table.lookup(self.var.value)

        if var_in_table and var_in_table["type"] != self.var_type.value:
            erro(f"Erro semântico: {self.var} declarado anteriormente com tipo {var_in_table['type']} ao invés de {self.var_type}")

        literal_temp = self.literal
        if isinstance(self.literal, (BinOp, Var)):
            literal_temp = self.literal.solve()

        if self.var_type.value == "num" and not isinstance(literal_temp, (Num, Emp)):
            erro(f"Erro semântico: {self.literal} não pode ser declarado como num")
        elif self.var_type.value == "str" and not isinstance(literal_temp, (Str, Emp)):
            erro(f"Erro semântico: {self.literal} não pode ser declarado como str")
        elif self.var_type.value == "tof" and not isinstance(literal_temp, (Bool, Emp)):
            erro(f"Erro semântico: {self.literal} não pode ser declarado como tof")

        var_table.insert(self.var.value, self.var_type.value, self.scope)

    def __str__(self):
        """
        Por ser fracamente tipado, ``perde-se'' a tipagem tratada no simple3.

        Decvar apresenta a estrutura: tipo identificador = valor;
        """
        tabs = "\t" * self.scope
        return f"{tabs}{self.var} = {self.literal}"


class Whl(Node):
    """
    Nó o qual representa uma estrutura de repetição whl (while/do).

    Seu nó filho pode conter todas as estruturas do programa (S).
    """

    def __init__(self, expr, s):
        """
        Estrutura de loop mais simples da linguagem.

        Argumentos:

        expr -- expressão teste que induza a execução do laço
        s -- não terminal inicial representando todas as partes da linguagem
        """
        self.expr = expr
        self.s = s
        self.tab = ""
        self.scope = 0

    def solve(self):
        """É testada se expr é válida."""
        r = self.expr.solve()
        if isinstance(r, Str):
            erro("Erro semântico: Expressão de whl não pode ser str")
        for line in self.s:
            if isinstance(line, (Control, Ifi)):
                line.inside_loop = True
            line.scope = self.scope + 1
            line.solve()

        var_table.remove_by_scope(self.scope+1)

    def __str__(self):
        """Whl será traduzido como: TAB*while expr:NEWLINE S."""
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
        """
        Construtor único do laço de repetição controlado.

        Argumentos:

        typo - tipo opcional da variável
        var  - identificador da variável
        rang - range x:y o qual define um range de x até y-1
        """
        self.typo = typo
        self.var = var
        self.rang = rang
        self.s = s
        self.tab = ""
        self.scope = 0

    def solve(self):
        """Realizados todos os mesmos tratamentos semânticos de S."""
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
            if isinstance(line, (Control, Ifi)):
                line.inside_loop = True
            line.scope = self.scope + 1
            line.solve()

        var_table.remove_by_scope(self.scope+1)

    def __str__(self):
        """
        Gerado for do python dependente da função ``range()''.

        Assume a forma: for var in range(lower_bound, higher_bound)
        """
        result = ""
        eol = "\n"

        self.tab = "\t" * self.scope

        for line in self.s:
            if line == self.s[-1]:
                eol = ""
            result += f"{line}{eol}"
        return f"{self.tab}for {self.var} in {self.rang}:\n{result}"


class Ifi(Node):
    """
    Nó representante da estrutura condicional ``ifi''.

    Tem formato ifi (expr) {S}, se ``expr'' for verdadeira,
    todas as expressões contidas em S são executadas
    """

    def __init__(self, expr, s, els):
        """
        Construtor padrão do nó Ifi.

        Argumentos:

        expr - teste o qual define se THEN ou ELSE será executado
        s    - pode expandir para qualquer outro elemento da linguagem
        els  - els é opcional e será executado caso expr resulte em falso
        """
        self.expr = expr
        self.s = s
        self.els = els
        self.tab = ""
        self.scope = 0
        self.inside_loop = False

    def solve(self):
        """
        É verificado se é necessário chamar recursivamente as expressões em S.

        Criado um erro caso o contrário.
        """
        self.expr.solve()

        for line in self.s:
            if isinstance(line, (Control, Ifi)):
                line.inside_loop = self.inside_loop
            line.scope = self.scope + 1
            line.solve()

        var_table.remove_by_scope(self.scope+1)

        if self.els:
            self.els.inside_loop = self.inside_loop
            self.els.scope = self.scope
            self.els.solve()

    def __str__(self):
        """
        Geração do código da estrutura condicional ifi.

        Gerado como ifi (expr) {S}. Podendo gerar um condicional ALTERNATIVO
        ELS caso necessário
        """
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
    """ELSE branch genérico, podendo conter todos os elementos da linguagem."""

    def __init__(self, s):
        """S - toda a linguagem."""
        self.s = s
        self.tab = ""
        self.scope = 0
        self.inside_loop = False

    def solve(self):
        """Checagem por mais estruturas de controle ou laço ocorrem aqui."""
        for line in self.s:
            if isinstance(line, (Control, Ifi)):
                line.inside_loop = self.inside_loop
            line.scope = self.scope + 1
            line.solve()
        var_table.remove_by_scope(self.scope+1)

    def __str__(self):
        """Produção do código do els, a indentação é gerada automaticamente."""
        result = ""
        eol = "\n"

        self.tab = "\t" * self.scope

        for line in self.s:
            if line == self.s[-1]:
                eol = ""
            result += f"{line}{eol}"
        return f"{self.tab}else:\n{result}"
