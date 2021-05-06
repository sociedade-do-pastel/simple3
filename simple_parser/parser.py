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

    def check_eol(self):
        if self.current_token is None:
            # TODO se for montar árvore, aqui que tá o \n
            if self.transpilar and self.code[-1] != '\n':
                self.code += "\n"
            self.current_token = self.next_token
            self.code_line += 1
            try:
                self.next_token = self.lexer.get_next_token()
            except Exception:
                self.next_token = None

    # Isso aqui é o S dos não terminais
    def init(self):
        d = ["EXPR", "DECVAR", "MATLAB", "FLUX", "RPT"]
        func_list = [self.expr, self.decvar, self.matlab, self.flux, self.rpt]
        chave = 0

        while True:
            try:
                func_list[chave]()
                print(f'{d[chave]} validado!')
                self.check_eol()
                chave = 0
            except IndexError:
                if self.current_token is not None and self.next_token is not None:
                    self.error(
                        f"Erro na linha {self.code_line}: cadeia não reconhecida pela linguagem.")

                if self.transpilar:
                    print("\n\nOLHA O CÓDIGO EM PYTHON AI:")
                    print(self.code, end="")
                sys.exit()
            except Exception as e:
                if "interrupt" in e.args:
                    self.error(
                        f"Erro na linha {self.code_line}: cadeia não reconhecida pela linguagem.")
                    sys.exit()
                chave += 1

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
            return sinTree.Str(self.current_token[1])

        a = self.matlab()
        if a is not None:
            return a

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
        # EXPR' OPBOOL EXPR' [(and|orr) EXPR'] | EXPR'
        # LITERAL | (EXPR)

        # EXPR'
        if not self.__expr_2():
            return False

        if not self.current_token:
            return True

        # checkpoint
        pos_temp = self.current_token_pos

        # OPBOOL EXPR'
        if not self.opbool():
            return True
        if not self.__expr_2():
            self.rewind_to(pos_temp)
            return True

        if not self.current_token:
            return True

        # checkpoint
        pos_temp = self.current_token_pos

        # [(and|orr) EXPR']
        if self.current_token[0] in ("and", "orr"):
            self.eat()
        else:
            return True
        if not self.__expr_2():
            self.rewind_to(pos_temp)
            return True

    def __expr_2(self):
        # LITERAL | (EXPR)

        # LITERAL
        if self.literal():
            return True

        # (EXPRR)
        if self.current_token[0] == "(":
            pos_temp = self.current_token_pos
            self.eat()
            if not self.expr():
                return self.vomit(1)
            if self.current_token[0] == ")":
                self.eat()
                return True
            else:
                self.rewind_to(pos_temp)
                return False

        return False

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
