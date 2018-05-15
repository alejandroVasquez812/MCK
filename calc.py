# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------

import sys
import math
import ply.yacc as yacc
import ply.lex as lex
import matrix
import asciimathml
import MathFunctions
import sympy

from xml.etree.ElementTree import tostring


sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input


literals = ['=', '+', '-', '*', '/', '(', ')', '^',',','[',']']

reserved = {
    'integral': 'INTEGRAL',
    'from': 'FROM',
    'to': 'TO',
    'derivative': 'DERIVATIVE',
    'limit': 'LIMIT',
    'when': 'WHEN',
    'of': 'OF',
    'oo': 'INFINITY',
    'sum': 'SUM',
    'product': 'PRODUCT',
    'sin': 'SIN',
    'cos': 'COS',
    'tan': 'TAN',
    'solve': 'SOLVE',
    'varlist' : 'PRINTLIST',
}

# Tokens
tokens = [
    'VAR',
    'FLOAT',
    'INT',
    'POWER',
    'X',
    'GOES',
    ] + list(reserved.values())


t_POWER = r'\^'
t_GOES = r'\->'
t_X = r'[x]'

def t_VAR(t):
    r'[a-wyzA-WYZ][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'VAR')    # Check for reserved words
    return t


# Set floating point structure
#   number '.' number                   -> example. 12.34
#   number '.' number 'e' '+/-' number  -> example. 12.34e+56 or 12.34E-56
#   number 'e' '+/-' number             -> example. 12E+34 or 12e-34
def t_FLOAT(t):
    r'([0-9]+)?([.][0-9]+)([eE][+-]?[0-9]+)?'
    t.value = float(t.value)
    return t


# Set integer structure
def t_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded


def t_error(t):
    print ("ERROR: Line %d: LEXER: Illegal character '%s' " % (t.lexer.lineno, t.value[0]))
    t.lexer.skip(1)


t_ignore = " \t"


# Build the lexer

lex.lex()

# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', 'POWER'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}


def p_statement_assign(p):
    'statement : VAR "=" expression'
    names[p[1]] = p[3]


def p_statement_expr(p):
    'statement : expression'
    print(p[1])


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression POWER expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '^' and p[1] != "x" and p[3] != "x":
        p[0] = p[1] ** p[3]
    elif p[2] == '^' and p[1] == "x" or p[3] == "x":
        p[0] = str(p[1]) + '^' + str(p[3])

    if p[2] != '^':
        y = tostring(asciimathml.parse(str(p[1])))
        y = y + tostring(asciimathml.parse(str(p[2])))
        y = y + tostring(asciimathml.parse(str(p[3])))

        x = tostring(asciimathml.parse(str(p[0])))

        print(str(y, "utf-8") + "=" + str(x, "utf-8"))
    elif p[1] != "x" and p[3] != "x":
        y = tostring(asciimathml.parse(str(p[1]) + "^" + str(p[3])))
        x = tostring(asciimathml.parse(str(p[0])))
        print(str(y, "utf-8") + "=" + str(x, "utf-8"))


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_number(p):
    "expression : INT"
    p[0] = p[1]


def p_expression_name(p):
    "expression : VAR"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


def p_expression_solve(p):
    '''expression : SOLVE expression'''
    if s.find('^') != -1:
        eq = MathFunctions.formateq(p[2])
    else:
        eq = str(p[2])
    if p[2] is not None:
        eq = (str(MathFunctions.msolve(eq, MathFunctions.symbols('x'))))
        eq = MathFunctions.reformateq(eq)
        p[0] = eq

    else:
        pass


def p_expression_derivative(p):
    '''expression : DERIVATIVE OF expression'''
    if s.find('^') != -1:
        eq = MathFunctions.formateq(p[3])
    else:
        eq = str(p[3])
    if p[3] is not None:
        eq = (str(MathFunctions.derivative(eq, MathFunctions.symbols('x'))))
        eq = MathFunctions.reformateq(eq)
        p[0] = eq
        w = tostring(asciimathml.parse('frac{d}{dx}'))
        y = tostring(asciimathml.parse(str(p[3])))
        x = tostring(asciimathml.parse(str(p[0])))
        print(str(w, "utf-8") + str(y, "utf-8") + "=" + str(x, "utf-8"))

    else:
        pass


def p_expression_limit(p):
    '''expression : LIMIT WHEN X GOES expression OF expression
              | LIMIT WHEN X GOES INFINITY OF expression'''

    limitOf = str(p[3])
    tendsTo = str(p[5])
    eq1 = str(p[7])

    if s.find('^') != -1:
        eq = MathFunctions.formateq(eq1)
    else:
        eq = str(eq1)
    if limitOf is not None and tendsTo is not None and p[7] is not None:
        eq = (str(MathFunctions.limits(eq, MathFunctions.symbols('x'), tendsTo)))
        eq = MathFunctions.reformateq(eq)
        p[0] = eq
        y = tostring(asciimathml.parse("lim_(" + str(limitOf) + "->" + str(tendsTo) + ")"))
        x = tostring(asciimathml.parse(str(p[0])))
        print(str(y, "utf-8") + "=" + str(x, "utf-8"))
    else:
        pass

