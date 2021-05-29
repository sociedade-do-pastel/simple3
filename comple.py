# -*- coding: utf-8 -*-
##############################################################
# Compilador para a linguagem de programação simple3.        #
# Neste arquivo estão presentes os métodos para delegação    #
# para análise léxica, análise sintática e semântica.        #
#                                                            #
# Para compilar basta invocar o nome do arquivo a ser        #
# compilado procedido por                                    #
# "python comple.py <nome arquivo>.sp3 [saida]"              #
##############################################################
import sys
# imports das classes do grupo
from simple_exceptions import exceptions
# aqui virao os analisadores lexico e sintatico
from simple_lexer.lexer import Lexer
from simple_lexer.lexer_exceptions import ErroLexer
from simple_parser.parser import Parser


def GetAsList(filename):
    """Retorna o arquivo lido como uma lista sem caracteres de nova linha."""
    with open(filename, "r") as arquivo:
        return [None if lin == '\n' else
                lin.strip() for lin in arquivo.readlines()]


def FileReader(filename, listar=False):
    """
    Retorna uma lista referente a todas as linhas do arquivo lido.

    No caso, com uma lista, e possivel determinar o numero da linha que um erro
    tenha ocorrido utilizando-se do indice da lista+1.
    """
    if filename.split(".")[1] != "sp3":
        raise exceptions.ArquivoNaoPadronizado(filename)  # se não for .sp3

    return GetAsList(filename)


def compiledFileSave(filename, target):
    """Salvamento do arquivo compilado com seu filename passado como arg."""
    with open(filename, "w") as arquivo:
        for element in target:
            arquivo.write(f'{element}\n')


def getOutputName(argv):
    """Definido ``filename'' do arquivo de saída dependente do input."""
    if len(argv) == 3 and argv[2][-3:] == ".py":
        filename_to_save = f"{argv[2]}"
    elif len(argv) == 3:
        filename_to_save = f"{argv[2]}.py"
    else:
        filename_to_save = f"{argv[1].split('/')[-1][:-4]}.py"

    return filename_to_save


def main(argv):
    """Função principal a qual define as fases da compilação."""
    if len(argv) < 2:
        print("Necessario um arquivo fonte da linguagem", file=sys.stderr)
        sys.exit(1)  # se o usuario nao inseriu um arquivo fonte
    else:
        arquivo_raw = argv[1]

        filename_to_save = getOutputName(argv)

        try:
            alvo_comp = FileReader(arquivo_raw, True)
        except exceptions.ArquivoNaoPadronizado as ExcObj:
            print(ExcObj, file=sys.stderr)
        except FileNotFoundError as FileError:
            print(f'{arquivo_raw} no encontrado: {FileError}', file=sys.stderr)
        except IndexError as Indice:
            print(f'Argumentos faltantes, inserir nome do arquivo\n\n{Indice}',
                  file=sys.stderr)
        # quando ocorrido algum erro na etapa de análise léxica
    try:
        lexing_object = Lexer(alvo_comp)
        lexing_object.analise_lexica()
    except ErroLexer as LexErr:
        print(LexErr, sys.stderr)
        sys.exit(1)

    lexing_object.flatten_token_list()

    try:
        parsing_object = Parser(lexing_object.flattened_list)
        parsing_object.parse()
        parsing_object.solve()  # analisador semântico
    except Exception as exx:
        print(exx)
        sys.exit(1)

    compiledFileSave(filename_to_save, parsing_object.treeList)


if __name__ == '__main__':
    main(sys.argv)
