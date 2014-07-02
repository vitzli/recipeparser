# -*- coding: UTF-8 -*-

import ply.lex as lex
import re

DESCR_REGEX = re.compile('U\=(?P<unloc>[\w\.\|\s\:\'\"\(\)\xA7\/\!\-\,\#\&\?]+)\|\|L\=(?P<loc>[\w\.\|\s\:\'\"\(\)\xA7\/\!\-\,\#\&\?]*|())')

BOOLEAN_LUT = {'True': True, 'False': False}

reserved = {
'recipedumper:item': 'CITEM',
'recipedumper:shapelessore': 'CSHAPELESSORE',
'recipedumper:shapedore': 'CSHAPEDORE',
'recipedumper:shaped': 'CSHAPED',
'recipedumper:shapeless': 'CSHAPELESS',
'recipedumper:furnace': 'CFURNACE',
'recipedumper:oredict': 'COREDICT',
'recipedumper:fluid': 'CFLUID',
}

# List of token names.   This is always required
tokens = [
          'NONE',
          'LPAREN',
          'RPAREN',
          'ITEMDESCRIPTION',
          'TARGET',
          'SEPARATOR',
          'SIZE',
          'ITEMID',
          'ORENAME',
          'AMOUNT',
          'BOOLEAN',
] + list(reserved.values())

# Regular expression rules for simple tokens
t_ORENAME = r'\@[\w\s\.\|\:\-\(\)]+\w'
t_NONE = r'None'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_TARGET = r'\-\>'
t_SEPARATOR = r'\!'

# \w\.\|\s\:\'\"\(\)\xA7\/\!\-\,\#\&

precedence = (('left', 'FLUIDCODE', 'ITEMID'),
              ('left', 'TARGET', 'ORENAME'),
              ('left', 'ORENAME', 'LPAREN', 'RPAREN'),
              )

def t_ITEMDESCRIPTION(t):
    r'U\=[\w\.\|\s\:\'\"\(\)\xA7\/\!\-\,\#\&\d\?]+\|\|L\=[\w\.\|\s\:\'\"\(\)\xA7\/\!\-\,\#\&\d\?]*'
    matched = DESCR_REGEX.match(t.value)
    if matched is not None:
        t.value = (matched.group('unloc').strip(), matched.group('loc').strip())
        return t
    else:
        return t


def t_MODESEL(t):
    r'recipedumper\:\w+'
    t.type = reserved.get(t.value)
    return t


def t_SIZE(t):
    r'w=\d+,h=\d+'
    t.value = tuple([int(x) for x in re.findall('\d+', t.value)])
    return t


def t_AMOUNT(t):
    r'\,(\d+)'
    t.value = int(t.value.strip(','))
    return t


def t_BOOLEAN(t):
    r'(?:True|False)'
    t.value = BOOLEAN_LUT.get(t.value, None)
    return t


def t_ITEMID(t):
    r'(?:-?\d+\:?)+'
    t.value = tuple([int(x) for x in t.value.split(':')])
    return t

t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    # print(t)
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == '__main__':

#     TEST = 'recipedumper:oredict!@record->(2256:0,1)(2257:0,1)(2258:0,1)'
#     '(2259:0,1)(2260:0,1)(2261:0,1)(2262:0,1)(2263:0,1)(2264:0,1)'
#     '(2265:0,1)(2266:0,1)(2267:0,1)'

    # TEST = 'recipedumper:item!26095:0 U=item.backpack.thaumaturgeT1 L='
    # TEST = 'recipedumper:item!26094:7 U=item.miscResources L=Essence of False Life'
    # TEST = 'recipedumper:fluid!@minechem chemical: glycine->(225:-1)(6691600:10:0:295:1000)(False) U=fluid.Minechem Chemical: Glycine L=fluid.Minechem Chemical: Glycine'
    TEST = 'recipedumper:fluid!@minechem chemical: aspirin->(260:-1)(2377298:10:0:295:1000)(False) U=fluid.Minechem Chemical: Aspirin||L=fluid.Minechem Chemical: Aspirin'

    lexer.input(TEST)
    for tok in lexer:
        if not tok:
            break
        print(lexer.lexstate, ':', tok)
