import itertools
import sqlalchemy as db
import configparser
from sqlalchemy.sql import text
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt

def generarGraficos():

    #Credenciales
    config = configparser.ConfigParser()
    config.read('db_config.ini')
    host = config['postgres']['host']
    db_name = config['postgres']['db_name']
    port = config['postgres']['port']
    user = config['postgres']['user']
    pwd = config['postgres']['pass']

    #Conección
    engine = db.create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}')
    metadata = db.MetaData()
    connection = engine.connect()

    instancias = ["mscp42.txt"
                    ,"mscp52.txt"
                    ,"mscp62.txt"
                    ,"mscpa2.txt"
                    ,"mscpb2.txt"
                    ,"mscpc2.txt"
                    ,"mscpd2.txt"
                    ,"mscpnre2.txt"
                    ,"mscpnrf2.txt"
                    ,"mscpnrg2.txt"
                    ,"mscpnrh2.txt"
                    ]

    parametros = ["inercia"
                    ,"accelPer"
                    ,"accelBest"
                    ,"numParticulas"]

    permParam = []
    for i in range(len(parametros)):
        if i == 0: continue
        c = list(itertools.combinations(parametros,i))
        unq = list(set(c))
        permParam.extend(unq)

    permParam.append(["inercia"
                    ,"accelPer"
                    ,"accelBest"
                    ,"numParticulas"])

    sqlExperimentos = text(""" SELECT
                            id
                        FROM
                            datos_ejecucion
                        WHERE
                            parametros ILIKE :instancia
                        AND parametros ILIKE :parametros;""")

    sqlConvergencia = text("""SELECT
                                    fitness_mejor, 
                                    fitness_promedio, 
                                    fitness_mejor_iteracion
                                FROM
                                    datos_iteracion
                                where id_ejecucion = :idEjecucion
                                order by id
                            """)

    for instancia in instancias:
        instanciaStr = f"%{instancia}%"
        
        for parametro in permParam:
            resParametro = []
            parametroStr = '%["' + '", "'.join(parametro) + '"]%'
            param = {"instancia":instanciaStr,"parametros":parametroStr}
            #print(sql)
            #print(param)
            arrResult = connection.execute(sqlExperimentos,**param)
            for idEjecucion in arrResult:
                param = {"idEjecucion":idEjecucion[0]}
                convergencia = connection.execute(sqlConvergencia,**param)
                fitnessMejor = []
                fitnessMejorIteracion = []
                fitnessPromedio = []
                for fitnessArr in convergencia:
                    fitnessMejor.append(fitnessArr[0])
                    fitnessMejorIteracion.append(fitnessArr[2])
                    fitnessPromedio.append(fitnessArr[1])
                
                #crear grafico

                titulo = f"{instancia.replace('.txt','').replace('m','')} - {', '.join(parametro).replace('accelPer','c1').replace('accelBest','c2').replace('inercia','w').replace('numParticulas','np')}"
                indices = np.arange(1,len(fitnessMejor)+1)
                print(titulo)
                print(indices)

                plt.plot(indices, np.array(fitnessMejor), label = "Best Fitness")
                plt.plot(indices, np.array(fitnessMejorIteracion), label = "Best Fitness in iteration")
                plt.plot(indices, np.array(fitnessPromedio), label = "Average Fitness")
                plt.xlabel('Iteration')
                # Set the y axis label of the current axis.
                plt.ylabel('Fitness')
                # Set a title of the current axes.
                plt.title(titulo)
                # show a legend on the plot
                plt.legend()
                # Display a figure.
                filename = str(idEjecucion[0])+instancia.replace('.txt','') + '_'.join(parametro).replace('accelPer','c1').replace('accelBest','c2').replace('inercia','w').replace('numParticulas','np')
                
                plt.savefig(f'graficos/{filename}.eps', format='eps')
                plt.clf()
                #plt.show()
                #exit()


if __name__ == '__main__':
    generarGraficos()