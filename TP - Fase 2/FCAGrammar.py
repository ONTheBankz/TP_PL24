import ply.yacc as yacc
from FCALexer import tokens

# Dicionário para armazenar funções
functions = {}

# Precedência dos operadores
precedence = (
    ('left', 'CONCAT'),
    ('left', '+', '-'),
    ('left', '*', '/'),
)

# Definição das regras gramaticais
def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : assignment_statement
                 | command_statement
                 | function_declaration'''
    p[0] = p[1]

def p_function_declaration(p):
    '''function_declaration : FUNCAO IDENTIFIER '(' parameter_list ')' ',' ':' expression ';' '''
    func_name = p[2]
    params = p[4]
    body = p[8]
    param_count = len(params)
    if func_name not in functions:
        functions[func_name] = {}
    functions[func_name][param_count] = (params, body)

def p_parameter_list(p):
    '''parameter_list : IDENTIFIER
                      | parameter_list ',' IDENTIFIER
                      | empty'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    else:
        p[0] = p[1] + [p[3]]

def p_assignment_statement(p):
    '''assignment_statement : IDENTIFIER '=' expression ';' '''
    p[0] = ('assign', p[1], p[3])

def p_command_statement(p):
    '''command_statement : ESCREVER '(' expression ')' ';'
                         | ESCREVER expression ';'
                         | ALEATORIO '(' ')' ';'
                         | ALEATORIO '(' expression ')' ';' '''
    if p[1].lower() in ('escrever', 'esc'):
        if len(p) == 6:
            p[0] = ('escrever', p[3])
        else:
            p[0] = ('escrever', p[2])
    elif p[1].lower() in ('aleatorio', 'ale'):
        if len(p) == 6:
            p[0] = ('aleatorio', p[3])
        else:
            p[0] = ('aleatorio',)

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_concat(p):
    '''expression : expression CONCAT expression'''
    p[0] = ('concat', p[1], p[3])

def p_expression_group(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = ('num', p[1])

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = ('string', p[1])

def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    p[0] = ('var', p[1])

def p_expression_function_call(p):
    '''expression : IDENTIFIER '(' argument_list ')' '''
    p[0] = ('call', p[1], p[3])

def p_expression_list(p):
    '''expression : '[' element_list ']' '''
    p[0] = ('list', p[2])

def p_element_list(p):
    '''element_list : expression
                    | element_list ',' expression
                    | empty'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    else:
        p[0] = p[1] + [p[3]]

def p_argument_list(p):
    '''argument_list : expression
                     | argument_list ',' expression
                     | empty'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    else:
        p[0] = p[1] + [p[3]]

def p_expression_entrada(p):
    '''expression : ENTRADA '(' ')' '''
    p[0] = ('entrada',)

def p_expression_aleatorio(p):
    '''expression : ALEATORIO '(' expression ')' '''
    p[0] = ('aleatorio', p[3])

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error: unexpected '{p.type}' at {p.value!r}")
    else:
        print("Syntax error: unexpected end of file")
    exit(1)

# Criação do parser
parser = yacc.yacc()
def parse(input_string):
    return parser.parse(input_string)
