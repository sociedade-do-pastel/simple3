from . import arvore_sintatica as sinTree


class Parser():
    """
    Classe responsável por todo o parser da linguagem.

    Implementado utilizando GLCs.
    """

    def __init__(self, token_list):
        """
        Construtor padrão da classe.

        token_list = lista de tokens recebida pelo lexer
        """
        self.token_list = token_list
        self.index = 0

        if len(self.token_list) > 0:
            self.current_token = self.token_list[self.index]
            self.do_loop = True
        else:
            self.current_token = None
            self.do_loop = False

        self.treeList = []

    def error(self, message=False):
        """
        Invoca uma exceção.

        Caso não receba parâmetro, imprime um erro genérico.
        """
        raise Exception(message if message else "deu merda")  # arrumar depois

    def eat(self):
        """Avança para o próximo token."""
        self.index += 1
        if self.index >= len(self.token_list):
            self.do_loop = False
        else:
            self.current_token = self.token_list[self.index]

    def vomit(self):
        """Retrocede para o token anterior."""
        if self.index == 0:
            pass
        else:
            self.index += 1
            self.current_token = self.token_list[self.index]

    def rollback_to(self, time):
        """Seta o token para um index especificado."""
        self.index = time
        self.current_token = self.token_list[self.index]

    def parse(self):
        """Faz a inicialização do parsing."""
        while self.do_loop:
            self.treeList.append(self.s())

    def solve(self):
        """Chama iterativamente as funções solve."""
        for i in self.treeList:
            i.solve()

    def s(self):
        """
        Representa os não terminais possíveis em uma linha.

        Itera entre todas as possibilidades e devolve o encontrado.
        """
        func_list = [self.decvar, self.matlab, self.flux, self.rpt,
                     self.control]

        for i in enumerate(func_list):
            a = i[1]()
            if a is not None:
                return a

        self.error(f"Erro no parser: sentença não reconhecida com {self.current_token[1]}")

    def decvar(self):
        """
        Implementa a seguinte GLC.

        type var '=' LITERAL eos
        """
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
            elif self.current_token[1] == "=" and pace == 2:
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
        """
        Implementa a seguinte GLC.

        str | MATLAB | BOOL | emp
        """
        if self.current_token[0] == "str":
            tree_node = sinTree.Str(self.current_token[1])
            self.eat()
            return tree_node

        if self.current_token[0] == "emp":
            tree_node = sinTree.Emp(self.current_token[1])
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
        """
        Implementa a seguinte GLC.

        tru | fls
        """
        if self.current_token[0] in ("tru", "fls"):
            a = sinTree.Bool(self.current_token[1])
            self.eat()
            return a
        else:
            return None

    def matlab(self, consume_eos=True):
        """
        Implementa a seguinte GLC.

        MATLAB' (+ | -) MATLAB [eos] | MATLAB' [eos]

        O parâmetro consume_eos serve como uma análise semântica imbutida.
        """
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

        node2 = self.matlab(consume_eos)
        if not node2:
            self.error("Erro no parser: operação matlab incompleta")

        if consume_eos and self.current_token and self.current_token[0] == "eos":
            self.eat()

        return sinTree.BinOp(node1, token[1], node2)

    def matlab1(self, consume_eos=True):
        """
        Implementa a seguinte GLC.

        MATLAB'' (* | / | ^) MATLAB'' [eos] | MATLAB''.

        O parâmetro consume_eos serve como uma análise semântica imbutida.
        É referido como MATLAB'
        """
        node1 = self.matlab2(consume_eos)

        if not node1:
            return None

        if self.current_token[1] in ('*', '/', '^'):
            token = self.current_token
            self.eat()
        else:
            return node1

        node2 = self.matlab1(consume_eos)

        if not node2:
            node2 = self.matlab(consume_eos)
            if not node2:
                self.error("Erro no parser: operação matlab incompleta")

        if consume_eos and self.current_token and self.current_token[0] == "eos":
            self.eat()

        return sinTree.BinOp(node1, token[1], node2)

    def matlab2(self, consume_eos=True):
        """
        Implementa a seguinte GLC.

        num | var | '(' MATLAB ')'.

        O parâmetro consume_eos serve como uma análise semântica imbutida.
        É referido como MATLAB''
        """
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
        """
        Implementa as seguintes GLC.

        IFI = ifi (EXPR) scope_init S scope_end
        ELS = els scope_init S scope_end
        """
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
        """
        Implementa a seguinte GLC.

        ifi (EXPR) scope_init S scope_end
        """
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
                    s.append(self.s())
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
        """
        Implementa a seguinte GLC.

        els scope_init S scope_end
        """
        checkpoint = self.index
        is_els = False

        sequence = ("els", "scope_init", "S", "scope_end")
        for i in enumerate(sequence):
            if not self.do_loop:
                break
            if i[0] == 0 and self.current_token[0] == "els":
                self.eat()
                is_els = True
            elif i[0] == 2:
                s = []
                while self.do_loop and self.current_token[0] != "scope_end":
                    s.append(self.s())
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
        """
        Implementa a seguinte GLC.

        EXPR' OPBOOL EXPR' [(and|orr) EXPR] | EXPR'
        """
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
        """
        Implementa a seguinte GLC.

        LITERAL | (EXPR) | ! EXPR
        É referido como EXPR'
        """
        # LITERAL
        a = self.literal()
        if a is not None:
            return a

        # (EXPR)
        if self.current_token[0] == "(":
            checkpoint = self.index
            self.eat()
            a = self.expr()
            if a is None:
                self.vomit()
                return None
            elif self.current_token[0] == ")":
                self.eat()
                return a
            else:
                self.rollback_to(checkpoint)

        # ! EXPR
        if self.current_token[1] == "!":
            checkpoint = self.index
            self.eat()
            if self.current_token[0] == "(":
                self.eat()
            else:
                self.error(
                    "Erro no parser: operação ! não seguido de parênteses"
                )
            a = self.expr()
            if a is None:
                self.rollback_to(checkpoint)
            else:
                if self.current_token[0] == ")":
                    self.eat()
                    return sinTree.UnOP("!", a)

        return None

    def opbool(self):
        """
        Implementa a seguinte GLC.

        == | > | >= | < | <=
        """
        tokens_aceitos = ("==", "!=", ">", ">=", "<", "<=")
        if self.current_token[1] in tokens_aceitos:
            a = sinTree.BinOp(None, self.current_token[1], None)
            self.eat()
            return a
        else:
            return None

    def rpt(self):
        """
        Implementa as seguintes GLCs.

        WHL = whl (EXPR) scope_init S scope_end
        FOR = for [type] var '=' RANGE scope_init S scope_end
        """
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
        """
        Implementa a seguinte GLC.

        whl (EXPR) scope_init S scope_end
        """
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
                    s.append(self.s())
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
        """
        Implementa a seguinte GLC.

        for [type] var '=' RANGE scope_init S scope_end
        """
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
                    s.append(self.s())
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
        """
        Implementa a seguinte GLC.

        num : num
        """
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
        """
        Implementa a seguinte GLC.

        brk | jmp | emp
        """
        if self.current_token[0] == "brk":
            token = "brk"
            self.eat()
        elif self.current_token[0] == "jmp":
            token = "jmp"
            self.eat()
        elif self.current_token[0] == "emp":
            token = "emp"
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
