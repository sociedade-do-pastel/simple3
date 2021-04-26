class Parser(list):
    def __init__(self, lexer):
        self.lexer = lexer
        # mais facil tratar uma lista sem None nesse caso, a lista é única, não
        # uma matriz
        self.lexer.flatten_token_list()
        # get_next_token funciona a partir de um iterador sobre essa lista
        # "plana" (lembrando que, toda vez que get_next_token é chamado, o
        # iterador sofre uma iteracao)
        self.current_token = self.lexer.get_next_token()
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

    def error(self):
        raise Exception("deu merda")  # arrumar depois

    def eat(self, token_type):
        # token = (tipo, valor, escopo)
        # verifica apenas o primeiro endereço
        if self.current_token[0] == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()  # TODO implementar a classe de erro

    # Isso aqui é o S dos não terminais
    def init(self):
        while True:
            try:
                self.decvar()
                # self.matlab()
                # self.flux()
                # self.rpt()

                if self.current_token is None: 
                    # TODO se for montar árvore, aqui que tá o \n
                    self.current_token = self.lexer.get_next_token()

            except Exception as e:
                print(e)
                break

    def decvar(self):
        pace = 0

        while pace < 5:
            if self.current_token[0] == "type" and pace == 0:
                self.eat("type")
                pace += 1
            elif self.current_token[0] == "var" and pace == 1:
                self.eat("var")
                pace += 1
            elif self.current_token[0] == "operator" and pace == 2:
                self.eat("operator")
                pace += 1
            elif self.current_token[0] in ("str", "num") and pace == 3:
                self.eat("str" if self.current_token[0] == "str" else "num")
                pace += 1
            elif self.current_token[0] == "eos" and pace == 4:
                self.eat("eos")
                print("DECVAR validado com sucesso!")
                pace += 1
            else:
                self.error()



    def literal(self):
        pass

    def bool_ean(self):
        # BOOL = tru | fls
        self.eat_generic("bool")

    def matlab(self):
        pass

    def operador(self):
        # OPERADOR = + | - | / | * | ^
        self.eat_generic("operador")

    def flux(self):
        pass

    def expr(self):
        pass

    def opbool(self):
        # OPBOOL = == | > | >= | < | <=
        self.eat_generic("opbool")

    def rpt(self):
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
