# lexer.py
import ply.lex as lex

# -------------------------------------
# Token List
# -------------------------------------
tokens = (
    # Keywords
    'LET', 'IF', 'ELSE', 'WHILE', 'FOR', 'FUNCTION', 'RETURN', 'PRINT',
    'INT', 'FLOAT', 'STRING', 'BOOL', 'TRUE', 'FALSE', 'NULL',

    # Literals
    'IDENTIFIER', 'INTEGER', 'FLOAT_NUMBER', 'STRING_LITERAL',

    # Operators
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'EQ', 'NEQ', 'LT', 'GT', 'LEQ', 'GEQ',
    'AND', 'OR', 'NOT',

    # Symbols
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'LBRACKET', 'RBRACKET', 'COMMA', 'SEMICOLON',
    'ASSIGN', 'COLON'
)

# -------------------------------------
# Reserved Keywords
# -------------------------------------
reserved = {
    'let': 'LET',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'fn': 'FUNCTION',
    'return': 'RETURN',
    'print': 'PRINT',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
    'bool': 'BOOL',
    'true': 'TRUE',
    'false': 'FALSE',
    'null': 'NULL'
}

# -------------------------------------
# Token Regex Rules
# -------------------------------------
# Operators
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_EQ = r'=='
t_NEQ = r'!='
t_LT = r'<'
t_GT = r'>'
t_LEQ = r'<='
t_GEQ = r'>='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'

# Symbols
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_SEMICOLON = r';'
t_ASSIGN = r'='
t_COLON = r':'

# -------------------------------------
# Complex Token Rules
# -------------------------------------
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'IDENTIFIER')  # Case-insensitive keywords
    return t

def t_FLOAT_NUMBER(t):
    r'\d+\.\d+([eE][+-]?\d+)? | \d+[eE][+-]?\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'\"(?:\\"|.)*?\" | \'(?:\\\'|.)*?\''
    t.value = t.value[1:-1]  # Remove quotes
    t.value = t.value.replace('\\"', '"').replace("\\'", "'")  # Handle escapes
    return t

# -------------------------------------
# Comment Handling
# -------------------------------------
def t_SINGLE_LINE_COMMENT(t):
    r'//.*'
    pass  # Ignore comments

def t_MULTI_LINE_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')  # Track line numbers
    pass  # Ignore comments

# -------------------------------------
# Whitespace and Newline Handling
# -------------------------------------
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t\r'  # Ignore spaces, tabs, carriage returns

# -------------------------------------
# Error Handling
# -------------------------------------
def t_error(t):
    error_msg = f"Illegal character '{t.value[0]}' at line {t.lineno}"
    print(error_msg)
    t.lexer.skip(1)

# -------------------------------------
# Build the Lexer
# -------------------------------------
lexer = lex.lex()

# -------------------------------------
# Helper Function for Testing
# -------------------------------------
def tokenize_input(input_text):
    lexer.input(input_text)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append({
            "type": tok.type,
            "value": tok.value,
            "line": tok.lineno
        })
    return tokens

if __name__ == "__main__":
    # Test the lexer
    sample_code = """
    let x = 42;
    fn add(a: int, b: int) -> int {
        return a + b;
    }
    print("Result: " + add(5, 3));
    """
    
    tokens = tokenize_input(sample_code)
    for tok in tokens:
        print(f"Line {tok['line']}: {tok['type']} -> {tok['value']}")
