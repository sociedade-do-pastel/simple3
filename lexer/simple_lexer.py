from . import sym_table, afds, token as tk


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
        self.tabela_simb = sym_table.SymbolsTable()
        self.tokens_reconhecidos = []

    def analise_lexica(self):
        if self.lista_p():
            self.tokens_reconhecidos = [
                self.reconhecer(linh) for linh in self.linhas]

    def get_tokens(self, linha_escolhida):
        return self.tokens_reconhecidos[linha_escolhida+1]

    def lista_p(self):
        # talvez utilize em mais de um lugar
        return isinstance(self.linhas, list)

    def reconhecer(self, un_lin):
        # retornam-se os tokens de uma unica linha
        # cada token seria objeto instanciado da clase Token
        lista_tokens = []
        for token in un_lin.split():
            lex_categorizado = afds.categorizar_lex(token)
            self.tabela_simb.insert(lex_categorizado[1],
                                    lex_categorizado[0],
                                    lex_categorizado[2])
            lista_tokens.append(tk.Token(lex_categorizado))
        return lista_tokens
