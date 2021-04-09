from . import categorizar_lex


class simple_lexer:
    '''
    Implementação do analisador lexico de passagem unica.
    Pelo fato deste apenas
    "existir" durante uma unica sessão, este é construido
    com um unico argumento (string ou lista de strings).

    (estao livres para modificar este comportamento)
    '''

    def __init__(self, linhas_p_tratar):
        self.linhas = linhas_p_tratar
        self.tokens_reconhecidos = []

    def analiseLexica(self):
        if self.listaP():
            linhas_an = [self.reconhecer(linh) for linh in self.linhas]
        else:
            pass  # TODO reconhecer unica string
        self.tokens_reconhecidos = linhas_an

    def getTokens(self, linha_escolhida):
        return self.tokens_reconhecidos[linha_escolhida]

    def getNextToken(self):
        pass

    def listaP(self):
        # talvez utilize em mais de um lugar
        return isinstance(self.linhas, list)

    def reconhecer(self, un_lin):
        # retornam-se os tokens de uma unica linha
        # cada token seria objeto instanciado da clase Token
        # (como o prof recomendou)?
        return [categorizar_lex(token) for token in un_lin.split(" ")]
