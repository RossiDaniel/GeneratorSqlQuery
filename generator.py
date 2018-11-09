#!/usr/bin/env python

import pandas as pd
import random
import string
from datetime import datetime



def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



def random_date():
    year = random.randint(1990, 2017)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return datetime(year, month, day)


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


values = []
for i in range(1000):

    values.append([
    random.randint(1,10),
    id_generator(6),
    id_generator(6),
    random.randint(1,10),
    random_date().strftime('%Y-%m-%d'),
    random.randint(1,10),
    random.randint(1,10),
    random.randint(1,10),
    random.randint(1,10),
    id_generator(6),
    id_generator(6),
    random.randint(1,10),
    random.randint(1,10),
    random.randint(1,10),
    id_generator(6),
    random.randint(1,10),
    id_generator(6),
    random.randint(1,10),
    random.randint(1,10),
    random_date().strftime('%Y-%m-%d'),
    random_date().strftime('%Y-%m-%d')])

name= ['Category',
'Make',
'Model',
'YearModel',
'DateMatriculation',
'NumDoors',
'Numseats',
'ExternalColor',
'InternalColor',
'InternalMaterials',
'FuelType',
'EngineCylinder',
'HorsePower',
'EmissionClass',
'Transmission',
'Gears',
'Traction',
'Mileage',
'NumOwners',
'DateLastCheckup',
'DateNextRevision']

file = open("query.txt","w") 
for v in values:
    q =(upsert("Vehicle",name,v))
    file.write(str(q)+'\n')
file.close() 





