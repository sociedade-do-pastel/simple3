from .lexer_exceptions import ErroLexer
from . import sym_table, afds


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
        self.flattened_list = []
        self.current_token_it = None

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

    def get_next_token(self):
        '''
        Funciona como um singleton.
        Itera =current_token_it= a cada vez que e chamado.
        '''
        if self.current_token_it is None:
            self.current_token_it = iter(self.flattened_list)
        return next(self.current_token_it)

    def flatten_token_list(self):
        '''
        flatten_token_list gera uma lista "plana".
        Uma vez que a simple3 funciona com
        terminadores de diretiva ";", isso se torna possivel e, alem disso,
        facilita o trabalho de gerar um token a seguir.

        '''
        for lines in self.tokens_reconhecidos:
            if lines is None:
                continue
            for tokens in lines:
                self.flattened_list.append(tokens)

    def lista_p(self):
        # talvez utilize em mais de um lugar
        return isinstance(self.linhas, list)

    def __add_to_symTable(self, sim_tbl):
        self.tabela_simb.insert(sim_tbl[1],
                                sim_tbl[0],
                                sim_tbl[2])

    def reconhecer(self, uma_linha):
        lista_tokens = []
        tamanho_linha = len(uma_linha)

        # caso seja um comentário, ignore a linha
        if uma_linha[0:2] == '/3':
            return lista_tokens

        p1 = 0                  # ponteiro para o início da substring
        p2 = 0                  # ponteiro para o final da substring
        num_temp = ''
        num_received = False

        while (p1 < tamanho_linha and p2 < tamanho_linha):

            # se uma_linha na posição p1 for espaço, ignora
            if uma_linha[p1] == ' ':
                p2 += 1
                p1 += 1
                continue

            result = afds.categorizar_lex(uma_linha[p1:p2+1])

            p2 += 1

            # como é possível identificar um subnúmero como um número, ele
            # salva o token encontrado e prossegue lendo em um range maior;
            # quando não for mais um número encontrado, esse último estado
            # salvo é o maior número encontrado
            if num_received:
                # um número terminado em ponto não é reconhecido, ignorar
                if uma_linha[p2-1] == '.':
                    continue
                # atualiza o estado de num encontrado
                elif result and result[0] == 'num':
                    num_temp = result
                    continue
                # parou de receber num em range maior
                else:
                    num_received = False
                    lista_tokens.append(num_temp)
                    self.__add_to_symTable(num_temp)
                    p2 -= 1
                    p1 = p2

            # token encontrado
            if result:
                if result[0] == 'num':
                    num_temp = result
                    num_received = True
                else:
                    lista_tokens.append(result)
                    self.__add_to_symTable(result)
                    p1 = p2

        # se p1 for diferente de p2 significa que a linha foi finalizada com um
        # bloco não reconhecido, portanto, não aceita
        if p1 != p2:
            return None

        return lista_tokens
