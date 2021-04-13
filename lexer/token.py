class Token:
    '''
    Representando um unico token, esta carrega
    as principais caracteristicas de um

    Membros:
    tipo -- tipo do token (ele mesmo, keyword, string, num, variavel, etc. )
    valor -- valor literal do token (caractere em ascii)
    '''

    def __init__(self, tupla_desc_token):
        self.tipo = tupla_desc_token[0]
        self.valor = tupla_desc_token[1]

    def __str__(self):
        return f'Tipo = {self.tipo}, valor = {self.valor}'
