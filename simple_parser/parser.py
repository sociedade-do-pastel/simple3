import sys
class Parser():
    def __init__(self, lexer, transpilar=False):
        self.lexer = lexer
        # mais facil tratar uma lista sem None nesse caso, a lista é única, não
        # uma matriz
        self.lexer.flatten_token_list()
        # get_next_token funciona a partir de um iterador sobre essa lista
        # "plana" (lembrando que, toda vez que get_next_token é chamado, o
        # iterador sofre uma iteracao)
        self.current_token = self.lexer.get_next_token()
        self.next_token = self.lexer.get_next_token()
        # teste de transpilação
        self.transpilar = transpilar
        self.code = ""
        # teste de debug
        self.code_line = 1
        # dicionario de tokens aceitos em cada nivel
        self.token_aceitos = {
            "decvar": ["type", "var", "operator", "eos"],
            "literal": ["str", "num"],
            "bool": ["tru", "fls"],
            "matlab": ["eos", "num", "(" ")"],
            "operador": ["+", "-", "/", "*", "^"],
            "flux": ["ifi", "scope_init", "scope_end", "els", "elf", "(", ")"],
            "expr": ["(", ")", "and", "orr"],
            "opbool": ["==", ">", ">=", "<", "<="],
            "rpt": ["whl", "for", "(", ")",
                    "scope_init", "scope_end", "type", "operator", "var"],
            "range": ["num", ":"]
        }

    def error(self, message=False):
        raise Exception(message if message else "deu merda")  # arrumar depois

    def eat(self, token_type):
        # token = (tipo, valor, escopo)
        # verifica apenas o primeiro endereço
        if self.current_token[0] == token_type:
            self.current_token = self.next_token
            try:
                self.next_token = self.lexer.get_next_token()
            except:
                self.next_token = None
        else:
            self.error()  # TODO implementar a classe de erro

    def check_eol(self):
        if self.current_token is None: 
            # TODO se for montar árvore, aqui que tá o \n
            if self.transpilar and self.code[-1] != '\n':
                self.code += "\n"
            self.current_token = self.next_token
            self.code_line += 1
            try:
                self.next_token = self.lexer.get_next_token()
            except:
                self.next_token = None

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
                if self.current_token is not None and self.next_token is not None:
                    self.error(f"Erro na linha {self.code_line}: cadeia não reconhecida pela linguagem.")

                if self.transpilar:
                    print("\n\nOLHA O CÓDIGO EM PYTHON AI:")
                    print(self.code, end="")
                sys.exit()
            except Exception as e:
                if "interrupt" in e.args:
                    self.error(f"Erro na linha {self.code_line}: cadeia não reconhecida pela linguagem.")
                    sys.exit()
                chave += 1


    def decvar(self):
        pace = 0

        while pace < 5:
            if self.current_token[0] == "type" and pace == 0:
                self.eat("type")
                pace += 1
            elif self.current_token[0] == "var" and pace == 1:
                if self.transpilar: self.code += self.current_token[1] + " "
                self.eat("var")
                pace += 1
            elif self.current_token[0] == "operator" and pace == 2:
                if self.transpilar: self.code += self.current_token[1] + " "
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
        if self.current_token[0] == "str":
            if self.transpilar: self.code += self.current_token[1] + " "
            self.eat("str")
        elif self.current_token[0] == "num":
            if self.next_token is not None and self.next_token[0] == "operator":
                self.matlab(consume_eos=False)
            else:
                if self.transpilar: self.code += self.current_token[1] + " "
                self.eat("num")
        elif self.current_token[0] == "var":
            if self.next_token is not None and self.next_token[0] == "operator":
                self.matlab(consume_eos=False)
            else:
                if self.transpilar: self.code += self.current_token[1] + " "
                self.eat("var")
        else:
            token_b4_matlab = self.current_token
            try:
                self.matlab(consume_eos=False)
            except:
                if self.current_token == token_b4_matlab:
                    self.bool_ean()
                else:
                    self.erro("erro no literal")

    def bool_ean(self):
        # BOOL = tru | fls
        if self.current_token[0] == "tru":
            if self.transpilar: self.code += "True "
            self.eat("tru")
        elif self.current_token[0] == "fls":
            if self.transpilar: self.code += "False "
            self.eat("fls")
        else:
            self.erro("erro no bool")

    def matlab(self, consume_eos=True):
        # MATLAB   ->  MATLAB' (+ | -) MATLAB' [eos] | MATLAB'
        # MATLAB'  ->  MATLAB'' (* | / | ^) MATLAB'' [eos] | MATLAB''
        # MATLAB'' ->  num | var | '(' MATLAB ')'
        node = self.matlab1(consume_eos)

        while self.current_token[1] in ('+', '-'):
            token = self.current_token
            if self.transpilar: self.code += self.current_token[1] + " "
            self.eat(token[0])
            if consume_eos and token == "eos":
                self.eat("eos")
            node = node + token[1] + self.matlab1(consume_eos)

        return node

    def matlab1(self, consume_eos=True):
        node = self.matlab2(consume_eos)

        while self.current_token[1] in ('*', '/', '^'):
            token = self.current_token
            if self.transpilar: self.code += self.current_token[1] + " "
            self.eat(token[0])
            node = node + token[1] + self.matlab2(consume_eos)
        
        return node

    def matlab2(self, consume_eos=True):
        token = self.current_token

        if token[0] == "num":
            if self.transpilar: self.code += self.current_token[1] + " "
            self.eat("num")
            return str(token[1])
        elif token[0] == "var":
            if self.transpilar: self.code += self.current_token[1] + " "
            self.eat("var")
            return str(token[1])
        elif token[0] == "(":
            if self.transpilar: self.code += self.current_token[1] + " "
            self.eat("(")
            node = self.matlab(consume_eos)
            if self.transpilar: self.code += self.current_token[1] + " "
            self.eat(")")
            return '(' + node + ')'
        else:
            self.erro("erro no matlab")


    def operador(self):
        # OPERADOR = + | - | / | * | ^
        self.eat_generic("operador")

    def flux(self):
        self.erro("erro no flux")
        pass

    def expr(self):
        pass

    def opbool(self):
        # OPBOOL = == | > | >= | < | <=
        self.eat_generic("opbool")

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