def p_expression_integral(p):
    '''expression : INTEGRAL OF expression'''
    if s.find('^') != -1:
        eq = MathFunctions.formateq(p[3])
    else:
        eq = str(p[3])
    if p[3] is not None:
        eq = (str(MathFunctions.integration(eq, MathFunctions.symbols('x'))))
        eq = MathFunctions.reformateq(eq)
        p[0] = eq

        y = tostring(asciimathml.parse("int" + str(p[3])))
        x = tostring(asciimathml.parse(str(p[0])))
        print(str(y, "utf-8") + "=" + str(x, "utf-8"))
    else:
        pass

def p_expression_definite_integral(p):
    '''expression : INTEGRAL FROM expression TO expression OF expression
              | INTEGRAL FROM expression TO INFINITY OF expression'''
    lowerbound = str(p[3])
    highbound = str(p[5])
    eq1 = str(p[7])
    if s.find('^') != -1:
        eq = MathFunctions.formateq(eq1)
    else:
        eq = str(eq1)
    if lowerbound is not None and highbound is not None and p[7] is not None:
        eq = (str(MathFunctions.integration(eq, (MathFunctions.symbols('x'), lowerbound, highbound))))
        eq = MathFunctions.reformateq(eq)
        p[0] = eq
        y = tostring(asciimathml.parse("int_"+lowerbound+"^"+highbound + " " + str(p[7])))
        x = tostring(asciimathml.parse(str(p[0])))
        print(str(y, "utf-8") + "=" + str(x, "utf-8"))
    else:
        pass


def p_eq_x(p):
    '''equation : X'''
    p[0] = str(p[1])


def p_expression_eq(p):
    '''expression : equation'''
    p[0] = str(p[1])


def p_mult_equation(p):
    '''equation : INT X'''
    p[0] = str(p[1]) + '*' + str(p[2])


def p_more_equations(p):
    '''equation : equation '+' equation
                  | equation '-' equation
                  | equation '*' equation
                  | equation '/' equation
                  | equation POWER equation
                  | equation '+' expression
                  | equation '-' expression
                  | equation '*' expression
                  | equation '/' expression
                  | equation POWER expression
                  | expression '+' equation
                  | expression '-' equation
                  | expression '*' equation
                  | expression '/' equation
                  | expression POWER equation'''
    if p[1] is None or p[3] is None:
        pass
    else:
        p[0] = str(p[1]) + str(p[2]) + str(p[3])


def p_expression_trigonometry(p):
    '''expression : SIN '(' expression ')'
                | COS '(' expression ')'
                | TAN '(' expression ')' '''
    p[0] = str(p[1]) + str(p[2]) + str(p[3]) + str(p[4])
    if p[1] == 'sin':
       p[0]=(math.sin(p[3]))
    if p[1] == 'cos':
       p[0] (math.cos(p[3]))
    if p[1] == 'tan':
       p[0]=(math.tan(p[3]))
    y = tostring(asciimathml.parse(str(p[1]) + str(p[3])))
    x = tostring(asciimathml.parse(str(p[0])))
    print(str(y, "utf-8") + "=" + str(x, "utf-8"))

def p_Celsius_Fahrenheit_Float(p):	
    '''	expression : INT VAR
		           | FLOAT VAR 
	'''
    if p[2] == 'F':
        temp =( (p[1] -32) / 9.0 *5.0)
        p[0]=("%s ° C "% temp)
    elif p[2] == 'C':
        temp = ( 9.0  / 5.0 *  p[1] + 32)
        p[0]= ("%s ° F "% temp)
    y = tostring(asciimathml.parse(str(p[1]) + "° " + str(p[2])))
    x = tostring(asciimathml.parse(str(p[0])))
    print(str(y, "utf-8") + "=" + str(x, "utf-8") )
# matrix 2x 2


def p_matrix_List(p):
   '''expression : '[' INT ',' INT ']' ',' '[' INT ',' INT ']'
   '''
   z = p[2]*p[10]-p[4]*p[8]
   y = tostring(asciimathml.parse("[[" + str(p[2]) + "," + str(p[4]) + "],[" + str(p[8]) + "," + str(p[10]) + "]]"))
   x = tostring(asciimathml.parse(str(z)))
   p[0] = z
   print(str(y, "utf-8") + "=" + str(x, "utf-8"))



def p_expression_sum(p):
    '''expression : SUM FROM expression TO expression OF expression'''
    lowerBound = p[3]
    highBound = p[5]
    eq1 = str(p[7])
    if s.find('^') != -1:
        eq = MathFunctions.formateq(eq1)
    else:
        eq = str(eq1)
    if lowerBound is not None and highBound is not None and p[7] is not None:
        p[0] = MathFunctions.summation(eq, lowerBound, highBound, MathFunctions.symbols('x'))
        y = tostring(asciimathml.parse("sum_"+ str(lowerBound) +"^"+ str(highBound)+ " " + str(p[7])))
        x = tostring(asciimathml.parse(str(p[0])))
        print(str(y, "utf-8") + "=" + str(x, "utf-8"))

    else:
        pass



def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")



yacc.yacc()

while 1:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)
