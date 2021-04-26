class Parser(list):
    def __init__(self, lexer):
        # mais facil tratar uma lista sem None nesse caso, a lista é única, não
        # uma matriz
        lexer.flatten_token_list()
        # get_next_token funciona a partir de um iterador sobre essa lista
        # "plana" (lembrando que, toda vez que get_next_token é chamado, o
        # iterador sofre uma iteracao)
        self.current_token = lexer.get_next_token()

    def error(self):
        raise Exception("deu merda")  # arrumar depois

    def eat(self, token_type):
        pass

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
