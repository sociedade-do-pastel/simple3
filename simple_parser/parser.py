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
                    "scope_init", "scope_end", "type", "operator", "var"]
        }

    def error(self):
        raise Exception("deu merda")  # arrumar depois

    def eat(self, token_type):
        # token = (tipo, valor, escopo)
        # verifica apenas o primeiro endereço
        if self.current_token[0] == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.erro()  # TODO implementar a classe de erro

    """
        Isso aqui é o S dos não terminais
    """

    def init(self):
        pass

    def decvar(self):
        pass

    def literal(self):
        pass

    def bo0l(self):  # lembra q tem o 0
        pass

    def matlab(self):
        pass

    def operador(self):
        pass

    def flux(self):
        pass

    def expr(self):
        pass

    def opbool(self):
        pass

    def rpt(self):
        pass

    def r4nge(self):  # lembra q tem o 4
        pass
