import os
import numpy as np
import datetime as dt
import configparser
import sqlalchemy as db
from sqlalchemy.sql import text
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.pyplot as plt
import json
import requests

import zlib
import pickle

def generarGraficosDiversidad(nombreAlgoritmo,engine,metadata,orden,directory):

    sql = """select 
            parametros_iteracion
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

    with engine.connect() as connection:
        for instancia in orden:
            estado = []
            facEvol = []
            
            instanciaStr = f"%{instancia}%"
            param = {"instancia":instanciaStr,"nomalg":nombreAlgoritmo}
            print(instanciaStr)
            
            arrResult = connection.execute(text(sql),**param)
            i = 0
            maxDiversidades = None
            porcXpl = []
            porcXpt = []
            for result in arrResult:
                fila = json.loads(result[0])
                # print(f"fila['PorcentajeExplor']: {fila['PorcentajeExplor']}")
                # print(f"fila['PorcentajeExplor']: {list(fila['PorcentajeExplor'].replace('[','').replace(']','').split(' '))}")
                PorcExplor = list(fila['PorcentajeExplor'].replace("[","").replace("]","").split(" ")) #[0, , , ,1,2,3,4,5]
                PorcExplor = np.array([float(item) for item in PorcExplor if item != ""])                
                porcXpl.append(PorcExplor)
                porcXpt.append(100 - PorcExplor)
                
            porcXpl = np.array(porcXpl)
            porcXpt = np.array(porcXpt)

            # print(f'porcXpl: {porcXpl.shape}')
            # print(f'porcXpt: {porcXpt.shape}')

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
                filename = f"{nombreAlgoritmo}-diversidad-{medidaDiv}-{instancia}"
                fig.savefig(f'{directory}/{filename}.png', format='png')
                plt.close()
                idx += 1
                #plt.show()
                #exit()