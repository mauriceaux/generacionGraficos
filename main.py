import os
import datetime as dt
import configparser
import sqlalchemy as db
from sqlalchemy.sql import text
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.pyplot as plt


import generarResumen as gr
import graficoConvergencia as gc
import generarTex as gt
import graficosDiversidad as gd

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

orden = {
                'scp41.txt':[0,429]
                ,'scp51.txt':[1,253]
                ,'scp61.txt':[2,138]
                ,'scpa1.txt':[3,253]
                ,'scpb1.txt':[0,69]
                ,'scpc1.txt':[1,227]
                ,'scpd1.txt':[2,60]
                }

instancias = ["mscp41.txt"
                ,"mscp51.txt"
                ,"mscp61.txt"
                ,"mscpa1.txt"
                ,"mscpb1.txt"
                ,"mscpc1.txt"
                ,"mscpd1.txt"
                ,"mscpnre1.txt"
                ,"mscpnrf1.txt"
                ,"mscpnrg1.txt"
                ,"mscpnrh1.txt"
                ]

# tablasResumen = [
# ,['GWO_SCP_BCL1','GWO_SCP_MIR2','GWO_SCP_QL1','GWO_SCP_QL2','GWO_SCP_QL3']
# ,['SCA_SCP_BCL1','SCA_SCP_MIR2','SCA_SCP_QL1','SCA_SCP_QL2','SCA_SCP_QL3']
# ,['HHO_SCP_BCL1','HHO_SCP_MIR2','HHO_SCP_QL1','HHO_SCP_QL2','HHO_SCP_QL3']
# ,['WOA_SCP_BCL1','WOA_SCP_MIR2','WOA_SCP_QL1','WOA_SCP_QL2','WOA_SCP_QL3']
# ]
experimentos2 = [
# ['GWO_SCP_BCL1_CPU_S','GWO_SCP_MIR2_CPU_S','GWO_SCP_QL1_CPU_S','GWO_SCP_QL2_CPU_S','GWO_SCP_QL3_CPU_S','GWO_SCP_QL4_CPU_S','GWO_SCP_QL5_CPU_S']
['GWO_SCP_BCL1_CPU_C','GWO_SCP_MIR2_CPU_C','GWO_SCP_QL1_CPU_C','GWO_SCP_QL2_CPU_C','GWO_SCP_QL3_CPU_C','GWO_SCP_QL4_CPU_C','GWO_SCP_QL5_CPU_C']
# ,['SCA_SCP_BCL1_CPU_S','SCA_SCP_MIR2_CPU_S','SCA_SCP_QL1_CPU_S','SCA_SCP_QL2_CPU_S','SCA_SCP_QL3_CPU_S','SCA_SCP_QL4_CPU_S','SCA_SCP_QL5_CPU_S'] 
,['SCA_SCP_BCL1_CPU_C','SCA_SCP_MIR2_CPU_C','SCA_SCP_QL1_CPU_C','SCA_SCP_QL2_CPU_C','SCA_SCP_QL3_CPU_C','SCA_SCP_QL4_CPU_C','SCA_SCP_QL5_CPU_C']
# ,['HHO_SCP_BCL1_CPU_S','HHO_SCP_MIR2_CPU_S','HHO_SCP_QL1_CPU_S','HHO_SCP_QL2_CPU_S','HHO_SCP_QL3_CPU_S','HHO_SCP_QL4_CPU_S','HHO_SCP_QL5_CPU_S'] 
,['HHO_SCP_BCL1_CPU_C','HHO_SCP_MIR2_CPU_C','HHO_SCP_QL1_CPU_C','HHO_SCP_QL2_CPU_C','HHO_SCP_QL3_CPU_C','HHO_SCP_QL4_CPU_C','HHO_SCP_QL5_CPU_C']
# ,['WOA_SCP_BCL1_CPU_S','WOA_SCP_MIR2_CPU_S','WOA_SCP_QL1_CPU_S','WOA_SCP_QL2_CPU_S','WOA_SCP_QL3_CPU_S','WOA_SCP_QL4_CPU_S','WOA_SCP_QL5_CPU_S']
,['WOA_SCP_BCL1_CPU_C','WOA_SCP_MIR2_CPU_C','WOA_SCP_QL1_CPU_C','WOA_SCP_QL2_CPU_C','WOA_SCP_QL3_CPU_C','WOA_SCP_QL4_CPU_C','WOA_SCP_QL5_CPU_C']
]

