from ply import yacc
from lexer import tokens  # Import tokens from lexer.py
import ast_nodes  # Custom AST node classes (defined below)

# Precedence rules for operators (adjust based on KJPL's rules)
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# --------------------------
# Grammar Rules
# --------------------------

def p_program(p):
    '''
    program : statements
    '''
    p[0] = ast_nodes.ProgramNode(statements=p[1])

def p_statements(p):
    '''
    statements : statements statement
               | statement
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''
    statement : assignment_stmt
              | print_stmt
              | if_stmt
              | while_stmt
              | empty
    '''
    p[0] = p[1]

def p_assignment_stmt(p):
    '''
    assignment_stmt : IDENTIFIER ASSIGN expression SEMICOLON
    '''
    p[0] = ast_nodes.AssignmentNode(identifier=p[1], expression=p[3])

def p_print_stmt(p):
    '''
    print_stmt : PRINT LPAREN expression RPAREN SEMICOLON
    '''
    p[0] = ast_nodes.PrintNode(expression=p[3])

def p_if_stmt(p):
    '''
    if_stmt : IF LPAREN condition RPAREN LBRACE statements RBRACE
            | IF LPAREN condition RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE
    '''
    if len(p) == 8:
        p[0] = ast_nodes.IfNode(condition=p[3], then_block=p[6], else_block=None)
    else:
        p[0] = ast_nodes.IfNode(condition=p[3], then_block=p[6], else_block=p[10])

def p_while_stmt(p):
    '''
    while_stmt : WHILE LPAREN condition RPAREN LBRACE statements RBRACE
    '''
    p[0] = ast_nodes.WhileNode(condition=p[3], body=p[6])

def p_condition(p):
    '''
    condition : expression COMPARISON expression
    '''
    p[0] = ast_nodes.ConditionNode(left=p[1], operator=p[2], right=p[3])

def p_expression(p):
    '''
    expression : expression PLUS term
               | expression MINUS term
               | term
    '''
    if len(p) == 4:
        p[0] = ast_nodes.BinaryOpNode(left=p[1], operator=p[2], right=p[3])
    else:
        p[0] = p[1]

def p_term(p):
    '''
    term : term TIMES factor
         | term DIVIDE factor
         | factor
    '''
    if len(p) == 4:
        p[0] = ast_nodes.BinaryOpNode(left=p[1], operator=p[2], right=p[3])
    else:
        p[0] = p[1]

def p_factor(p):
    '''
    factor : NUMBER
           | IDENTIFIER
           | LPAREN expression RPAREN
    '''
    if isinstance(p[1], int):
        p[0] = ast_nodes.NumberNode(value=p[1])
    elif p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = ast_nodes.IdentifierNode(name=p[1])

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

# --------------------------
# Error Handling
# --------------------------
def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}: Unexpected token '{p.value}'")
    else:
        print("Syntax error: Unexpected end of input")

# --------------------------
# Abstract Syntax Tree (AST) Nodes
# --------------------------
class ast_nodes:
    class ProgramNode:
        def __init__(self, statements):
            self.statements = statements

    class AssignmentNode:
        def __init__(self, identifier, expression):
            self.identifier = identifier
            self.expression = expression

    class PrintNode:
        def __init__(self, expression):
            self.expression = expression

    class IfNode:
        def __init__(self, condition, then_block, else_block):
            self.condition = condition
            self.then_block = then_block
            self.else_block = else_block

    class WhileNode:
        def __init__(self, condition, body):
            self.condition = condition
            self.body = body

    class ConditionNode:
        def __init__(self, left, operator, right):
            self.left = left
            self.operator = operator
            self.right = right

    class BinaryOpNode:
        def __init__(self, left, operator, right):
            self.left = left
            self.operator = operator
            self.right = right

    class NumberNode:
        def __init__(self, value):
            self.value = value

    class IdentifierNode:
        def __init__(self, name):
            self.name = name

# --------------------------
# Build the Parser
# --------------------------
parser = yacc.yacc()
