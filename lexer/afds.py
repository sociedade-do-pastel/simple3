def afd_num(lex):
    """
    Função que verifica um num através de seu autômato

    Argumentos:
        lex - Lexema a ser testado

    Retorno:
        - Sucesso: ('str', lex)
        - Falha: None
    """
    afd = {
        0: {'0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1},
        1: {'0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, '.': 2},
        2: {'0': 3, '1': 3, '2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3},
        3: {'0': 3, '1': 3, '2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3}
    }
    final_states = [1, 3]
    current_state = 0

    for word in str(lex):
        current_state = afd[current_state].get(word)
        if current_state is None:
            return None

    if current_state in final_states:
        return ('num', lex)


def afd_var(lex):
    """
    Função que verifica uma variável através de seu autômato

    Argumentos:
        lex - Lexema a ser testado

    Retorno:
        - Sucesso: ('var', lex)
        _ Falha: None
    """
    afd = {
        0: {'a': 1,  'b': 1,  'c': 1,  'd': 1,  'e': 1,  'f': 1,  'g': 1,  'h': 1,  'i': 1,  'j': 1,
            'k': 1,  'l': 1,  'm': 1,  'n': 1,  'o': 1,  'p': 1,  'q': 1,  'r': 1,  's': 1,  't': 1,
            'u': 1,  'v': 1,  'w': 1,  'x': 1,  'y': 1,  'z': 1,  'A': 1,  'B': 1,  'C': 1,  'D': 1,
            'E': 1,  'F': 1,  'G': 1,  'H': 1,  'I': 1,  'J': 1,  'K': 1,  'L': 1,  'M': 1,  'N': 1,
            'O': 1,  'P': 1,  'Q': 1,  'R': 1,  'S': 1,  'T': 1,  'U': 1,  'V': 1,  'W': 1,  'X': 1,
            'Y': 1,  'Z': 1},
        1: {'a': 2,  'b': 2,  'c': 2,  'd': 2,  'e': 2,  'f': 2,  'g': 2,  'h': 2,  'i': 2,  'j': 2,
            'k': 2,  'l': 2,  'm': 2,  'n': 2,  'o': 2,  'p': 2,  'q': 2,  'r': 2,  's': 2,  't': 2,
            'u': 2,  'v': 2,  'w': 2,  'x': 2,  'y': 2,  'z': 2,  'A': 2,  'B': 2,  'C': 2,  'D': 2,
            'E': 2,  'F': 2,  'G': 2,  'H': 2,  'I': 2,  'J': 2,  'K': 2,  'L': 2,  'M': 2,  'N': 2,
            'O': 2,  'P': 2,  'Q': 2,  'R': 2,  'S': 2,  'T': 2,  'U': 2,  'V': 2,  'W': 2,  'X': 2,
            'Y': 2,  'Z': 2},
        2: {'a': 3,  'b': 3,  'c': 3,  'd': 3,  'e': 3,  'f': 3,  'g': 3,  'h': 3,  'i': 3,  'j': 3,
            'k': 3,  'l': 3,  'm': 3,  'n': 3,  'o': 3,  'p': 3,  'q': 3,  'r': 3,  's': 3,  't': 3,
            'u': 3,  'v': 3,  'w': 3,  'x': 3,  'y': 3,  'z': 3,  'A': 3,  'B': 3,  'C': 3,  'D': 3,
            'E': 3,  'F': 3,  'G': 3,  'H': 3,  'I': 3,  'J': 3,  'K': 3,  'L': 3,  'M': 3,  'N': 3,
            'O': 3,  'P': 3,  'Q': 3,  'R': 3,  'S': 3,  'T': 3,  'U': 3,  'V': 3,  'W': 3,  'X': 3,
            'Y': 3,  'Z': 3},
        3: {}
    }
    final_states = [3]
    current_state = 0

    for word in str(lex):
        current_state = afd[current_state].get(word)
        if current_state is None:
            return None

    if current_state in final_states:
        return ('var', lex)


def afd_emp(lex):
    """
    Função que verifica um emp através de seu autômato

    Argumentos:
        lex - Lexema a ser testado

    Retorno:
        - Sucesso: ('emp', 'emp')
        - Falha: None
    """
    afd = {
        0: {'e': 1},
        1: {'m': 2},
        2: {'p': 3},
        3: {}
    }
    final_states = [3]
    current_state = 0

    for word in str(lex):
        current_state = afd[current_state].get(word)
        if current_state is None:
            return None

    if current_state in final_states:
        return ('emp', lex)


def afd_str(lex):
    """
    Função que verifica uma string através de seu autômato

    Argumentos:
        lex - Lexema a ser testado

    Retorno:
        - Sucesso: ('str', lex)
        - Falha: None
    """
    afd = {
        0: {'"': 1},
        1: {'"': 2},
        2: {}
    }
    final_states = [2]
    current_state = 0

    for word in str(lex):
        if current_state == 1:
            current_state = afd[current_state].get(word, 1)
        else:
            current_state = afd[current_state].get(word)
            if current_state is None:
                return None

    if current_state in final_states:
        return ('str', lex)


def afd_keyword(lex):
    """
    Função que verifica uma keyword através de seu autômato

    Argumentos:
        lex - Lexema a ser testado

    Retorno:
        - Sucesso: ('keyword', lex)
        - Falha: None
    """
    afd = {
        0: {
            'b': 1, 'e': 2, 'f': 3, 'i': 4, 'j': 5, 'r': 6, 't': 7, 'v': 8, 'w': 9
        },
        1: {'r': 10},
        2: {'l': 11},
        3: {'o': 12},
        4: {'f': 13},
        5: {'m': 14},
        6: {'e': 15},
        7: {'o': 16},
        8: {'e': 17},
        9: {'h': 18},
        10: {'k': 19},
        11: {'f': 20, 's': 21},
        12: {'r': 22},
        13: {'i': 23},
        14: {'p': 24},
        15: {'t': 25},
        16: {'f': 26},
        17: {'c': 27},
        18: {'l': 28},
        19: {},
        20: {},
        21: {},
        22: {},
        23: {},
        24: {},
        25: {},
        26: {},
        27: {'<': 29},
        28: {},
        29: {'n': 30, 's': 31},
        30: {'u': 32},
        31: {'t': 33},
        32: {'m': 34},
        33: {'r': 35},
        34: {'>': 36},
        35: {'>': 37},
        36: {},
        37: {}
    }
    final_states = [19, 20, 21, 22, 23, 24, 25, 26, 28, 36, 37]
    current_state = 0

    for word in str(lex):
        current_state = afd[current_state].get(word)
        if current_state is None:
            return None

    if current_state in final_states:
        return ('keyword', lex)


def categorizar_lex(lex):
    # uma grande cadeia de condicionais,
    # as prioridades de token sao definidas pela ordem de tais condicionais
    # var nao pode conter numeros, checado primeiro num e nao obtemos conflitos.
    # Talvez seja necessario contruir um afd geral?
    # tipos
    # numeric
    # TODO
    # string
    # TODO
    # empty (nil)
    # TODO
    # keywords
    # TODO
    # identifiers
    # TODO
    # operators
    # TODO
    pass
