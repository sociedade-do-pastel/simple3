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
