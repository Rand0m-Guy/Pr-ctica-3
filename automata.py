import nltk
import re

# AUTÓMATA IMPLEMENTADO

pila = ['Z'] # pila
s = ""

ws = [' ', '\t', '\n', '\v', '\f', '\r'] # caracteres en blanco de C

# FUNCIONES AUXILIARES

# Verifica si es simbolo valido en variable, verificando que el primer caracter no sea numerico
def simboloValidoVar(c, starting = False):
    if(starting):
        return c.isalpha() or c=='_'
    
    return c.isalpha() or c.isdigit() or c=='_'

# AUTOMATA DE PILA
def q0(i):
    if i >= len(s):
        return False
    if simboloValidoVar(s[i], True) and pila[-1] == 'Z':
        return V0(i + 1)
    if s[i] in ws and pila[-1] == 'Z':
        return E0(i + 1)
    
    return False

def V0(i):
    if i >= len(s):
        return False

    if simboloValidoVar(s[i]) and pila[-1] == 'Z':
        return V0(i+1)
    if s[i] in ws and pila[-1] == 'Z':
        pila.append('V')
        return E0(i + 1)
    if s[i] == '=' and pila[-1] == 'Z':
        return q1(i + 1)
    
    return False

def E0(i):
    if i >= len(s):
        return False

    if s[i] in ws and (pila[-1] == 'Z' or pila[-1] == 'V'):
        return E0(i + 1)
    if s[i] == '=' and pila[-1] == 'V':
        pila.pop()
        return q1(i + 1)
    if simboloValidoVar(s[i]) and pila[-1] == 'Z':
        return v0(i + 1)
    
    return False

def q1(i):
    if i >= len(s):
        return False

    if s[i] == '(' and pila[-1] == 'Z':
        pila.append('P')
        return O0(i + 1)
    if s[i] in ws and pila[-1] == 'Z':
        return E1(i + 1)
    if simboloValidoVar(s[i], True) and pila[-1] == 'Z':
        pila.append('V')
        return V1(i + 1)
    if s[i].isdigit() and pila[-1] == 'Z':
        pila.append('D')
        return N0(i + 1)
    
    return False

def E1(i):
    if i >= len(s):
        return False
    
    if s[i] == '(' and pila[-1] == 'Z':
        pila.append('P')
        return O0(i + 1)
    if s[i] in ws and pila[-1] == 'Z':
        return E1(i + 1)
    if simboloValidoVar(s[i], True) and pila[-1] == 'Z':
        pila.append('V')
        return V1(i + 1)
    if s[i].isdigit() and pila[-1] == 'Z':
        pila.append('D')
        return N0(i + 1)

    return False

def O0(i):
    if i >= len(s):
        return False

    if s[i] == '(' and pila[-1] == 'P':
        pila.append('P')
        return O0(i + 1)
    if simboloValidoVar(s[i], True) and pila[-1] == 'P':
        pila.append('V')
        return V1(i + 1)
    if s[i].isdigit() and pila[-1] == 'P':
        pila.append('D')
        return N0(i + 1)
    if s[i] in ws and pila[-1] == 'P':
        return E2(i + 1)
    
    # LARGA:
    if(pila[-1] == 'V' or pila[-1] == 'D'):
        if(s[i] == '+' or s[i] == '-' or s[i] == '*' or s[i] == '/' or s[i] == '%'):
            pila.pop()
            return O1(i + 1)
    if(pila[-1] == 'V' and s[i] == '='):
        pila.pop()
        return O1(i + 1)

    return False

def V1(i):
    if i >= len(s):
        return False

    if simboloValidoVar(s[i]):
        return V1(i + 1)
    if s[i] in ws and pila[-1] == 'V':
        return E2(i + 1)
    if s[i] == ')' and pila[-1] == 'V':
        pila.pop()
        return q4(i + 1)
    if s[i] == ';' and pila[-1] == 'V':
        pila.pop()
        return q2(i + 1)
    
    # LARGA:
    if(pila[-1] == 'V' or pila[-1] == 'D'):
        if(s[i] == '+' or s[i] == '-' or s[i] == '*' or s[i] == '/' or s[i] == '%'):
            pila.pop()
            return O1(i + 1)
    if(pila[-1] == 'V' and s[i] == '='):
        pila.pop()
        return O1(i + 1)

    return False

