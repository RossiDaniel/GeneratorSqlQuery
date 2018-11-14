import random
import string
from datetime import datetime
from interface import implements, Interface
from enum import Enum
import names

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
    def changeBound(self,sta,sto):
	if sto < sta : raise ValueError('il primo valore deve essere minore del secondo')
        self.start=sta
        self.stop=sto	
    def generate(self):
        return random.randint(self.start,self.stop)
    def clone(self):
        return IntGenerator()

class NameGenerator(implements(Generator)):
    def __init__(self, nm = []):
	self.name = nm
    def generate(self):
        if len(self.name) == 0: return names.get_first_name()
    def clone(self):
        return NameGenerator()

class SurnameGenerator(implements(Generator)):
    def __init__(self, nm = []):
	self.name = nm
    def generate(self):
        if len(self.name) == 0: return names.get_last_name()
    def clone(self):
        return SurnameGenerator()

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
        self.num='0123456789'
        self.size=sz
    def generate(self):
        return ''.join(random.choice(self.uc + self.lc) for _ in range(self.size))
    def clone(self):
        return StringGenerator()

class CodiceFiscaleGenerator(implements(Generator)):
    def __init__(self):
        self.uc=string.ascii_uppercase
        self.num='0123456789'
    def generate(self):
        p1= ''.join(random.choice(self.uc) for _ in range(6))
        p2= ''.join(random.choice(self.num) for _ in range(2))
        p3= ''.join(random.choice(self.uc))
        p4= ''.join(random.choice(self.num) for _ in range(2))
        p5= ''.join(random.choice(self.uc))
        p6= ''.join(random.choice(self.num) for _ in range(3))
        p7= ''.join(random.choice(self.uc))
        return p1+p2+p3+p4+p5+p6+p7
    def clone(self):
        return CodiceFiscaleGenerator()

class ArrayGenerator(implements(Generator)):
    def __init__(self):
        self.l=[]
        self.pre=''
    def addElements(self,elements):
        self.l+=elements
    def resetElements(self):
        self.l=[]
    def addPre(self,p):
        self.pre=p
    def generate(self):
        if len(self.l) == 0: raise ValueError('Lista vuota')
        return self.pre+str(random.choice(self.l))
    def clone(self):
        return ArrayGenerator()


class Attr:
    def __init__(self,nm,gn,pr):
        self.name=nm
        self.generator=gn
        self.primaryKey=pr
    def generate(self):
        return self.generator.generate()
    def __eq__(self,other):
        return self.name == other.name
    
class Type(Enum):
    VARCHAR = StringGenerator()
    INT = IntGenerator()
    DATE = DataGenerator()
    NAME = NameGenerator()
    SURNAME = SurnameGenerator()
    CODICEFISCALE = CodiceFiscaleGenerator()
    ARRAY = ArrayGenerator()

class Table: 
    def __init__(self,nm):
        self.name = nm
        self.attr = []
    def addAttribute(self,nm,gn,pr=False):
        for at in self.attr:
            if at.name == nm: raise ValueError('Non puoi inserire attributi con lo stesso nome')
        gen = gn.value.clone()
        self.attr.append(Attr(nm,gen,pr))
        return gen

    def generate(self,n=10):
        self.name_value = [i.name for i in self.attr]
        self.attr_value = []
        pr = []
        for i in range(n):
            c = 1
            value = []
            counter = 0
            while c != 0: 
                if counter >= 10 : raise ValueError('Non ci sono abbastanza valori per formare le PR per il numero di righe richieste')
                value = [j.generate() for j in self.attr]
                temp = []
                for j in range(len(self.attr)):
                    if self.attr[j].primaryKey == True:
                        temp.append(value[j])
                if(len(temp) == 0): c=0
                else: c = sum([j == temp for j in pr])
                counter=counter+1
            self.attr_value.append(value)
            pr.append(temp)

    def write(self,name='query'):
        if len(self.attr_value) == 0: raise ValueError('Devi prima richiamare il metodo generate')
        file = open(str(name)+".txt","w")
        for v in self.attr_value: 
            q =(upsert(self.name,self.name_value,v))
            file.write(str(q)+'\n')
        file.close()
