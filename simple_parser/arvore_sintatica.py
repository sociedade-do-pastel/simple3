from ABC import abc, abstractmethod


class Node(abc):
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
    "+", "-", "*", "/", ":", "and", "orr", ">=", "<=", "==", "<", ">".
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
        return f"{self.left} {self.operator} {self.right}"


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


class Num(Node):
    def __init__(self, value):
        self.value = value

    def solve(self):
        pass

    def __str__(self):
        return self.value


class Str(Node):
    def __init__(self, value):
        self.value = value

    def solve(self):
        pass

    def __str__(self):
        return self.value


class Bool(Node):
    def __init__(self, value):
        self.value = value

    def solve(self):
        pass

    def __str__(self):
        return self.value
