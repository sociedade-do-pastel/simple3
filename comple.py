# -*- coding: utf-8 -*-
##############################################################
# Compilador para a linguagem de programação simple3.        #
# Neste arquivo estão presentes os métodos para delegação    #
# para análise léxica e análise sintática (TODO).            #
#                                                            #
# Para compilar basta invocar o nome do arquivo a ser        #
# compilado procedido por                                    #
# "python comple.py <nome arquivo>.sp3"                      #
##############################################################
import sys
# imports das classes do grupo
from simple_exceptions import exceptions
# aqui virao os analisadores lexico e sintatico
# from lexer import lexer   # ou algo assim
# from parser import parser # same as before


def GetAsList(filename):
    """
    Retorna o arquivo lido como uma lista sem caracteres de nova linha
    """
    with open(filename, "r") as arquivo:
        return [linhas.strip("\n") for linhas in arquivo.readlines()]


def GetAsString(filename):
    """
    Retorna o arquivo lido como uma string completa
    """
    with open(filename, "r") as arquivo:
        return arquivo.read().strip("\n")


def FileReader(filename, listar=False):
    """
    Retorna uma lista ou string referente a todas as linhas do arquivo
    lido. O implementador pode escolher como realizar o processo de parsing,
    porem, no caso da lista, e possivel determinar o numero da linha
    que um erro tenha ocorrido utilizando-se do indice da lista+1.
    """
    if filename.split(".")[1] != ".sp3":
        raise exceptions.ArquivoNaoPadronizado
    else:
        if listar:
            return GetAsList(filename)
        return GetAsString(filename)


def main(argv):
    filename_to_save = "output.py"

    if len(argv) < 2:
        print("Necessario um arquivo fonte da linguagem", file=sys.stderr)
        exit(1)  # se o usuario nao inseriu um arquivo fonte

    arquivo_raw = argv[1]
    try:
        alvo_comp = FileReader(arquivo_raw, True)
        print(alvo_comp)
    except exceptions.ArquivoNaoPadronizado as ExcObj:
        print(ExcObj, file=sys.stderr)
    except FileNotFoundError as FileError:
        print(f'{arquivo_raw} no encontrado: {FileError}', file=sys.stderr)
    except IndexError as Indice:
        print(f'Argumentos faltantes, inserir nome do arquivo\n\n{Indice}', file=sys.stderr)
    # quando ocorrido algum erro na etapa de análise léxica
    try:
        # TODO realizar aqui processo de analise lexica
        # lexer(alvo_comp)
        pass
    except exceptions.ErroLexer as LexErr:
        print(LexErr, sys.stderr)
    # TODO tratar filenames de saída customizáveis (necessário?)
    # compiledFileSave(filename_to_save)


if __name__ == '__main__':
    main(sys.argv)
