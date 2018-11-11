#!/usr/bin/envimport pandas as pd
import random
import string
from datetime import datetime
from interface import implements, Interface
from enum import Enum

def upsert(table, name,values):
    keys = ['%s' % k for k in name]
    values = ["'%s'" % v for v in values]
    sql = list()
    sql.append("INSERT INTO %s (" % table)
    sql.append(", ".join(keys))
    sql.append(") VALUES (")
    sql.append(", ".join(values))
    sql.append(");")
    return "".join(sql)

class Generator(Interface):

    def generate(self):
        pass

    def clone(self):
        pass

class IntGenerator(implements(Generator)):
    def __init__(self,sta=0,sto=100):
        self.start=sta
        self.stop=sto
    def generate(self):
        return random.randint(self.start,self.stop)
    def clone(self):
        return IntGenerator()

class DataGenerator(implements(Generator)):
    def __init__(self,sta=1980,sto=2018):
        self.start=sta
        self.stop=sto
    def generate(self):
        year = random.randint(self.start, self.stop)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return str(datetime(year, month, day))    
    def clone(self):
        return DataGenerator()

class StringGenerator(implements(Generator)):
    def __init__(self,sz=6):
        self.uc=string.ascii_uppercase
        self.lc=string.ascii_lowercase
        self.size=sz
    def generate(self):
        return ''.join(random.choice(self.uc + self.lc) for _ in range(self.size))
    def clone(self):
        return StringGenerator()

class Attr:
    def __init__(self,nm,gn,pr):
        self.name=nm
        self.generator=gn
        self.primaryKey=pr
    def generate(self):
        return self.generator.generate()
    
class Type(Enum):
    VARCHAR = StringGenerator()
    INT = IntGenerator()
    DATE = DataGenerator()

class Table:
    def __init__(self,nm):
        self.name = nm
        self.attr = []
    def addAttribute(self,nm,gn,pr=False):
        for at in self.attr:
            if at.name == nm: raise ValueError('Non puoi inserire attributi con lo stesso nome')
        gen=gn.value.clone()
        self.attr.append(Attr(nm,gen,pr))
        return gen
    def generate(self,n=10):
        self.name = [i.name for i in self.attr]
        self.value = [[i.generate() for i in self.attr] for _ in range(n)]
    def write(self,name='query'):
        if len(self.value) == 0: raise ValueError('Devi prima richiamare il metodo generate')
        file = open(str(name)+".txt","w")
        for v in self.value: 
            q =(upsert("Vehicle",self.name,v))
            file.write(str(q)+'\n')
        file.close()
