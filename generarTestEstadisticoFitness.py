import sqlalchemy as db
import configparser
from sqlalchemy.sql import text
import pandas as pd
import numpy as np
import json
from scipy.stats import ranksums, mannwhitneyu
import csv

instancias = [
    'scp41.txt'
    ,'scp51.txt'
    ,'scp61.txt'
    ,'scpa1.txt'
    ,'scpb1.txt'
    ,'scpc1.txt'
    ,'scpd1.txt'
    ,'scpnre1.txt'
    ,'scpnrf1.txt'
    ,'scpnrg1.txt'
    ,'scpnrh1.txt']

config = configparser.ConfigParser()
config.read('db_config.ini')
host = config['postgres']['host']
db_name = config['postgres']['db_name']
port = config['postgres']['port']
user = config['postgres']['user']
pwd = config['postgres']['pass']

engine = db.create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}')
metadata = db.MetaData()

sql = text("""select 
        *
        from
        resultado_ejecucion
        where id_ejecucion in (
        select datos_ejecucion.id from datos_ejecucion 
        inner join resultado_ejecucion on datos_ejecucion.id = resultado_ejecucion.id_ejecucion
        where datos_ejecucion.parametros ILIKE :instancia
        and nombre_algoritmo = :nomalg
        order by resultado_ejecucion.fitness );""")

nombreAlgoritmo = ['GSO-AUTO','GSO-ORIGINAL']

with engine.connect() as connection:
    test = {'instancia':[],'hgso<gso':[],'gso<hgso':[]}
    for instancia in instancias:
        res = {}
        for alg in nombreAlgoritmo:
            instanciaStr = f"%{instancia}%"
            param = {"instancia":instanciaStr,"nomalg":alg}
            arrResult = connection.execute(sql,**param)
            if alg not in res: res[alg] = []
            for result in arrResult:
                res[alg].append(result[2])
        print(res[nombreAlgoritmo[0]])
        print(res[nombreAlgoritmo[1]])
        pValue1 = mannwhitneyu(res[nombreAlgoritmo[0]], res[nombreAlgoritmo[1]], alternative='less')[1]
        pValue2 = mannwhitneyu(res[nombreAlgoritmo[1]], res[nombreAlgoritmo[0]], alternative='less')[1]
        test['instancia'].append(instancia)
        if pValue1 < 0.05:
            test['hgso<gso'].append("\\textbf{" + "{:.3f}".format(pValue1) + "}")
        else:
            test['hgso<gso'].append("{:.3f}".format(pValue1))
        if pValue2 < 0.05:
            test['gso<hgso'].append("\\textbf{" + "{:.3f}".format(pValue2) + "}")
        else:
            test['gso<hgso'].append("{:.3f}".format(pValue2))
        
    df1 = pd.DataFrame(test)
    df1.index = df1.index+1
    df1.to_csv(f'testEstadistico.csv', sep='&', line_terminator='\\\\\n',  quoting=csv.QUOTE_NONE, escapechar=" ")

