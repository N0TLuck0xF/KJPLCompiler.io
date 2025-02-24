import ply.yacc as yacc
from lexer import tokens

# Grammar rules
def p_program(p):
    '''program : statement
              | program statement'''
    pass

def p_statement(p):
    '''statement : PRINT expression
                | expression'''
    pass

def p_expression(p):
    '''expression : expression PLUS term
                  | term'''
    pass

def p_term(p):
    '''term : NUMBER'''
    pass

# Error handling
def p_error(p):
    print("Syntax error!")

# Build the parser
parser = yacc.yacc()
