# -*- coding: UTF-8 -*-

# import dataconfig
import ply
import ply.yacc as yacc
# import re
import pprint
from repmak_lex import tokens  # @UnusedImport


def p_main_modeoredict(p):
    'main : COREDICT SEPARATOR ORENAME TARGET ingredientlist'
    p[0] = {'mode': p[1], 'orename': p[3], 'target': p[5]}


def p_main_modeshapeless(p):
    '''main : CSHAPELESSORE SEPARATOR ingredientlist TARGET ingredient
            | CSHAPELESS SEPARATOR ingredientlist TARGET ingredient'''
    p[0] = {'mode': p[1], 'ingredients': p[3], 'target': p[5]}


def p_main_modeshaped(p):
    '''main : CSHAPED SEPARATOR recipesize ingredientlist TARGET ingredient
            | CSHAPEDORE SEPARATOR recipesize ingredientlist TARGET ingredient'''
    p[0] = {'mode': p[1], 'size': p[3], 'ingredients': p[4], 'target': p[6]}


def p_main_modeitem(p):
    'main : CITEM SEPARATOR ITEMID ITEMDESCRIPTION'
    p[0] = {'mode': p[1], 'itemid': p[3], 'description': p[4]}


def p_main_modefurnace(p):
    'main : CFURNACE SEPARATOR ingredient TARGET ingredient'
    p[0] = {'mode': p[1], 'source': p[3], 'target': p[5]}


def p_main_modeliquidreg(p):
    'main : CFLUID SEPARATOR ORENAME TARGET fluid fluid booleanst ITEMDESCRIPTION'
    p[0] = {'mode': p[1], 'fluid': p[3], 'ids': p[5], \
            'properties': p[6], 'is_gaseous': p[7], 'description': p[8]}


def p_booleanst_st(p):
    'booleanst : LPAREN BOOLEAN RPAREN'
    p[0] = p[2]


def p_fluid(p):
    'fluid : LPAREN ITEMID RPAREN'
    p[0] = p[2]


def p_ingredientlist_single(p):
    'ingredientlist : ingredient'
    p[0] = [p[1]]


def p_ingredientlist_multi(p):
    'ingredientlist : ingredientlist ingredient'
    p[0] = list()
    if isinstance(p[1], list):
        p[0].extend(p[1])
        p[0].append(p[2])
    else:
        p[0].append(p[1])
        p[0].append(p[2])


def p_ingredient_item(p):
    'ingredient : LPAREN ITEMID AMOUNT RPAREN'
    p[0] = {'itemid': p[2], 'amt': p[3]}


def p_ingredient_none(p):
    'ingredient : LPAREN NONE RPAREN'
    p[0] = None


def p_ingredient_orename(p):
    'ingredient : LPAREN ORENAME AMOUNT RPAREN'
    p[0] = {'orename': p[2], 'amt': p[3]}


def p_recipesize(p):
    'recipesize : LPAREN SIZE RPAREN'
    p[0] = p[2]


def p_error(p):
    pass


TEST = ['recipedumper:shaped!(w=3,h=1)(1869:2,1)(1869:2,1)(1869:2,1)->(1883:2,6)',
'recipedumper:shaped!(w=3,h=3)(None)(None)(1151:32767,1)(None)(1151:32767,1)(1151:32767,1)(1151:32767,1)(1151:32767,1)(1151:32767,1)->(1154:0,4)',
'recipedumper:shapeless!(20893:100,1)(7462:0,1)->(7462:0,1)',
'recipedumper:shapedore!(w=3,h=3)(1417:4,1)(None)(None)(1417:4,1)(1417:4,1)(None)(1417:4,1)(1417:4,1)(1417:4,1)->(1396:0,4)',
'recipedumper:shapedore!(w=3,h=3)(@plankWood,1)(@plankWood,1)(@plankWood,1)(None)(@stickWood,1)(None)(None)(@stickWood,1)(None)->(270:0,1)',
'recipedumper:shapedore!(w=3,h=3)(@cobblestone,1)(@cobblestone,1)(@cobblestone,1)(@cobblestone,1)(None)(@cobblestone,1)(@cobblestone,1)(@cobblestone,1)(@cobblestone,1)->(61:0,1)',
'recipedumper:shapedore!(w=3,h=3)(20:32767,1)(265:0,1)(20:32767,1)(20:32767,1)(None)(20:32767,1)(None)(@stickWood,1)(None)->(21534:0,1)',
'recipedumper:shapelessore!(2243:2,1)(@dyeOrange,1)->(2243:5,1)',
'recipedumper:shapelessore!(@dustMidasium,1)(@dustHaderoth,1)->(5357:0,1)',
'recipedumper:shapelessore!(@cellEmpty,1)(326:0,1)->(13086:0,1)',
'recipedumper:item!1:0 U=tile.stone||L=Stone',
'recipedumper:item!17586:47 U=item.backpack.big_white||L=Big White Backpack',
'recipedumper:oredict!@oreVulcanite->(1703:8,1)(2944:0,1)(2944:1,1)',
'recipedumper:oredict!@ingotPlastic->',
'recipedumper:oredict!@rubbleManganese->(13056:50,1)',
'recipedumper:oredict!@ingotLead->(9270:0,1)(8464:67,1)(19034:0,1)(12332:3,1)',
'recipedumper:fluid!@minechem chemical: aspirin->(260:-1)(2377298:10:0:295:1000)(False) U=fluid.Minechem Chemical: Aspirin||L=fluid.Minechem Chemical: Aspirin',
'recipedumper:fluid!@lithium->(329:-1)(256:10:0:295:1000)(False) U=fluid.Lithium||L=fluid.Lithium',
'recipedumper:furnace!(27160:0,1)->(27157:0,3)',
'recipedumper:furnace!(25911:0,1)->(25907:0,2)',
]

parser = yacc.yacc()

if __name__ == '__main__':
    for row in TEST:
        try:
            r = parser.parse(row)
            if r is not None:
                pprint.pprint(r)
        except:
            print('E: cannot parse message', row)
