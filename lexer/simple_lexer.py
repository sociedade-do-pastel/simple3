from simple_exceptions.exceptions import ErroLexer
from . import sym_table, afds, token as tk
import sys
sys.path.append("..")


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
        '''
        Responsavel pelo tratamento de cada linha em tokens.
        '''
        if self.lista_p():
            for num_linha, linha_unica in enumerate(self.linhas, 1):
                # se linha recebida era formada por '\n'
                if linha_unica is None:
                    self.tokens_reconhecidos.append(None)
                    continue
                tokens_linha = self.reconhecer(linha_unica)
                # se teve um token nao reconhecido
                # instanciar erro com o numero de linha correto
                if tokens_linha is None:
                    raise ErroLexer(num_linha, "Token nao reconhecido")
                else:
                    self.tokens_reconhecidos.append(tokens_linha)

    def get_tokens(self, linha_escolhida):
        return self.tokens_reconhecidos[linha_escolhida+1]

    def lista_p(self):
        # talvez utilize em mais de um lugar
        return isinstance(self.linhas, list)

    def reconhecer(self, uma_linha):
        # retornam-se os tokens de uma unica linha
        # cada token seria objeto instanciado da clase Token
        lista_tokens = []
        for token in uma_linha.split():
            lex_categorizado = []
            result = afds.categorizar_lex(token)
            # retornada uma lista de tokens ou um unico
            lex_categorizado += result if isinstance(
                result, list) else [result]

            if None in lex_categorizado:
                return None

            # O(n) no pior caso, O(1) sem recursoes
            for lista_tok in lex_categorizado:
                self.tabela_simb.insert(lista_tok[1],
                                        lista_tok[0],
                                        lista_tok[2])  # tuplas atrapalham aqui
                lista_tokens.append(tk.Token(lista_tok))
        return lista_tokens