experimentos =[['WOA_SCP_BCL1_CPU_C','WOA_SCP_MIR2_CPU_C','WOA_SCP_QL1_CPU_C','WOA_SCP_QL2_CPU_C','WOA_SCP_QL3_CPU_C','WOA_SCP_QL4_CPU_C','WOA_SCP_QL5_CPU_C']]

#Condicionales

#Para Generar Tablas resumen
generarTablasResumen = False
CompararConOtros = False

#Para Generar Gráficos de Convergencia
generarGraficosConvergencia = False
formatoGraficos = "png"

#Para generar Tex con gráficos de Convergencia
generarTexGraficosConvergencia = False
directoryTex = "archivoGeneradoTex.txt"
escaleColumnWidth = 0.5

#Para generar Gráficos de Diversidad
generarGraficosDiversidad = True





# Generar Tablas resumen
if generarTablasResumen == True:
    for i in range(len(experimentos)):
        print("\n")

        print("\\begin{table}[]")
        print(f'\\centering \\caption{{{experimentos[i][0].replace("_SCP_BCL1_CPU_S","-repair-Simple").replace("_SCP_BCL1_CPU_C","-repair-Compleja")}}}')
        print("\\resizebox{\\textwidth}{!}{")
        print("\\begin{tabular}{@{}ll|lll|lll|lll|lll|lll|lll|lll@{}}")
        print("\\toprule")
        print("\\multicolumn{1}{c}{}  & \\multicolumn{1}{c}{}")

        #for
        for j in range(len(experimentos[i])):
            print(f'& \\multicolumn{{3}}{{c}}{{{experimentos[i][j].replace("GWO_SCP_","").replace("SCA_SCP_","").replace("HHO_SCP_","").replace("WOA_SCP_","").replace("_","-")}}}')

        print("\\\\")
        print("\\multicolumn{1}{c}{Inst.}  & \\multicolumn{1}{c}{Opt.}")

        #for
        for j in range(len(experimentos[i])):
            print("& \\multicolumn{1}{c}{Best}  & \\multicolumn{1}{c}{Avg}  & \\multicolumn{1}{c}{RPD}")


        print("\\\\")
        print("\\midrule")

        gr.generarResumen(experimentos[i],CompararConOtros,engine,metadata,orden)

        print("\\bottomrule")
        print("\\end{tabular}  }")
        print("\\end{table}")

        print("\n")


#Generar gráficos de Convergencia
if generarGraficosConvergencia == True:
    for i in range(len(experimentos)):
        for j in range(len(experimentos[i])):
            #Crear directorio
            directory = experimentos[i][j].replace('_','-')
            try:
                os.mkdir(str(directory))
            except OSError:
                print("Ya existe el directorio %s " % directory)
            else:
                print("Se ha creado el directorio: %s " % directory)
            gc.generarGraficosConvergencia(experimentos[i][j],engine,metadata,instancias,orden,directory,formatoGraficos)


#Generar tex con gráficos de convergencia
if generarTexGraficosConvergencia == True:
    file = open(directoryTex, "w")
    for i in range(len(experimentos)):
        for j in range(len(experimentos[i])):
            for instancia in orden:
                instanciSinTxt = instancia.replace('.txt','')
                graficoConvergencia = experimentos[i][j].replace('_','-')
                gt.generarTex(file,graficoConvergencia,instanciSinTxt,escaleColumnWidth,formatoGraficos)
    file.close()
    print(".txt generado")


if generarGraficosDiversidad == True:
    for i in range(len(experimentos)):
        for j in range(len(experimentos[i])):
            directory = experimentos[i][j].replace('_','-')
            try:
                os.mkdir(str(directory))
            except OSError:
                print("Ya existe el directorio %s " % directory)
            else:
                print("Se ha creado el directorio: %s " % directory)

            gd.generarGraficosDiversidad(experimentos[i][j],engine,metadata,orden,directory)