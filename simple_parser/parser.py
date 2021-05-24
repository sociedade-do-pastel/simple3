import sys
from . import arvore_sintatica as sinTree


class Parser():
    def __init__(self, token_list):
        self.token_list = token_list
        self.index = 0
        self.current_token = self.token_list[self.index]
        self.code_line = 1
        self.do_loop = True
        self.treeList = []
        self.bootstrap()
        self.solveIter()

    def error(self, message=False):
        raise Exception(message if message else "deu merda")  # arrumar depois

    def eat(self):
        """
            Avança para o próximo token
        """
        self.index += 1
        if self.index >= len(self.token_list):
            self.do_loop = False
        else:
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
        """
            Checa se o token atual é None (identificador)
            de fim de linha e, caso positivo, avança para
            o próximo token
        """
        if self.current_token is None:
            self.eat()

    def bootstrap(self):
        """
            Faz a inicialização do parsing
        """
        while self.do_loop:
            try:
                self.treeList.append(self.init())
            except Exception as e:
                print(e)
                return

    def solveIter(self):
        """
            Chama iterativamente as funções solve
        """
        try:
            for i in self.treeList:
                i.solve()
        except Exception as e:
            print(e)

    # Isso aqui é o S dos não terminais
    def init(self):
        func_list = [self.decvar, self.matlab, self.flux, self.rpt,
                     self.control]

        for i in enumerate(func_list):
            a = i[1]()
            if a is not None:
                return a

        self.error(f"Erro no parser: sentença não reconhecida com {self.current_token[1]}")

    def decvar(self):
        pace = 0
        index_backup = self.index
        node_list = []
        is_decvar = False

        while pace < 5:
            if self.current_token[0] == "type" and pace == 0:
                node_list.append(self.current_token[1])
                self.eat()
                pace += 1
                is_decvar = True
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
            elif is_decvar:
                self.error("Erro no parser: decvar incompleto")
            else:
                return None

        if len(node_list) < 3:
            self.rollback_to(index_backup)
            self.error("erro no decvar")

        for node in node_list:
            if node is None:
                self.rollback_to(index_backup)
                self.error("erro no decvar")

        return sinTree.Decvar(sinTree.Type(node_list[0]),
                              sinTree.Var(node_list[1]),
                              node_list[2])

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
        # MATLAB   ->  MATLAB' (+ | -) MATLAB' [eos] | MATLAB' [eos]
        # MATLAB'  ->  MATLAB'' (* | / | ^) MATLAB'' [eos] | MATLAB''
        # MATLAB'' ->  num | var | '(' MATLAB ')'
        node1 = self.matlab1(consume_eos)

        if not node1:
            return None

        if self.current_token and self.current_token[1] in ('+', '-'):
            token = self.current_token
            self.eat()
        elif consume_eos and self.current_token and self.current_token[0] == "eos":
            self.eat()
            return node1
        else:
            return node1

        node2 = self.matlab1(consume_eos)
        if not node2:
            self.error("Erro no parser: operação matlab incompleta")

        if consume_eos and self.current_token and self.current_token[0] == "eos":
            self.eat()

        return sinTree.BinOp(node1, token[1], node2)

    def matlab1(self, consume_eos=True):
        """MATLAB'  ->  MATLAB'' (* | / | ^) MATLAB'' [eos] | MATLAB''."""
        node1 = self.matlab2(consume_eos)

        if not node1:
            return None

        if self.current_token[1] in ('*', '/', '^'):
            token = self.current_token
            self.eat()
        else:
            return node1

        node2 = self.matlab2(consume_eos)

        if not node2:
            self.error("Erro no parser: operação matlab incompleta")

        if consume_eos and self.current_token and self.current_token[0] == "eos":
            self.eat()

        return sinTree.BinOp(node1, token[1], node2)

    def matlab2(self, consume_eos=True):
        """MATLAB'' ->  num | var | '(' MATLAB ')'."""
        token = self.current_token

        if token[0] == "num":
            self.eat()
            return sinTree.Num(token[1])
        elif token[0] == "var":
            self.eat()
            return sinTree.Var(token[1])
        elif token[0] == "(":
            self.eat()
            node = self.matlab(consume_eos)
            if self.current_token[0] == ')':
                self.eat()
                return node
            else:
                self.error("Erro no parser: faltando )")

    def flux(self):
        # ifi (EXPR) scope_init S scope_end
        ifi = self.flux_ifi()
        if ifi is None:
            return None

        if not self.do_loop:
            return ifi

        els = self.flux_els()
        if els is None:
            return ifi
        else:
            ifi.els = els
            return ifi

    def flux_ifi(self):
        # ifi (EXPR) scope_init S scope_end
        checkpoint = self.index
        is_ifi = False

        sequence = ("ifi", "(", "EXPR", ")", "scope_init", "S", "scope_end")
        for i in enumerate(sequence):
            if not self.do_loop:
                break
            if i[0] == 0 and self.current_token[0] == i[1]:
                self.eat()
                is_ifi = True
            elif i[0] == 2:
                expr = self.expr()
                if expr is None:
                    break
            elif i[0] == 5:
                s = []
                while self.do_loop and self.current_token[0] != "scope_end":
                    s.append(self.init())
                if len(s) == 0:
                    break
            elif self.current_token[0] == i[1]:
                self.eat()
            else:
                break
        else:
            return sinTree.Ifi(expr, s, None)

        if is_ifi:
            self.error("Erro no parser: ifi incompleto")
        else:
            self.rollback_to(checkpoint)
            return None

    def flux_els(self):
        # els scope_init S scope_end
        checkpoint = self.index
        is_els = False

        sequence = ("els", "scope_init", "S", "scope_end")
        for i in enumerate(sequence):
            if not self.do_loop:
                break
            if i[0] == 0:
                self.eat()
                is_els = True
            elif i[0] == 2:
                s = []
                while self.do_loop and self.current_token[0] != "scope_end":
                    s.append(self.init())
                if len(s) == 0:
                    break
            elif self.current_token[0] == i[1]:
                self.eat()
            else:
                break
        else:
            return sinTree.Els(s)

        if is_els:
            self.error("Erro no parser: els incompleto")
        else:
            self.rollback_to(checkpoint)
            return None

    def expr(self):
        # EXPR' OPBOOL EXPR' [(and|orr) EXPR] | EXPR'
        # LITERAL | (EXPR)

        # EXPR'
        expr1 = self.expr2()
        if expr1 is None:
            return None

        checkpoint = self.index

        # OPBOOL
        op = self.opbool()
        if op is None:
            return expr1

        # EXPR'
        expr2 = self.expr2()
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

    def expr2(self):
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
        # whl (EXPR) scope_init S scope_end
        # for [type] var '=' RANGE scope_init S scope_end

        # whl (EXPR) scope_init S scope_end
        a = self.rpt_whl()
        if a is not None:
            return a

        # for [type] var '=' RANGE scope_init S scope_end
        a = self.rpt_for()
        if a is not None:
            return a
        return None

    def rpt_whl(self):
        # whl (EXPR) scope_init S scope_end
        checkpoint = self.index
        is_whl = False

        sequence = ("whl", "(", "EXPR", ")", "scope_init", "S", "scope_end")
        for i in enumerate(sequence):
            if not self.do_loop:
                break
            if i[0] == 0 and self.current_token[0] == i[1]:
                self.eat()
                is_whl = True
            elif i[0] == 2:
                expr = self.expr()
                if expr is None:
                    break
            elif i[0] == 5:
                s = []
                while self.do_loop and self.current_token[0] != "scope_end":
                    s.append(self.init())
                if len(s) == 0:
                    break
            elif self.current_token[0] == i[1]:
                self.eat()
            else:
                break
        else:
            return sinTree.Whl(expr, s)

        if is_whl:
            self.error("Erro no parser: whl incompleto")
        else:
            self.rollback_to(checkpoint)
            return None

    def rpt_for(self):
        # for [type] var '=' RANGE scope_init S scope_end
        checkpoint = self.index
        is_for = False

        sequence = ("for", "type", "var", "=", "RANGE", "scope_init", "S",
                    "scope_end")
        for i in enumerate(sequence):
            if not self.do_loop:
                break
            if i[0] == 0 and self.current_token[0] == i[1]:
                self.eat()
                is_for = True
            elif i[0] == 1:
                if self.current_token[0] == "type":
                    typo = self.current_token[1]
                    self.eat()
                else:
                    typo = None
            elif i[0] == 2:
                if self.current_token[0] == "var":
                    var = sinTree.Var(self.current_token[1])
                    self.eat()
                else:
                    break
            elif i[0] == 3:
                if self.current_token[1] == "=":
                    self.eat()
            elif i[0] == 4:
                rang = self.ranger()
                if not rang:
                    break
            elif i[0] == 6:
                s = []
                while self.do_loop and self.current_token[0] != "scope_end":
                    s.append(self.init())
                if len(s) == 0:
                    break
            elif self.current_token[0] == i[1]:
                self.eat()
            else:
                break
        else:
            return sinTree.For(typo, var, rang, s)

        if is_for:
            self.error("Erro no parser: for incompleto")
        else:
            self.rollback_to(checkpoint)
            return None

    def ranger(self):
        # num : num

        # num
        if self.current_token[0] == "num":
            num1 = sinTree.Num(self.current_token[1])
            self.eat()
        else:
            return None

        # :
        if self.current_token[1] == ":":
            self.eat()
        else:
            self.vomit()
            return None

        # num
        if self.current_token[0] == "num":
            num2 = sinTree.Num(self.current_token[1])
            self.eat()
            return sinTree.BinOp(num1, ":", num2)
        else:
            self.vomit()
            self.vomit()
            return None

    def control(self):
        # brk | jmp
        if self.current_token[0] == "brk":
            token = "brk"
            self.eat()
        elif self.current_token[0] == "jmp":
            token = "jmp"
            self.eat()
        else:
            return None

        # ;
        if self.current_token[0] == "eos":
            self.eat()
            return sinTree.Control(token)
        else:
            self.vomit()
            return None
