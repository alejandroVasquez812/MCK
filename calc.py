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
from xml.etree.ElementTree import tostring

sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input


literals = ['=', '+', '-', '*', '/', '(', ')', '^',',','[',']']

reserved = {
    'integral': 'INTEGRAL',
    'from': 'FROM',
    'to': 'TO',
    'derivation': 'DERIVATIVE',
    'limit': 'LIMIT',
    'when': 'WHEN',
    'of': 'OF',
    'oo': 'INFINITY',
    'sum': 'SUM',
    'product': 'PRODUCT',
    'sin': 'SIN',
    'cos': 'COS',
    'tan': 'TAN',
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


def p_result_derivative(p):
    '''expression : DERIVATIVE OF expression'''
    if s.find('^') != -1:
        eq = MathFunctions.formateq(p[3])
    else:
        eq = str(p[3])
    if p[3] is not None:
        eq = (str(MathFunctions.derivative(eq, MathFunctions.symbols('x'))))
        eq = MathFunctions.reformateq(eq)
        p[0] = eq
    else:
        pass


def p_result_limit(p):
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
    else:
        pass

def p_result_integral(p):
    '''expression : INTEGRAL OF expression'''
    if s.find('^') != -1:
        eq = MathFunctions.formateq(p[3])
    else:
        eq = str(p[3])
    if p[3] is not None:
        eq = (str(MathFunctions.integration(eq, MathFunctions.symbols('x'))))
        eq = MathFunctions.reformateq(eq)
        p[0] = eq
    else:
        pass


def p_result_definite_integral(p):
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
    else:
        pass


def p_expression_x(p):
    '''expression : X'''
    p[0] = str(p[1])


def p_mult_expression(p):
    '''expression : INT X'''
    p[0] = str(p[1]) + '*' + str(p[2])


def p_expression_trigonometry(p):
    '''expression : SIN '(' expression ')'
                | COS '(' expression ')'
                | TAN '(' expression ')' '''
    p[0] = str(p[1]) + str(p[2]) + str(p[3]) + str(p[4])
    if p[1] == 'sin':
       p[0]=("Answer: %s: "% math.sin(p[3]))
    if p[1] == 'cos':
       p[0] ("Answer: %s" % math.cos(p[3]))
    if p[1] == 'tan':
       p[0]=("Answer: %s" % math.tan(p[3]))

def p_Celsius_Fahrenheit_Float(p):	
	'''	expression : INT VAR
		           | FLOAT VAR 
	'''
	if p[2] == 'F':
	     temp =( (p[1] -32) / 9.0 *5.0)
	     p[0]=("%s Celsius", temp)
	elif p[2] == 'C':
	  temp = ( 9.0  / 5.0 *  p[1] + 32) 
	  p[0]= ("%s Fahrenheit"% temp)
# matrix 2x 2
def p_matrix_List(p):
	#creando la lista 
    '''  expression : '[' INT ']' ',' '[' INT ']'
    '''
    #print(p[2])
    #print(p[6])
    sampleList = []
    sampleList2= []
    for digit_str in str(p[2]):
     for digit in digit_str:
      sampleList.append(digit)
    #print(sampleList)  esto es para verificar la lista esta correcta  NO ES NECESARIO
#la otra
    for digit_st in str(p[6]):
     for digits in digit_st:
      sampleList2.append(digits)
    #print(sampleList2)  esto es para verificar la lista esta correcta  NO ES NECESARIO
    matrix1= matrix.Matrix([int(sampleList[0]),int(sampleList[1])],[int(sampleList2[0]),int(sampleList2[1])])
    print(matrix1)
    p[0]= (matrix1.det)


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
