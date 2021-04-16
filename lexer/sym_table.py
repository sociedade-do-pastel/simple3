# Leon Ferreira Bellini    | 22.218.002-8
# Felipe Maciel de Sousa   | 22.218.042-4
# Pedro Freitas Barbosa    | 22.218.013-5
# Guilherme Ormond Sampaio | 22.218.007-7

class SymbolsTable():
    def __init__(self):
        """
            Quando a classe SymbolsTable for instanciada,
            será criado um dicionário vazio chamado 'table'
            para armazenar as variáveis.
        """
        self._table = dict()

    def get_table(self):
        """
            O método 'get_table()', retorna uma cópia do dicionário 'table'
            contendo o nome das variáveis e seus respectivos tipos e escopos.
            Caso não encontre o dicionário, será retornado None.
        """
        return self._table.copy()

    def insert(self, name, rec_type, scope):
        """Insere ou atualiza um símbolo na tabela.

        Argumentos:
        name  -- nome do símbolo e também sua chave na tabela
        rec_type  -- tipo do símbolo
        scope -- escopo no qual o símbolo pertence

        Retorno:
        Conteúdo da linha do elemento inserido.
        """

        name_exists = self._table.get(name)

        if scope > 0:
            name_scope = "local"
        else:
            name_scope = "global"

        if name_exists:
            self._table[name].append({'type': rec_type, 'scope': name_scope})
        else:
            self._table[name] = [dict({'type': rec_type, 'scope': name_scope})]

        return self._table

    def lookup(self, name):
        """Método de lookup (busca) para os símbolos da tabela,
        este utilizando-se do método nativo de dicionários get().

        Argumentos:
        name -- "Nome" do símbolo a ser procurado

        Retorno:
        Valor do símbolo a ser encontrado ou None

        """
        return self._table.get(name)
