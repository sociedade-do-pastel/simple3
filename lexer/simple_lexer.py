from . import afds


class simple_lexer:
    '''
    Implementação do analisador lexico de passagem unica.
    Pelo fato deste apenas
    "existir" durante uma unica sessão, este é construido
    com um unico argumento (lista de strings).

    (estao livres para modificar este comportamento)
    '''

    def __init__(self, linhas_p_tratar):
        self.linhas = linhas_p_tratar
        self.tokens_reconhecidos = []

    def analise_lexica(self):
        if self.lista_p():
            self.tokens_reconhecidos = [self.reconhecer(linh) for linh in self.linhas]

    def get_tokens(self, linha_escolhida):
        return self.tokens_reconhecidos[linha_escolhida]

    def lista_p(self):
        # talvez utilize em mais de um lugar
        return isinstance(self.linhas, list)

    def reconhecer(self, un_lin):
        # retornam-se os tokens de uma unica linha
        # cada token seria objeto instanciado da clase Token
        # (como o prof recomendou)?
        return [afds.categorizar_lex(token) for token in un_lin.split()]
