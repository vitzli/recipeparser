# -*- coding: UTF-8 -*-

import dataconfig
from repmak_yacc import parser
# from repmak_lex import reserved
import pprint


class FluidProperties:
    def __init__(self):
        pass

    def __call__(self, properties):
        self.color = properties[0]
        self.density = properties[1]
        self.luminosity = properties[2]
        self.temp = properties[3]
        self.viscosity = properties[4]


class ModeSelector:

    def __init__(self):
        self.ore_lookup = dict()
        self.fluid_lookup = dict()
        self.modes = {'recipedumper:oredict': self.load_oredict,
                      'recipedumper:fluid': self.load_fluid,
                      }

    def __call__(self, itemdict):
        currentmode = itemdict.get('mode', None)
        if currentmode is not None and currentmode in self.modes.keys():
            self.modes[currentmode](itemdict)

    def load_oredict(self, oredict):
        ts_items = [x.get('itemid') for x in oredict['target']]
        self.ore_lookup[oredict['orename']] = ts_items
        for item in ts_items:
            self.ore_lookup[item] = oredict['orename']

    def load_fluid(self, fluiddict):
        self.fluid_lookup[fluiddict['fluid']] = fluiddict.get('properties')

    def getOreDictionary(self):
        return self.ore_lookup.items()

FILES = [dataconfig.ITEMS, dataconfig.OREDICT, dataconfig.RECIPES]

itemlist = list()

MS = ModeSelector()
P = FluidProperties()

fp = open(dataconfig.FLUID, mode='rt')

for line in fp:
    s = parser.parse(line.strip('\n'))
    if (s is not None):
        MS(s)
fp.close()

for k, v in MS.fluid_lookup.items():
    P(v)
    print(P.color)
