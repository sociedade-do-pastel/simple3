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
from lexer.simple_lexer import simple_lexer
from lexer.lexer_exceptions import ErroLexer
from simple_parser.parser import Parser


def GetAsList(filename):
    """
    Retorna o arquivo lido como uma lista sem caracteres de nova linha
    """
    with open(filename, "r") as arquivo:
        return [None if lin == '\n' else lin.strip() for lin in arquivo.readlines()]


def FileReader(filename, listar=False):
    """
    Retorna uma lista referente a todas as linhas do arquivo lido. No caso, com
    uma lista, e possivel determinar o numero da linha que um erro tenha
    ocorrido utilizando-se do indice da lista+1.
    """
    if filename.split(".")[1] != "sp3":
        raise exceptions.ArquivoNaoPadronizado(filename)

    return GetAsList(filename)


def compiledFileSave(filename, target, lex=False):
    if lex:
        with open(filename, "w") as arquivo:
            for num, linhas in enumerate(target.tokens_reconhecidos, 1):
                arquivo.write(f'Linha: {num} ')
                if linhas is not None:
                    for lexemas in linhas:
                        arquivo.write(f'{str(lexemas)}, ')
                arquivo.write('\n')
            arquivo.write('\n'*10)
            arquivo.write('Tabela de simbolos:\n')
            for key, value in target.tabela_simb.get_table().items():
                arquivo.write(f'{key} : {value} \n')


def main(argv):
    filename_to_save = "output.txt"

    if len(argv) < 2:
        print("Necessario um arquivo fonte da linguagem", file=sys.stderr)
        exit(1)  # se o usuario nao inseriu um arquivo fonte
    else:
        arquivo_raw = argv[1]
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
        lexing_object = simple_lexer(alvo_comp)
        lexing_object.analise_lexica()
    except ErroLexer as LexErr:
        print(LexErr, sys.stderr)
    try:
        parsing_object = Parser(lexing_object, transpilar=False)
        # parsing_object.init()
    except Exception as exx:
        print(exx)

    # TODO tratar filenames de saída customizáveis (necessário?)
    compiledFileSave(filename_to_save,
                     lexing_object, lex=True)


if __name__ == '__main__':
    main(sys.argv)
