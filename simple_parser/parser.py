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
            self.current_token += 1
            self.code_line += 1

    # Isso aqui é o S dos não terminais
    def init(self):
        d = ["DECVAR", "MATLAB", "FLUX", "RPT"]
        func_list = [self.decvar, self.matlab, self.flux, self.rpt]
        chave = 0

        while True:
            try:
                func_list[chave]()
                print(f'{d[chave]} validado!')
                self.check_eol()
                chave = 0
            except IndexError:
                if self.current_token is not None and self.token_list[self.index+1] is not None:
                    self.error(
                        f"Erro na linha {self.code_line}: cadeia não reconhecida pela linguagem.")
                sys.exit()
            except Exception as e:
                if "interrupt" in e.args:
                    self.error(
                        f"Erro na linha {self.code_line}: cadeia não reconhecida pela linguagem.")
                    sys.exit()
                chave += 1

    def decvar(self):
        pace = 0
        index_backup = self.index
        node_list = []

        while pace < 5:
            if self.current_token[0] == "type" and pace == 0:
                node_list.append(self.current_token[1])
                self.eat()
                pace += 1
            elif self.current_token[0] == "var" and pace == 1:
                node_list.append(self.current_token[1])
                self.eat()
                pace += 1
            elif self.current_token[0] == "operator" and pace == 2:
                self.eat()
                pace += 1
            elif pace == 3:
                node = self.literal()
                node_list.append(node)
                pace += 1
            elif self.current_token[0] == "eos" and pace == 4:
                self.eat()
                pace += 1
            else:
                self.rollback_to(index_backup)
                self.error("erro do decvar")
        
        if len(node_list) < 3:
            self.rollback_to(index_backup)
            self.error("erro no decvar")
        
        for node in node_list:
            if node is None:
                self.rollback_to(index_backup)
                self.error("erro no decvar")

        return sinTree.Decvar(sinTree.Type(node_list[0]), sinTree.Var(node_list[1]), node_list[2])            
                

    def literal(self):
        # str | MATLAB | BOOL
        if self.current_token[0] == "str":
            tree_node = sinTree.Str(self.current_token[1])
            self.eat()
            return tree_node

        a = self.matlab(consume_eos=False)
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
            self.eat()
            if consume_eos and token == "eos":
                self.eat()
            node = sinTree.BinOp(node, token[1], self.matlab1(consume_eos))

        # edge cases
        if isinstance(node, sinTree.Var):
            self.error("erro no matlab")

        return node

    def matlab1(self, consume_eos=True):
        node = self.matlab2(consume_eos)

        while self.current_token[1] in ('*', '/', '^'):
            token = self.current_token
            self.eat()
            node = sinTree.BinOp(node, token[1], self.matlab2(consume_eos))

        return node

    def matlab2(self, consume_eos=True):
        token = self.current_token

        if token[0] == "num":
            self.eat()
            return sinTree.Str(token[1])
        elif token[0] == "var":
            self.eat()
            return sinTree.Var(token[1])
        elif token[0] == "(":
            self.eat()
            node = self.matlab(consume_eos)
            self.eat()
            return node

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
