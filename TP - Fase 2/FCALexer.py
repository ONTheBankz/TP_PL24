import ply.lex as lex

# Definição dos tokens
tokens = (
    'NUMBER',
    'IDENTIFIER',
    'STRING',
    'ESCREVER',
    'ENTRADA',
    'ALEATORIO',
    'CONCAT',
    'FUNCAO'
)

# Definição dos literais
literals = ['+', '-', '*', '/', '(', ')', '=', ';', ',', ':', '[', ']']

# Ignorar espaços e tabulações
t_ignore = " \t"

# Definição das expressões regulares para os tokens
def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\"]|\\.)*\"'
    t.value = t.value[1:-1]  # Remove as aspas
    return t

def t_CONCAT(t):
    r'<>'
    return t

def t_FUNCAO(t):
    r'FUNCAO'
    return t

def t_ESCREVER(t):
    r"[Ee][Ss][Cc]([Rr][Ee][Vv][Ee][Rr])?\b"
    return t

def t_ENTRADA(t):
    r"[Ee][Nn][Tt]([Rr][Aa][Dd][Aa])?\b"
    return t

def t_ALEATORIO(t):
    r"[Aa][Ll][Ee]([Aa][Tt][Oo][Rr][Ii][Oo])?\b"
    return t

def t_IDENTIFIER(t):
    r"[a-z_][a-zA-Z0-9_]*[\?\!]*"
    return t

# Ignorar comentários de múltiplas linhas
def t_comment_multi(t):
    r'\{\-([\s\S]*?)\-\}'
    t.lexer.lineno += t.value.count('\n')
    pass

# Ignorar comentários de uma linha
def t_comment_single(t):
    r'\-\-.*'
    pass

# Contagem de novas linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erros
def t_error(t):
    print(f"Unexpected token: [{t.value[:10]}]")
    t.lexer.skip(1)

# Criação do lexer
lexer = lex.lex()
