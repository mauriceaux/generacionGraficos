import os
import numpy as np
import datetime as dt
import configparser
import sqlalchemy as db
from sqlalchemy.sql import text
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.pyplot as plt

import zlib
import pickle
import diversidades

orden = {
        'scp41.txt':[0,429]
        ,'scp42.txt':[1,512]
        ,'scp43.txt':[2,516]
        ,'scp44.txt':[3,494]
        ,'scp45.txt':[0,512]
        ,'scp46.txt':[1,560]
        ,'scp47.txt':[2,430]
        ,'scp48.txt':[3,492]
        ,'scp49.txt':[0,641]
        ,'scp410.txt':[1,514]
        ,'scp51.txt':[2,253]
        ,'scp52.txt':[3,302]
        ,'scp53.txt':[0,226]
        ,'scp54.txt':[1,242]
        ,'scp55.txt':[2,211]
        ,'scp56.txt':[3,213]
        ,'scp57.txt':[0,293]
        ,'scp58.txt':[1,288]
        ,'scp59.txt':[2,279]
        ,'scp510.txt':[3,265]
        ,'scp61.txt':[0,138]
        ,'scp62.txt':[1,146]
        ,'scp63.txt':[2,145]
        ,'scp64.txt':[3,131]
        ,'scp65.txt':[0,161]
        ,'scpa1.txt':[1,253]
        ,'scpa2.txt':[2,252]
        ,'scpa3.txt':[3,232]
        ,'scpa4.txt':[0,234]
        ,'scpa5.txt':[1,236]
        ,'scpb1.txt':[2,69]
        ,'scpb2.txt':[3,76]
        ,'scpb3.txt':[0,80]
        ,'scpb4.txt':[1,79]
        ,'scpb5.txt':[2,72]
        ,'scpc1.txt':[3,227]
        ,'scpc2.txt':[0,219]
        ,'scpc3.txt':[1,243]
        ,'scpc4.txt':[2,219]
        ,'scpc5.txt':[3,215]
        ,'scpd1.txt':[0,60]
        ,'scpd2.txt':[1,66]
        ,'scpd3.txt':[2,72]
        ,'scpd4.txt':[3,62]
        ,'scpd5.txt':[0,61]
        ,'scpnre1.txt':[1,29]
        ,'scpnre2.txt':[2,30]
        ,'scpnre3.txt':[3,27]
        ,'scpnre4.txt':[0,28]
        ,'scpnre5.txt':[1,28]
        ,'scpnrf1.txt':[2,14]
        ,'scpnrf2.txt':[3,15]
        ,'scpnrf3.txt':[0,14]
        ,'scpnrf4.txt':[1,14]
        ,'scpnrf5.txt':[2,13]
        ,'scpnrg1.txt':[3,176]
        ,'scpnrg2.txt':[0,154]
        ,'scpnrg3.txt':[1,166]
        ,'scpnrg4.txt':[2,168]
        ,'scpnrg5.txt':[3,168]
        ,'scpnrh1.txt':[0,63]
        ,'scpnrh2.txt':[1,63]
        ,'scpnrh3.txt':[2,59]
        ,'scpnrh4.txt':[3,58]
        ,'scpnrh5.txt':[0,55]

        }

config = configparser.ConfigParser()
config.read('db_config.ini')
host = config['postgres']['host']
db_name = config['postgres']['db_name']
port = config['postgres']['port']
user = config['postgres']['user']
pwd = config['postgres']['pass']

engine = db.create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}')
metadata = db.MetaData()


nombreAlgoritmo = 'GSO-PAPER-4'

sql = """select 
        datos_internos
        from
        datos_iteracion
        where id_ejecucion = (
        select datos_ejecucion.id from datos_ejecucion 
        inner join resultado_ejecucion on datos_ejecucion.id = resultado_ejecucion.id_ejecucion
        where datos_ejecucion.parametros ILIKE :instancia
        and nombre_algoritmo = :nomalg
        order by resultado_ejecucion.fitness asc
        limit 1
        ) order by datos_iteracion.id asc"""
res = []
i=0

estadosDict = {
    'Exploration' : 0,
    'Exploitation' : 1,
    'Convergence' : 2,
    'Jump out' : 3

}
with engine.connect() as connection:
    for instancia in orden:
        estado = []
        facEvol = []
    #instancia = "scpa5."
        instanciaStr = f"%{instancia}%"
        param = {"instancia":instanciaStr,"nomalg":nombreAlgoritmo}
        print(instanciaStr)
        #print(sql)
        arrResult = connection.execute(text(sql),**param)
        i = 0
        maxDiversidades = None
        porcXpl = []
        porcXpt = []
        for result in arrResult:
            uncompressed = zlib.decompress(result[0])
            
            datosInternos = pickle.loads(uncompressed)

            d, maxDiversidades, PorcentajeExplor, PorcentajeExplot, state = diversidades.ObtenerDiversidadYEstado(datosInternos['solucionesBin'], maxDiversidades)
            porcXpl.append(PorcentajeExplor)
            porcXpt.append(PorcentajeExplot)
            
        # print(len(facEvol))
        # print(len(estado))
        # exit()
        porcXpl = np.array(porcXpl)
        porcXpt = np.array(porcXpt)

        medidasDiversidad = []
        medidasDiversidad.append('DimensionalHussain') #0
        medidasDiversidad.append('PesosDeInercia') #1
        medidasDiversidad.append('LeungGaoXu') #2
        medidasDiversidad.append('Entropica') #3
        medidasDiversidad.append('Hamming') #4
        medidasDiversidad.append('MomentoDeInercia') #5

        idx = 0

        for medidaDiv in medidasDiversidad:

            fig, ax = plt.subplots()
            fig.suptitle(f"{medidaDiv} % Exploration and Exploitation {instancia.replace('scp','').replace('nr','').replace('.txt','')}", fontsize=16)
            plt.plot(np.arange(porcXpl.shape[0]),porcXpl[:,idx])
            plt.plot(np.arange(porcXpt.shape[0]),porcXpt[:,idx])
            plt.legend(['% XPL', '% XPLT'], loc='upper left')
            filename = f"diversidad-{medidaDiv}-{instancia}"
            fig.savefig(f'graficosDiversidad/{filename}.eps', format='eps')
            plt.close()
            idx += 1
            #plt.show()
            #exit()