def N0(i):
    if i >= len(s):
        return False
    
    if s[i].isdigit():
        return N0(i + 1)
    if s[i] in ws and pila[-1] == 'D':
        return E2(i + 1)
    if s[i] == ')' and pila[-1] == 'D':
        pila.pop()
        return q4(i + 1)
    if s[i] == ';' and pila[-1] == 'D':
        pila.pop()
        return q2(i + 1)
    
    # LARGA:
    if(pila[-1] == 'V' or pila[-1] == 'D'):
        if(s[i] == '+' or s[i] == '-' or s[i] == '*' or s[i] == '/' or s[i] == '%'):
            pila.pop()
            return O1(i + 1)
    if(pila[-1] == 'V' and s[i] == '='):
        pila.pop()
        return O1(i + 1)
    
    return False

def E2(i):
    if i >= len(s):
        return False
    
    if s[i] in ws:
        return E2(i + 1)
    if s[i] == '(':
        pila.append('P')
        return O0(i + 1)
    if simboloValidoVar(s[i], True):
        pila.append('V')
        return V1(i + 1)
    if s[i].isdigit():
        pila.append('D')
        return N0(i + 1)
    if s[i] == ')' and (pila[-1] == 'P' or pila[-1] == 'D'):
        pila.pop()
        return q4(i + 1)
    
    # LARGA:
    if(pila[-1] == 'V' or pila[-1] == 'D'):
        if(s[i] == '+' or s[i] == '-' or s[i] == '*' or s[i] == '/' or s[i] == '%'):
            pila.pop()
            return O1(i + 1)
    if(pila[-1] == 'V' and s[i] == '='):
        pila.pop()
        return O1(i + 1)

    return False

def O1(i):
    if i >= len(s):
        return False

    if s[i] in ws:
        return E2(i + 1)
    if s[i] == '(':
        pila.append('P')
        return O0(i + 1)
    if simboloValidoVar(s[i], True):
        pila.append('V')
        return V1(i + 1)
    if s[i].isdigit():
        pila.append('D')
        return N0(i + 1)

    return False

def q4(i):
    if i >= len(s):
        return False

    if pila[-1] == 'P':
        pila.pop()
        return O2(i)

    return False

def O2(i):
    if i >= len(s):
        return False

    if s[i] == ')' and pila[-1] == 'P':
        pila.pop()
        return O2(i + 1)
    if s[i] in ws:
        return O2(i + 1)
    if s[i] == ';' and pila[-1] == 'Z':
        return q2(i + 1)

    if(s[i] == '+' or s[i] == '-' or s[i] == '*' or s[i] == '/' or s[i] == '%'):
        return O1(i + 1)

    return False

def q2(i):
    if i >= len(s):
        if pila[-1] == 'Z':
            pila.pop()
            return q3()
    return False

def q3():
    return len(pila) == 0

# Cadena a analizar
s = "VARIABLE_=(3)/((3*5)+_vasdAAA/(2%1)*var)-(2+3)*variable;"
print(s)
ans = q0(0)
if ans:
    print("La cadena sí pertenece a la gramática")
else:
    print("La cadena no pertenece a la gramatica")

if ans:

    # GENERACIÓN DEL ÁRBOL
    grammar = nltk.CFG.fromstring("""


    S -> Axiom
    Axiom -> VAR IGUAL OPERACION END
    OPERACION -> OPERACION OPERADOR OPERACION | PA OPERACION PC | VAR | NUMS | VAR IGUAL OPERACION  
    VAR ->  CARACTERES | VAR CARACTERES | VAR NUMS
    CARACTERES -> 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' | GB
    NUMS ->  '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | NUMS NUMS
    WSP -> ' ' | ''
    OPERADOR -> '+' | '-' | '*' | '/' | '%'
    IGUAL -> '='
    PA -> '('
    PC -> ')'
    GB -> '_'
    END -> ';'
    """)

    operacion = s


    caracteres=[]
    for i in operacion:
        if i==' ':
            pass
        else:
            caracteres.append(i)
    sentence=' '.join(caracteres)
    # print(sentence)
    parser = nltk.ChartParser(grammar)
    tokens = sentence.split()
    for tree in parser.parse(tokens):
        tree.pretty_print()
        break
