import sys
from . import arvore_sintatica as sinTree


class Parser():
    def __init__(self, token_list):
        self.token_list = token_list
        self.index = 0
        self.current_token = self.token_list[self.index]
        self.code_line = 1
        self.init()

    def error(self, message=False):
        raise Exception(message if message else "deu merda")  # arrumar depois

    def eat(self):
        """
            Avança para o próximo token
        """
        self.index += 1
        self.current_token = self.token_list[self.index]

    def vomit(self):
        """
            Retrocede para o token anterior
        """
        if self.index == 0:
            pass
        else:
            self.index += 1
            self.current_token = self.token_list[self.index]

    def rollback_to(self, time):
        """
            Seta o token para um index especificado
        """
        self.index = time
        self.current_token = self.token_list[self.index]

    # Isso aqui é o S dos não terminais
    def init(self):
        func_list = [self.decvar, self.matlab, self.flux, self.rpt]

        for i in enumerate(func_list):
            a = i[1]()
            if a is not None:
                print(a)
                return a

        return None

    def decvar(self):
        pace = 0

        while pace < 5:
            if self.current_token[0] == "type" and pace == 0:
                self.eat("type")
                pace += 1
            elif self.current_token[0] != "type" and pace == 0:
                pace += 1
            elif self.current_token[0] == "var" and pace == 1:
                if self.transpilar:
                    self.code += self.current_token[1] + " "
                self.eat("var")
                pace += 1
            elif self.current_token[0] == "operator" and pace == 2:
                if self.transpilar:
                    self.code += self.current_token[1] + " "
                self.eat("operator")
                pace += 1
            elif pace == 3:
                self.literal()
                pace += 1
            elif self.current_token[0] == "eos" and pace == 4:
                self.eat("eos")
                pace += 1
            else:
                self.error("erro do decvar")

    def literal(self):
        # str | MATLAB | BOOL
        if self.current_token[0] == "str":
            a = sinTree.Str(self.current_token[1])
            self.eat()
            return a
        if self.current_token[0] == "num":
            a = sinTree.Str(self.current_token[1])
            self.eat()
            return a

        # a = self.matlab()
        # if a is not None:
        #     return a

        a = self.bool_ean()
        if a is not None:
            return a

        return None

    def bool_ean(self):
        # BOOL = tru | fls
        if self.current_token[0] in ("tru", "fls"):
            a = sinTree.Bool(self.current_token[1])
            self.eat()
            return a
        else:
            return None

    def matlab(self, consume_eos=True):
        # MATLAB   ->  MATLAB' (+ | -) MATLAB' [eos] | MATLAB'
        # MATLAB'  ->  MATLAB'' (* | / | ^) MATLAB'' [eos] | MATLAB''
        # MATLAB'' ->  num | var | '(' MATLAB ')'
        node = self.matlab1(consume_eos)

        while self.current_token[1] in ('+', '-'):
            token = self.current_token
            if self.transpilar:
                self.code += self.current_token[1] + " "
            self.eat(token[0])
            if consume_eos and token == "eos":
                self.eat("eos")
            node = node + token[1] + self.matlab1(consume_eos)

        return node

    def matlab1(self, consume_eos=True):
        node = self.matlab2(consume_eos)

        while self.current_token[1] in ('*', '/', '^'):
            token = self.current_token
            if self.transpilar:
                self.code += self.current_token[1] + " "
            self.eat(token[0])
            node = node + token[1] + self.matlab2(consume_eos)

        return node

    def matlab2(self, consume_eos=True):
        token = self.current_token

        if token[0] == "num":
            if self.transpilar:
                self.code += self.current_token[1] + " "
            self.eat("num")
            return str(token[1])
        elif token[0] == "var":
            if self.transpilar:
                self.code += self.current_token[1] + " "
            self.eat("var")
            return str(token[1])
        elif token[0] == "(":
            if self.transpilar:
                self.code += self.current_token[1] + " "
            self.eat("(")
            node = self.matlab(consume_eos)
            if self.transpilar:
                self.code += self.current_token[1] + " "
            self.eat(")")
            return '(' + node + ')'
        else:
            self.error("erro no matlab")

    def operador(self):
        # OPERADOR = + | - | / | * | ^
        self.eat_generic("operador")

    def flux(self):
        self.erro("erro no flux")
        pass

    def expr(self):
        # EXPR' OPBOOL EXPR' [(and|orr) EXPR] | EXPR'
        # LITERAL | (EXPR)

        # EXPR'
        expr1 = self.__expr_2()
        if expr1 is None:
            return None

        checkpoint = self.index

        # OPBOOL
        op = self.opbool()
        if op is None:
            return expr1

        # EXPR'
        expr2 = self.__expr_2()
        if expr2 is None:
            self.rollback_to(checkpoint)
            return expr1
        else:
            op.left = expr1
            op.right = expr2

        checkpoint = self.index

        # (and|orr)
        if self.current_token and self.current_token[1] in ("and", "orr"):
            op2 = sinTree.BinOp(None, self.current_token[1], None)
            self.eat()
        else:
            return op

        # EXPR
        expr3 = self.expr()
        if expr3 is None:
            self.rollback_to(checkpoint)
            return op
        else:
            op2.left = op
            op2.right = expr3
            return op2

    def __expr_2(self):
        # LITERAL | (EXPR)

        # LITERAL
        a = self.literal()
        if a is None:
            pass
        else:
            return a

        # (EXPR)
        if self.current_token[0] == "(":
            checkpoint = self.index
            self.eat()
            a = self.expr()
            if a is None:
                self.vomit(1)
                return None
            elif self.current_token[0] == ")":
                self.eat()
                return a
            else:
                self.rollback_to(checkpoint)

        return None

    def opbool(self):
        tokens_aceitos = ("==", ">", ">=", "<", "<=")
        if self.current_token[1] in tokens_aceitos:
            a = sinTree.BinOp(None, self.current_token[1], None)
            self.eat()
            return a
        else:
            return None

    def rpt(self):
        self.erro("erro no rpt")
        pass

    def ranger(self):
        pass

    def eat_generic(self, dic_string):
        '''
        Consome um token baseado na entrada presente no dicionário de tokens
        por nível.
        '''
        for token_value in self.tokens_aceitos[dic_string]:
            if token_value == self.current_token[1]:
                self.eat(token_value)
