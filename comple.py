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
import os


def FileReader(filename):
    pass
        

def main(argv, argc):
    filename_to_save = "output.py" 
    
    FileReader(argv[1])
    # TODO tratar filenames de saída customizáveis

if __name__ == '__main__':
    main(sys.argv, sys.argc)
    
