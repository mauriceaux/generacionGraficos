import pandas as pd
from os import listdir
from os.path import isfile, join
from scipy.stats import ranksums, mannwhitneyu
import matplotlib.pyplot as plt
import numpy as np


import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy.sql import text
import configparser
import sqlalchemy as db






def adjacent_values(vals, q1, q3):
    upper_adjacent_value = q3 + (q3 - q1) * 1.5
    upper_adjacent_value = np.clip(upper_adjacent_value, q3, vals[-1])

    lower_adjacent_value = q1 - (q3 - q1) * 1.5
    lower_adjacent_value = np.clip(lower_adjacent_value, vals[0], q1)
    return lower_adjacent_value, upper_adjacent_value


def set_axis_style(ax, labels):
    ax.get_xaxis().set_tick_params(direction='out')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks(np.arange(1, len(labels) + 1))
    ax.set_xticklabels(labels)
    ax.set_xlim(0.25, len(labels) + 0.75)
    ax.set_xlabel('Instance')


config = configparser.ConfigParser()
config.read('db_config.ini')
host = config['postgres']['host']
db_name = config['postgres']['db_name']
port = config['postgres']['port']
user = config['postgres']['user']
pwd = config['postgres']['pass']

engine = db.create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}')
metadata = db.MetaData()
connection = engine.connect()

instancias = [
    'scp41.txt'
    ,'scp42.txt'
    ,'scp43.txt'
    ,'scp44.txt'
    ,'scp45.txt'
    ,'scp46.txt'
    ,'scp47.txt'
    ,'scp48.txt'
    ,'scp49.txt'
    ,'scp410.txt'
    ,'scp51.txt'
    ,'scp52.txt'
    ,'scp53.txt'
    ,'scp54.txt'
    ,'scp55.txt'
    ,'scp56.txt'
    ,'scp57.txt'
    ,'scp58.txt'
    ,'scp59.txt'
    ,'scp510.txt'
    ,'scp61.txt'
    ,'scp62.txt'
    ,'scp63.txt'
    ,'scp64.txt'
    ,'scp65.txt'
    ,'scpa1.txt'
    ,'scpa2.txt'
    ,'scpa3.txt'
    ,'scpa4.txt'
    ,'scpa5.txt'
    ,'scpb1.txt'
    ,'scpb2.txt'
    ,'scpb3.txt'
    ,'scpb4.txt'
    ,'scpb5.txt'
    ,'scpc1.txt'
    ,'scpc2.txt'
    ,'scpc3.txt'
    ,'scpc4.txt'
    ,'scpc5.txt'
    ,'scpd1.txt'
    ,'scpd2.txt'
    ,'scpd3.txt'
    ,'scpd4.txt'
    ,'scpd5.txt'
    ,'scpnre1.txt'
    ,'scpnre2.txt'
    ,'scpnre3.txt'
    ,'scpnre4.txt'
    ,'scpnre5.txt'
    ,'scpnrf1.txt'
    ,'scpnrf2.txt'
    ,'scpnrf3.txt'
    ,'scpnrf4.txt'
    ,'scpnrf5.txt'
    ,'scpnrg1.txt'
    ,'scpnrg2.txt'
    ,'scpnrg3.txt'
    ,'scpnrg4.txt'
    ,'scpnrg5.txt'
    ,'scpnrh1.txt'
    ,'scpnrh2.txt'
    ,'scpnrh3.txt'
    ,'scpnrh4.txt'
    ,'scpnrh5.txt'

]

sql = text(""" SELECT 
                fitness 
            FROM 
                resultado_ejecucion 
            WHERE 
                id_ejecucion IN 
                (   SELECT
                        id
                    FROM
                        datos_ejecucion
                    WHERE
                        parametros ILIKE :instancia
                    AND nombre_algoritmo = :nomalg)
            ORDER BY 
                fitness ASC 
            LIMIT 
                31;""")

data = []

for instancia in instancias:
    #resInstancia = []
    instanciaStr = f"%{instancia}%"
    
    nombre = 'GSO-PAPER-4'
    param = {"instancia":instanciaStr,"nomalg":nombre}
    #print(sql)
    print(param)
    arrResult = connection.execute(sql,**param)
    dataInstancia = []
    for result in arrResult:
        dataInstancia.append(result[0])

    data.append(dataInstancia)



i = 0
labels = []
dataViolin = []
for dataInstancia in data:
    print(f"analizando instancia {instancias[i]}")
    labels.append(instancias[i].replace("scp","").replace("mscp","").replace(".txt","").replace(".csv",""))
    dataViolin.append(dataInstancia)
    if (i+1)%5 == 0:
        fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(9, 5), sharey=True)

        ax1.set_title('Fitness distribution')
        ax1.set_ylabel('Fitness')
        ax1.set_xlabel('Instance')
        ax1.violinplot(dataViolin)
        set_axis_style(ax1, labels)

        plt.subplots_adjust(bottom=0.15, wspace=0.05)
        filename = "_".join([instancia  for instancia in labels] )
        plt.savefig(f'graficos/violin/{filename}.eps', format='eps')

        labels = []
        dataViolin = []

    i += 1
    
    




