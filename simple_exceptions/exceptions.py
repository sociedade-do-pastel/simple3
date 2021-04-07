class ErroLexer(Exception):
    '''
    Responsavel pelos apontamentos dos erros os quais ocorreram
    no processo de analise lexica.

    Argumentos:
    localizacao -- Analisador lexico, hardcoded para caso um integrante
    queira printar a localizacao hardcoded

    linha -- linha onde tal erro de analise pelos AFDs ocorreu

    mensagem_de_erro -- mensagem descritiva quanto ao erro ocorrido
    '''
    def __init__(self, linha, mensagem_de_erro):
        self.localizacao = "Lexer/Analisador Lexico"
        self.linha = linha
        self.mensagem_de_erro = mensagem_de_erro

    def __str__(self):
        return f'''Erro genérico em {self.localizacao}
        com a mensagem {self.mensagem_de_erro} na linha {self.linha}'''


class ArquivoNaoPadronizado(Exception):
    '''
    Exception basica que ocorre quando um arquivo nao contem
    a extensao .sp3 detalhada na documentacao.

    Argumentos:
    nome_arquivo -- nome do arquivo fonte dado pelo usuario
    '''
    def __init__(self, nome_arquivo):
        self.mensagem_de_erro = f'''O arquivo {nome_arquivo}
        nao está de acordo com o padrão definido na documentação'''

    def __str__(self):
        return self.mensagem_de_erro
