#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 04:24:34 2020

@author: christian
"""
import os
os.environ["CDF_LIB"] = "/home/christian/Desktop/cdf-dist-all/cdf37_1-dist/lib"
import pandas as pd
import datetime
from spacepy import pycdf
import csv
import datetime
import numpy as np

###############################################################################
#                         Arranco con los datos de GCR                        #
###############################################################################

indices_a = []

for i in range(0,20):
    indices_a.append(i * 8760)

for i in range(0,len(indices_a)):
    if i == 3 or i == 4 or i == 5 or i == 6:
        indices_a[i] = indices_a[i] + 24
    elif i == 7 or i == 8 or i == 9 or i == 10:
        indices_a[i] = indices_a[i] + 48
    elif i == 11 or i == 12 or i == 13 or i == 14:
        indices_a[i] = indices_a[i] + 72
    elif i == 15 or i == 16 or i == 17 or i == 18:
        indices_a[i] = indices_a[i] + 96
    elif i == 19 or i == 20:
        indices_a[i] = indices_a[i] + 96 + 24
    else:
        pass    

indices_a.append(indices_a[-1] + 1032)

añofor = [] #Genero la "lista" vacia
cosmiC = [] #Genero la "lista" vacia
añoC = [] #Genero la "lista" vacia
mesC = [] #Genero la "lista" vacia
diaC = [] #Genero la "lista" vacia
horaC= [] #Genero la "lista" vacia        

for i in range (1998,2018):
    añofor.append(str(i))
    
for i in range(0,len(añofor)):
    a = []
    archivo = open("/media/christian/Elements/tesis/datos/Neutron_Monitor_Data/"+añofor[i]+".txt","r") #Abro el archivo cuando arranca el evento
    for line in archivo.readlines(): #recorro todas las lineas del txt
        a.append(line) #a es una lista que tiene todas las lineas del archivo eventos (la fecha del inicio del evento)
    for j in range(0,len(a)):
            evento = a[j]
            añoC.append(float(evento[0:4])) #me quedo con los primeras 4 caracteres de a que corresponden al año de inicio del evento
            mesC.append(float(evento[5:7])) #me quedo con los caracteres de a que corresponden al mes del inicio del evento
            diaC.append(float(evento[8:10])) #me quedo con los caracteres de a que corresponden al dia inicial del evento
            horaC.append(float(evento[11:13]))
            cosmiC.append(float(evento[18:23]))
            archivo.close()

###############################################################################
#          Lo que viene ahora es todo lo que está en el código sirs           #
###############################################################################

df = pd.read_excel("/media/christian/Elements/tesis/datos/STEREO_Level3_SIR.xls", sheet_name = "Sheet2")

indices_A = []
indices_B = []
fecha_inicio_A = []
fecha_inicio_B = []
fecha_final_A = []
fecha_final_B = []

for i in range(len(df)):
    if df.loc[i][2] == 'A':
        indices_A.append(i)
        fecha_inicio_A.append(df.loc[i][3].split(' '))
        fecha_final_A.append(df.loc[i][4].split(' '))
    elif df.loc[i][2] == 'B':
        indices_B.append(i)
        fecha_inicio_B.append(df.loc[i][3].split(' '))
        fecha_final_B.append(df.loc[i][4].split(' '))        
        pass

###############################################################################
""" 
En este paso se va a chequear que las listas creadas anteriormente sean de 3
dimensiones, ya que se observa que algunos casos tienen 4 dimensiones producto que
la primera dimensión corresponde al año 
"""

borrar_fecha_inicio_A = []
borrar_fecha_final_A = []
borrar_fecha_inicio_B = []
borrar_fecha_final_B = []
    
for i in range(len(fecha_inicio_B)):
    if len(fecha_inicio_B[i]) == 4:
        borrar_fecha_inicio_B.append(i)
    else:
        pass
for i in range(len(fecha_final_B)):    
    if len(fecha_final_B[i]) == 4:
        borrar_fecha_final_B.append(i)
    else:
        pass

for i in range(len(fecha_final_A)):
    if len(fecha_inicio_A[i]) == 4:
        borrar_fecha_inicio_A.append(i)
    elif len(fecha_final_A[i]) == 4:
        borrar_fecha_final_A.append(i)

###############################################################################
"""
Se procede a borrar los datos innecesarios, que en este caso son los correspondientes
a los encontrados en el paso anterior
"""

for i in (borrar_fecha_inicio_B):
    del fecha_inicio_B[i][0]

for i in (borrar_fecha_final_B):
    del fecha_final_B[i][0]
    
for i in (borrar_fecha_inicio_A):
    del fecha_inicio_A[i][0]
    
for i in (borrar_fecha_final_A):
    del fecha_final_A[i][0]
    
###############################################################################
"""
Los eventos arrancan de 2007, lo que se hace en este paso es crear un vector asociado
a los años de los eventos y separar en otro vector el día del año en que ocurrieron
"""
dia_inicio_A = []
año_inicio_A = []
dia_fin_A = []
año_fin_A = []
año = 2007

for i in range(0,len(fecha_final_A)):
    dia_inicio_A.append(int(fecha_inicio_A[i][0])) 
    if i == 0:
        año_inicio_A.append(int(año))
    else:
        if int(fecha_inicio_A[i][0]) < int(fecha_inicio_A[i-1][0]):
            año = año + 1
            año_inicio_A.append(int(año))
        else:
            año_inicio_A.append(int(año))

año = 2007

for i in range(0,len(fecha_final_A)):
    dia_fin_A.append(int(fecha_final_A[i][0])) 
    if i == 0:
        año_fin_A.append(int(año))
    else:
        if int(fecha_final_A[i][0]) < int(fecha_final_A[i-1][0]):
            año = año + 1
            año_fin_A.append(int(año))
        else:
            año_fin_A.append(int(año))

###############################################################################
"""
En esta parte se asigna el día correspondiente a cada mes y el mes de incio y fin
de cada evento
"""

dia_inicio_A_limpio = []
mes_inicio_A = []
dia_fin_A_limpio = []
mes_fin_A = []

for i in range(0,len(dia_inicio_A)):
    if np.remainder(año_inicio_A[i],4) != 0:
        if dia_inicio_A[i] <= 31:
            dia_inicio_A_limpio.append(dia_inicio_A[i])
            mes_inicio_A.append(int(1))
        if dia_inicio_A[i] <= 59 and dia_inicio_A[i] > 31:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 31)
            mes_inicio_A.append(int(2))
        if dia_inicio_A[i] <= 90 and dia_inicio_A[i] > 59:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 59)
            mes_inicio_A.append(int(3))
        if dia_inicio_A[i] <= 120 and dia_inicio_A[i] > 90:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 90)
            mes_inicio_A.append(int(4))
        if dia_inicio_A[i] <= 151 and dia_inicio_A[i] > 120:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 120)
            mes_inicio_A.append(int(5))
        if dia_inicio_A[i] <= 181 and dia_inicio_A[i] > 151:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 151)
            mes_inicio_A.append(int(6))
        if dia_inicio_A[i] <= 212 and dia_inicio_A[i] > 181:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 181)
            mes_inicio_A.append(int(7))
        if dia_inicio_A[i] <= 243 and dia_inicio_A[i] > 212:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 212)
            mes_inicio_A.append(int(8))
        if dia_inicio_A[i] <= 273 and dia_inicio_A[i] > 243:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 243)
            mes_inicio_A.append(int(9))
        if dia_inicio_A[i] <= 304 and dia_inicio_A[i] > 273:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 273)
            mes_inicio_A.append(int(10))
        if dia_inicio_A[i] <= 334 and dia_inicio_A[i] > 304:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 304)
            mes_inicio_A.append(int(11))
        if dia_inicio_A[i] <= 365 and dia_inicio_A[i] > 334:
            dia_inicio_A_limpio.append(dia_inicio_A[i] -334)
            mes_inicio_A.append(int(12))
    else:
        if dia_inicio_A[i] <= 31:
            dia_inicio_A_limpio.append(dia_inicio_A[i])
            mes_inicio_A.append(int(1))
        if dia_inicio_A[i] <= 60 and dia_inicio_A[i] > 31:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 31)
            mes_inicio_A.append(int(2))
        if dia_inicio_A[i] <= 91 and dia_inicio_A[i] > 60:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 60)
            mes_inicio_A.append(int(3))
        if dia_inicio_A[i] <= 121 and dia_inicio_A[i] > 91:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 91)
            mes_inicio_A.append(int(4))
        if dia_inicio_A[i] <= 152 and dia_inicio_A[i] > 121:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 121)
            mes_inicio_A.append(int(5))
        if dia_inicio_A[i] <= 182 and dia_inicio_A[i] > 152:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 155)
            mes_inicio_A.append(int(6))
        if dia_inicio_A[i] <= 213 and dia_inicio_A[i] > 182:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 182)
            mes_inicio_A.append(int(7))
        if dia_inicio_A[i] <= 244 and dia_inicio_A[i] > 213:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 213)
            mes_inicio_A.append(int(8))
        if dia_inicio_A[i] <= 274 and dia_inicio_A[i] > 244:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 244)
            mes_inicio_A.append(int(9))
        if dia_inicio_A[i] <= 305 and dia_inicio_A[i] > 274:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 274)
            mes_inicio_A.append(int(10))
        if dia_inicio_A[i] <= 335 and dia_inicio_A[i] > 305:
            dia_inicio_A_limpio.append(dia_inicio_A[i] - 305)
            mes_inicio_A.append(int(11))
        if dia_inicio_A[i] <= 366 and dia_inicio_A[i] > 335:
            dia_inicio_A_limpio.append(dia_inicio_A[i] -335)
            mes_inicio_A.append(int(12))
            
            
for i in range(0,len(dia_fin_A)):
    if np.remainder(año_fin_A[i],4) != 0:
        if dia_fin_A[i] <= 31:
            dia_fin_A_limpio.append(dia_fin_A[i])
            mes_fin_A.append(int(1))
        if dia_fin_A[i] <= 59 and dia_fin_A[i] > 31:
            dia_fin_A_limpio.append(dia_fin_A[i] - 31)
            mes_fin_A.append(int(2))
        if dia_fin_A[i] <= 90 and dia_fin_A[i] > 59:
            dia_fin_A_limpio.append(dia_fin_A[i] - 59)
            mes_fin_A.append(int(3))
        if dia_fin_A[i] <= 120 and dia_fin_A[i] > 90:
            dia_fin_A_limpio.append(dia_fin_A[i] - 90)
            mes_fin_A.append(int(4))
        if dia_fin_A[i] <= 151 and dia_fin_A[i] > 120:
            dia_fin_A_limpio.append(dia_fin_A[i] - 120)
            mes_fin_A.append(int(5))
        if dia_fin_A[i] <= 181 and dia_fin_A[i] > 151:
            dia_fin_A_limpio.append(dia_fin_A[i] - 151)
            mes_fin_A.append(int(6))
        if dia_fin_A[i] <= 212 and dia_fin_A[i] > 181:
            dia_fin_A_limpio.append(dia_fin_A[i] - 181)
            mes_fin_A.append(int(7))
        if dia_fin_A[i] <= 243 and dia_fin_A[i] > 212:
            dia_fin_A_limpio.append(dia_fin_A[i] - 212)
            mes_fin_A.append(int(8))
        if dia_fin_A[i] <= 273 and dia_fin_A[i] > 243:
            dia_fin_A_limpio.append(dia_fin_A[i] - 243)
            mes_fin_A.append(int(9))
        if dia_fin_A[i] <= 304 and dia_fin_A[i] > 273:
            dia_fin_A_limpio.append(dia_fin_A[i] - 273)
            mes_fin_A.append(int(10))
        if dia_fin_A[i] <= 334 and dia_fin_A[i] > 304:
            dia_fin_A_limpio.append(dia_fin_A[i] - 304)
            mes_fin_A.append(int(11))
        if dia_fin_A[i] <= 365 and dia_fin_A[i] > 334:
            dia_fin_A_limpio.append(dia_fin_A[i] -334)
            mes_fin_A.append(int(12))
    else:
        if dia_fin_A[i] <= 31:
            dia_fin_A_limpio.append(dia_fin_A[i])
            mes_fin_A.append(int(1))
        if dia_fin_A[i] <= 60 and dia_fin_A[i] > 31:
            dia_fin_A_limpio.append(dia_fin_A[i] - 31)
            mes_fin_A.append(int(2))
        if dia_fin_A[i] <= 91 and dia_fin_A[i] > 60:
            dia_fin_A_limpio.append(dia_fin_A[i] - 60)
            mes_fin_A.append(int(3))
        if dia_fin_A[i] <= 121 and dia_fin_A[i] > 91:
            dia_fin_A_limpio.append(dia_fin_A[i] - 91)
            mes_fin_A.append(int(4))
        if dia_fin_A[i] <= 152 and dia_fin_A[i] > 121:
            dia_fin_A_limpio.append(dia_fin_A[i] - 121)
            mes_fin_A.append(int(5))
        if dia_fin_A[i] <= 182 and dia_fin_A[i] > 152:
            dia_fin_A_limpio.append(dia_fin_A[i] - 155)
            mes_fin_A.append(int(6))
        if dia_fin_A[i] <= 213 and dia_fin_A[i] > 182:
            dia_fin_A_limpio.append(dia_fin_A[i] - 182)
            mes_fin_A.append(int(7))
        if dia_fin_A[i] <= 244 and dia_fin_A[i] > 213:
            dia_fin_A_limpio.append(dia_fin_A[i] - 213)
            mes_fin_A.append(int(8))
        if dia_fin_A[i] <= 274 and dia_fin_A[i] > 244:
            dia_fin_A_limpio.append(dia_fin_A[i] - 244)
            mes_fin_A.append(int(9))
        if dia_fin_A[i] <= 305 and dia_fin_A[i] > 274:
            dia_fin_A_limpio.append(dia_fin_A[i] - 274)
            mes_fin_A.append(int(10))
        if dia_fin_A[i] <= 335 and dia_fin_A[i] > 305:
            dia_fin_A_limpio.append(dia_fin_A[i] - 305)
            mes_fin_A.append(int(11))
        if dia_fin_A[i] <= 366 and dia_fin_A[i] > 335:
            dia_fin_A_limpio.append(dia_fin_A[i] -335)
            mes_fin_A.append(int(12))
            
###############################################################################
"""
En esta parte se crean los vectores hora y minuto de los eventos
"""

horario_inicio_A = []
hora_inicio_A = []
minuto_inicio_A = []

for i in range(0,len(fecha_final_A)):
    horario_inicio_A.append(fecha_inicio_A[i][2].split(':'))
    
for i in range(0,len(fecha_final_A)):
    hora_inicio_A.append(int(horario_inicio_A[i][0]))  
    minuto_inicio_A.append(round(float(horario_inicio_A[i][1])))
    
horario_fin_A = []
hora_fin_A = []
minuto_fin_A = []

for i in range(0,len(fecha_final_A)):
    horario_fin_A.append(fecha_final_A[i][2].split(':'))
    
for i in range(0,len(fecha_final_A)):
    hora_fin_A.append(int(horario_fin_A[i][0]))
    minuto_fin_A.append(round(float(horario_fin_A[i][1])))

###############################################################################
#       En esta parte se crea el vector inico del SIR, final del SIR, la      #
#       duración del SIR, #el inicio del dominio y el final del dominio       #    
###############################################################################

for i in range(0,len(año_fin_A)):
    inicio_sir_datetime = datetime.datetime(año_inicio_A[i], mes_inicio_A[i], dia_inicio_A_limpio[i], hora_inicio_A[i], minuto_inicio_A[i])
    fin_sir_datetime = datetime.datetime(año_fin_A[i], mes_fin_A[i], dia_fin_A_limpio[i], hora_fin_A[i], minuto_fin_A[i])
    delta_t = fin_sir_datetime - inicio_sir_datetime
    contador = int(delta_t.total_seconds()/(60*24*60)) + 1
    
    inicio_dominio = inicio_sir_datetime - delta_t
    fin_dominio = fin_sir_datetime + delta_t

###############################################################################
#En este paso se crean los vectores año, mes, día y hora que se van a plotear #
#se utiliza el vector contador que corresponde a la longitud del evento como  #
#número entero (días que dura el evento) y luego se toma de dominio esa canti-#
#dad anterior y esa cantidad posterior. Se va a arrancar del -contador y se va# 
#                   a llegar a 2 veces el contador +1                         #
###############################################################################

for i in range(0,len(dia_fin_A_limpio)): # len(dia_fin_A_limpio)

    cosmic_ray = []
    vr_año =[] #Genero la "lista" vacia
    vr_mes = [] #Genero la "lista" vacia
    vr_dia = [] #Genero la "lista" vacia
    vr_hora = [] #Genero la "lista" vacia    
    
    inicio_sir_datetime = datetime.datetime(año_inicio_A[i], mes_inicio_A[i], dia_inicio_A_limpio[i], hora_inicio_A[i], minuto_inicio_A[i])
    fin_sir_datetime = datetime.datetime(año_fin_A[i], mes_fin_A[i], dia_fin_A_limpio[i], hora_fin_A[i], minuto_fin_A[i])
    delta_t = fin_sir_datetime - inicio_sir_datetime
    contador = int(delta_t.total_seconds()/(60*24*60)) + 1
    
    inicio_dominio = inicio_sir_datetime - delta_t
    fin_dominio = fin_sir_datetime + delta_t
    
    if dia_inicio_A_limpio[i] - contador >= 10 and (mes_inicio_A[i] < 10):
        for x in range(0,24):
            vr_hora.append(x)
            vr_año.append(año_inicio_A[i])
            vr_mes.append(mes_inicio_A[i])
            vr_dia.append(dia_inicio_A_limpio[i] - contador)
    elif dia_inicio_A_limpio[i] - contador >= 10 and (mes_inicio_A[i] >= 10):
        for x in range(0,24):
            vr_hora.append(x)
            vr_año.append(año_inicio_A[i])
            vr_mes.append(mes_inicio_A[i])
            vr_dia.append(dia_inicio_A_limpio[i] - contador)
    elif dia_inicio_A_limpio[i] - contador < 10 and dia_inicio_A_limpio[i] - contador >= 1 and (mes_inicio_A[i] < 10):
        for x in range(0,24):
            vr_hora.append(x)
            vr_año.append(año_inicio_A[i])
            vr_mes.append(mes_inicio_A[i])
            vr_dia.append(dia_inicio_A_limpio[i] - contador)
    elif dia_inicio_A_limpio[i] - contador < 10 and dia_inicio_A_limpio[i] - contador >= 1 and (mes_inicio_A[i] >= 10):
        for x in range(0,24):
            vr_hora.append(x)
            vr_año.append(año_inicio_A[i])
            vr_mes.append(mes_inicio_A[i])
            vr_dia.append(dia_inicio_A_limpio[i] - contador)
    elif dia_inicio_A_limpio[i] - contador < 1 and (mes_inicio_A[i] == 2 or mes_inicio_A[i] == 4 or mes_inicio_A[i] == 6 or mes_inicio_A[i] == 8 or mes_inicio_A[i] == 9):
        for x in range(0,24):
            vr_hora.append(x)
            vr_año.append(año_inicio_A[i])
            vr_mes.append(mes_inicio_A[i] - 1)
            vr_dia.append(dia_inicio_A_limpio[i] - contador + 31)
    elif dia_inicio_A_limpio[i] - contador < 1 and (mes_inicio_A[i] == 5 or mes_inicio_A[i] == 7 or mes_inicio_A[i] == 10):
        for x in range(0,24):
            vr_hora.append(x)
            vr_año.append(año_inicio_A[i])
            vr_mes.append(mes_inicio_A[i] - 1)
            vr_dia.append(dia_inicio_A_limpio[i] - contador + 30)
    elif dia_inicio_A_limpio[i] - contador < 1 and mes_inicio_A[i] == 11:
        for x in range(0,24):
            vr_hora.append(x)
            vr_año.append(año_inicio_A[i])
            vr_mes.append(mes_inicio_A[i] - 1)
            vr_dia.append(dia_inicio_A_limpio[i] - contador + 31)
    elif dia_inicio_A_limpio[i] - contador < 1 and mes_inicio_A[i] == 12:
        for x in range(0,24):
            vr_hora.append(x)
            vr_año.append(año_inicio_A[i])
            vr_mes.append(mes_inicio_A[i] - 1)
            vr_dia.append(dia_inicio_A_limpio[i] - contador + 30)
    elif dia_inicio_A_limpio[i] - contador < 1 and mes_inicio_A[i] == 3 and np.remainder(año_inicio_A[i],4) != 0:
        for x in range(0,24):
            vr_hora.append(x)
            vr_año.append(año_inicio_A[i])
            vr_mes.append(mes_inicio_A[i] - 1)
            vr_dia.append(dia_inicio_A_limpio[i] - contador + 28)
    elif dia_inicio_A_limpio[i] - contador < 1 and mes_inicio_A[i] == 3 and np.remainder(año_inicio_A[i],4) == 0:
        for x in range(0,24):
            vr_hora.append(x)
            vr_año.append(año_inicio_A[i])
            vr_mes.append(mes_inicio_A[i] - 1)
            vr_dia.append(dia_inicio_A_limpio[i] - contador + 29)
    elif dia_inicio_A_limpio[i] - contador < 1 and mes_inicio_A[i] == 1:
        for x in range(0,24):
            vr_hora.append(x)
            vr_año.append(año_inicio_A[i] - 1)
            vr_mes.append(12)
            vr_dia.append(dia_inicio_A_limpio[i] - contador + 31)
            
    for j in range(-contador + 1, contador * 2 + 1):
        if j < 0:
            if dia_inicio_A_limpio[i] + j >= 10 and (mes_inicio_A[i] < 10):
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(mes_inicio_A[i])
                    vr_dia.append(dia_inicio_A_limpio[i] + j)
            elif dia_inicio_A_limpio[i] + j >= 10 and (mes_inicio_A[i] >= 10):
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(mes_inicio_A[i])
                    vr_dia.append(dia_inicio_A_limpio[i] + j)
            elif dia_inicio_A_limpio[i] + j < 10 and dia_inicio_A_limpio[i] + j >= 1 and (mes_inicio_A[i] < 10):
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(mes_inicio_A[i])
                    vr_dia.append(dia_inicio_A_limpio[i] + j)
            elif dia_inicio_A_limpio[i] + j < 10 and dia_inicio_A_limpio[i] + j >= 1 and (mes_inicio_A[i] >= 10):
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(mes_inicio_A[i])
                    vr_dia.append(dia_inicio_A_limpio[i] + j)
            elif dia_inicio_A_limpio[i] + j < 1 and (mes_inicio_A[i] == 2 or mes_inicio_A[i] == 4 or mes_inicio_A[i] == 6 or mes_inicio_A[i] == 8 or mes_inicio_A[i] == 9):
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(mes_inicio_A[i] - 1)
                    vr_dia.append(dia_inicio_A_limpio[i] + j + 31)
            elif dia_inicio_A_limpio[i] + j < 1 and (mes_inicio_A[i] == 5 or mes_inicio_A[i] == 7 or mes_inicio_A[i] == 10):
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(mes_inicio_A[i] - 1)
                    vr_dia.append(dia_inicio_A_limpio[i] + j + 30)
            elif dia_inicio_A_limpio[i] + j < 1 and mes_inicio_A[i] == 11:
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(mes_inicio_A[i] - 1)
                    vr_dia.append(dia_inicio_A_limpio[i] + j + 31)
            elif dia_inicio_A_limpio[i] + j < 1 and mes_inicio_A[i] == 12:
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(mes_inicio_A[i] - 1)
                    vr_dia.append(dia_inicio_A_limpio[i] + j + 30)
            elif dia_inicio_A_limpio[i] + j < 1 and mes_inicio_A[i] == 3 and np.remainder(año_inicio_A[i],4) != 0:
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(mes_inicio_A[i] - 1)
                    vr_dia.append(dia_inicio_A_limpio[i] + j + 28)
            elif dia_inicio_A_limpio[i] + j < 1 and mes_inicio_A[i] == 3 and np.remainder(año_inicio_A[i],4) == 0:
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(mes_inicio_A[i] - 1)
                    vr_dia.append(dia_inicio_A_limpio[i] + j + 29)
            elif dia_inicio_A_limpio[i] + j < 1 and mes_inicio_A[i] == 1:
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i] - 1)
                    vr_mes.append(12)
                    vr_dia.append(dia_inicio_A_limpio[i] + j + 31)

        elif j == 0:
            for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(mes_inicio_A[i])
                    vr_dia.append(dia_inicio_A_limpio[i])

        else:
            if dia_inicio_A_limpio[i] + j == 32 and (mes_inicio_A[i] == 1 or mes_inicio_A[i] == 3 or mes_inicio_A[i] == 5 or mes_inicio_A[i] == 7 or mes_inicio_A[i] == 8):
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(mes_inicio_A[i] + 1)
                    vr_dia.append(1)
            elif dia_inicio_A_limpio[i] + j == 31 and (mes_inicio_A[i] == 4 or mes_inicio_A[i] == 6):
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(mes_inicio_A[i] + 1)
                    vr_dia.append(1)
            elif dia_inicio_A_limpio[i] + j == 32 and mes_inicio_A[i] == 10:
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(mes_inicio_A[i] + 1)
                    vr_dia.append(1)
            elif dia_inicio_A_limpio[i] + j == 31 and (mes_inicio_A[i] == 9 or mes_inicio_A[i] == 11):
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(mes_inicio_A[i] + 1)
                    vr_dia.append(1)
            elif dia_inicio_A_limpio[i] + j == 32 and mes_inicio_A[i] == 12:
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i] + 1)
                    vr_mes.append(1)
                    vr_dia.append(1)
            elif dia_inicio_A_limpio[i] + j == 29 and mes_inicio_A[i] == 2 and np.remainder(año_inicio_A[i],4) != 0:
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(3)
                    vr_dia.append(1)
            elif dia_inicio_A_limpio[i] + j == 30 and mes_inicio_A[i] == 2 and np.remainder(año_inicio_A[i],4) == 0:
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(3)
                    vr_dia.append(1)
            elif dia_inicio_A_limpio[i] + j < 10 and (mes_inicio_A[i] == 1 or mes_inicio_A[i] == 3 or mes_inicio_A[i] == 5 or mes_inicio_A[i] == 7 or mes_inicio_A[i] == 8):
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(mes_inicio_A[i])
                    vr_dia.append(dia_inicio_A_limpio[i]+j)
            elif dia_inicio_A_limpio[i] + j < 32 and dia_inicio_A_limpio[i] + j >= 10 and (mes_inicio_A[i] == 1 or mes_inicio_A[i] == 3 or mes_inicio_A[i] == 5 or mes_inicio_A[i] == 7 or mes_inicio_A[i] == 8):
                for x in range(0,24):
                    vr_hora.append(x)
                    vr_año.append(año_inicio_A[i])
                    vr_mes.append(mes_inicio_A[i])
                    vr_dia.append(dia_inicio_A_limpio[i]+j)
            elif dia_inicio_A_limpio[i] + j < 31 and (mes_inicio_A[i] == 4 or mes_inicio_A[i] == 6 or mes_inicio_A[i] == 9):
                if dia_inicio_A_limpio[i] + j < 10:
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i])
                        vr_dia.append(dia_inicio_A_limpio[i]+j)
                elif dia_inicio_A_limpio[i] + j >= 10:
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i])
                        vr_dia.append(dia_inicio_A_limpio[i]+j)
            elif dia_inicio_A_limpio[i] + j < 32 and mes_inicio_A[i] == 10:
                if dia_inicio_A_limpio[i] + j < 10:
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i])
                        vr_dia.append(dia_inicio_A_limpio[i]+j)
                elif dia_inicio_A_limpio[i] + j >= 10:
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i])
                        vr_dia.append(dia_inicio_A_limpio[i]+j)
            elif dia_inicio_A_limpio[i] + j < 31 and (mes_inicio_A[i] == 11):
                if dia_inicio_A_limpio[i] + j < 10:
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i])
                        vr_dia.append(dia_inicio_A_limpio[i]+j)
                elif dia_inicio_A_limpio[i] + j >= 10:
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i])
                        vr_dia.append(dia_inicio_A_limpio[i]+j)
            elif dia_inicio_A_limpio[i] + j < 32 and mes_inicio_A[i] == 12:
                if dia_inicio_A_limpio[i] + j < 10:
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i])
                        vr_dia.append(dia_inicio_A_limpio[i]+j)
                elif dia_inicio_A_limpio[i] + j >= 10:
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i])
                        vr_dia.append(dia_inicio_A_limpio[i]+j)
            elif dia_inicio_A_limpio[i] + j < 29 and mes_inicio_A[i] == 2 and np.remainder(año_inicio_A[i],4) != 0:
                if dia_inicio_A_limpio[i] + j < 10:                        
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(2)
                        vr_dia.append(dia_inicio_A_limpio[i]+j)
                elif dia_inicio_A_limpio[i] + j >= 10:                        
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(2)
                        vr_dia.append(dia_inicio_A_limpio[i]+j)
            elif dia_inicio_A_limpio[i] + j < 30 and mes_inicio_A[i] == 2 and np.remainder(año_inicio_A[i],4) == 0:
                if dia_inicio_A_limpio[i] + j < 10:                        
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(2)
                        vr_dia.append(dia_inicio_A_limpio[i]+j)
                elif dia_inicio_A_limpio[i] + j >= 10:                        
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(2)
                        vr_dia.append(dia_inicio_A_limpio[i]+j)
            elif dia_inicio_A_limpio[i] + j > 32 and (mes_inicio_A[i] == 1 or mes_inicio_A[i] == 3 or mes_inicio_A[i] == 5 or mes_inicio_A[i] == 7 or mes_inicio_A[i] == 8):
                for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i] + 1)
                        vr_dia.append(dia_inicio_A_limpio[i] + j - 31)
            elif dia_inicio_A_limpio[i] + j > 31 and (mes_inicio_A[i] == 4 or mes_inicio_A[i] == 6):                    
                for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i] + 1)
                        vr_dia.append(dia_inicio_A_limpio[i] + j - 30)
            elif dia_inicio_A_limpio[i] + j > 32 and mes_inicio_A[i] == 10:                    
                for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i] + 1)
                        vr_dia.append(dia_inicio_A_limpio[i] + j - 31)
            elif dia_inicio_A_limpio[i] + j > 31 and (mes_inicio_A[i] == 9 or mes_inicio_A[i] == 11):
                for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i] + 1)
                        vr_dia.append(dia_inicio_A_limpio[i] + j - 30)
            elif dia_inicio_A_limpio[i] + j > 32 and mes_inicio_A[i] == 12:                    
                for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i] + 1)
                        vr_mes.append(1)
                        vr_dia.append(dia_inicio_A_limpio[i] + j - 31)
            elif dia_inicio_A_limpio[i] + j > 29 and mes_inicio_A[i] == 2 and np.remainder(año_inicio_A[i],4) != 0:                    
                for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(3)
                        vr_dia.append(dia_inicio_A_limpio[i] + j - 28)
            elif dia_inicio_A_limpio[i] + j > 30 and mes_inicio_A[i] == 2 and np.remainder(año_inicio_A[i],4) == 0:
                for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(3)
                        vr_dia.append(dia_inicio_A_limpio[i] + j - 29)
                        
    for l in range(0,len(vr_año)):        
        if vr_año[0] == 1998:
            for k in range(indices_a[0],indices_a[1] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
        if vr_año[0] == 1999:
            for k in range(indices_a[1] - 168 ,indices_a[2] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
        if vr_año[0] == 2000:
            for k in range(indices_a[2] - 168 ,indices_a[3] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
        if vr_año[0] == 2001:
            for k in range(indices_a[3] - 168 ,indices_a[4] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
        if vr_año[0] == 2002:
            for k in range(indices_a[4] - 168 ,indices_a[5] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
        if vr_año[0] == 2003:
            for k in range(indices_a[5] - 168 ,indices_a[6] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
        if vr_año[0] == 2004:
            for k in range(indices_a[6] - 168 ,indices_a[7] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass                
        if vr_año[0] == 2005:
            for k in range(indices_a[7] - 168 ,indices_a[8] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
        if vr_año[0] == 2006:
            for k in range(indices_a[8] - 168 ,indices_a[9] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
        if vr_año[0] == 2007:
            for k in range(indices_a[9] - 168 ,indices_a[10] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
        if vr_año[0] == 2008:
            for k in range(indices_a[10] - 168 ,indices_a[11] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
        if vr_año[0] == 2009:
            for k in range(indices_a[11] - 168 ,indices_a[12] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
        if vr_año[0] == 2010:
            for k in range(indices_a[12] - 168 ,indices_a[13] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
        if vr_año[0] == 2011:
            for k in range(indices_a[13] - 168 ,indices_a[14] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
        if vr_año[0] == 2012:
            for k in range(indices_a[14] - 168 ,indices_a[15] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
        if vr_año[0] == 2013:
            for k in range(indices_a[15] - 168 ,indices_a[16] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
        if vr_año[0] == 2014:
            for k in range(indices_a[16] - 168 ,indices_a[17] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
        if vr_año[0] == 2015:
            for k in range(indices_a[17] - 168 ,indices_a[18] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
        if vr_año[0] == 2016:
            for k in range(indices_a[18] - 168 ,indices_a[19] + 168):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
        if vr_año[0] == 2017:
            for k in range(indices_a[19] - 168 ,indices_a[20]):            
                if vr_dia[l] == diaC[k] and vr_mes[l] == mesC[k] and vr_año[l] == añoC[k] and vr_hora[l] == horaC[k]:
                    cosmic_ray.append(cosmiC[k])
                else:
                    pass
            
###############################################################################
#              Ahora se crean los archivos csv para los GCR                   # 
###############################################################################
            
    with open("/media/christian/Elements/tesis/dominio_sirs/data"+str(i)+".csv", mode = 'w+') as data_file:
        data_file = csv.writer(data_file, delimiter=',')        
        data_file.writerow(cosmic_ray)
        data_file.writerow(cosmic_ray)
        data_file.writerow(vr_año)
        data_file.writerow(vr_mes)
        data_file.writerow(vr_dia)
        data_file.writerow(vr_hora)
