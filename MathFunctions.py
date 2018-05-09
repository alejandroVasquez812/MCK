from sympy import *


# method to derive equations based on variables passed to it
def derivative(eq, *args):

    if len(args) == 0:
        eq = diff(eq)
    for sym in args:
        eq = diff(eq, sym)
    return eq


# integrate definite/indefinite integrals
def integration(eq, *args):
    if len(args) == 0:
        eq = integrate(eq)
    for tups in args:
        eq = integrate(eq, tups)
    return eq


def summation(eq, lower, upper, sym):
    sumtotal = 0
    sumexpr = sympify(eq)
    while lower <= upper:
        newexpr = sumexpr.subs(sym, lower)
        sumtotal = sumtotal + newexpr
        lower += 1
    return sumtotal


# Method to evaluate limits; can evaluate from one side
def limits(eq, sym, sym0, side=None):
    if side is None:
        return limit(eq, sym, sym0)
    else:
        return limit(eq, sym, sym0, side)


def msolve(eq, sym):
    return solve(eq, sym)


# method to change equation format; Not working for some reason
def formateq(eq):
    if isinstance(eq, str):
        tired = str(eq)
        tired.replace("^", "**")
        return str(tired)


def reformateq(eq):
    if isinstance(eq, str):
        tired = str(eq)
        tired = tired.replace("**", "^")
        return tired
