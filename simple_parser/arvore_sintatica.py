class AST:
    pass


class BinOp(AST):
    '''
    Essa classe representa uma operação binária na linguagem e herda de AST;

    Uma operação binária pode ser do tipo
    "+", "-", "*", "/", ":", "and", "orr", ">=", "<=", "==", "<", ">".
    '''

    def __init__(self, left, token, right):
        '''
        Construtor padrão da classe.

        Argumentos:

        left  -- nó esquerdo da opearção
        right -- nó direito da operação
        token -- token o qual contém o operador
        '''
        self.left = left
        self.right = right
        self.token = token
        self.operator = token[0]  # operador


class UnOP(AST):
    '''
    Essa classe cria um nó da árvore representando uma operação unária.

    Uma operação unária pode ser do tipo
    "!" (negação).
    '''

    def __init__(self, token, operand):
        '''
        Toda operação unária apresenta um único nó filho:

        Argumentos:

        token -- token representando a operação (! apenas até o momento)
        operand -- operando da operação

        '''
        self.token = token
        self.operator = token[0]
        self.operand = operand


class Num(AST):
    pass


class Str(AST):
    pass


class Bool(AST):
    pass
