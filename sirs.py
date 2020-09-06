#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 08:43:38 2020

@author: christian
"""
import os
os.environ["CDF_LIB"] = "/home/christian/Desktop/cdf-dist-all/cdf37_1-dist/lib"
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
from spacepy import pycdf
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages

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
"""
En esta parte se crea el vector inico del SIR, final del SIR, la duración del SIR,
el inicio del dominio y el final del dominio    


for i in range(0,len(año_fin_A)):
    inicio_sir_datetime = datetime.datetime(año_inicio_A[i], mes_inicio_A[i], dia_inicio_A_limpio[i], hora_inicio_A[i], minuto_inicio_A[i])
    fin_sir_datetime = datetime.datetime(año_fin_A[i], mes_fin_A[i], dia_fin_A_limpio[i], hora_fin_A[i], minuto_fin_A[i])
    delta_t = fin_sir_datetime - inicio_sir_datetime
    contador = int(delta_t.total_seconds()/(60*24*60)) + 1
    
    inicio_dominio = inicio_sir_datetime - delta_t
    fin_dominio = fin_sir_datetime + delta_t
"""    
###############################################################################
"""
En este paso se crean los vectores año, mes, día y hora que se van a plotear, se
utiliza el vector contador que corresponde a la longitud del evento como número entero
(días que dura el evento) y luego se toma de dominio esa cantidad anterior y esa
cantidad posterior. Se va a arrancar del -contador y se va a llegar a 2 veces el contador +1
"""

vr_año =[] #Genero la "lista" vacia
vr_mes = [] #Genero la "lista" vacia
vr_dia = [] #Genero la "lista" vacia
vr_hora = [] #Genero la "lista" vacia

with PdfPages("/media/christian/Elements/SIRS_VIEJA") as pp:
    for i in range(0,2): # len(dia_fin_A_limpio)
    
        inicio_sir_datetime = datetime.datetime(año_inicio_A[i], mes_inicio_A[i], dia_inicio_A_limpio[i], hora_inicio_A[i], minuto_inicio_A[i])
        fin_sir_datetime = datetime.datetime(año_fin_A[i], mes_fin_A[i], dia_fin_A_limpio[i], hora_fin_A[i], minuto_fin_A[i])
        delta_t = fin_sir_datetime - inicio_sir_datetime
        contador = int(delta_t.total_seconds()/(60*24*60)) + 1
        
        inicio_dominio = inicio_sir_datetime - delta_t
        fin_dominio = fin_sir_datetime + delta_t
        
        if dia_inicio_A_limpio[i] - contador >= 10 and (mes_inicio_A[i] < 10):
            cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i] - contador))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i] - contador))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_inicio_A[i])
                vr_mes.append(mes_inicio_A[i])
                vr_dia.append(dia_inicio_A_limpio[i] - contador)
        elif dia_inicio_A_limpio[i] - contador >= 10 and (mes_inicio_A[i] >= 10):
            cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i] - contador))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i] - contador))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_inicio_A[i])
                vr_mes.append(mes_inicio_A[i])
                vr_dia.append(dia_inicio_A_limpio[i] - contador)
        elif dia_inicio_A_limpio[i] - contador < 10 and dia_inicio_A_limpio[i] - contador >= 1 and (mes_inicio_A[i] < 10):
            cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i] - contador))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i] - contador))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_inicio_A[i])
                vr_mes.append(mes_inicio_A[i])
                vr_dia.append(dia_inicio_A_limpio[i] - contador)
        elif dia_inicio_A_limpio[i] - contador < 10 and dia_inicio_A_limpio[i] - contador >= 1 and (mes_inicio_A[i] >= 10):
            cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i] - contador))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i] - contador))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_inicio_A[i])
                vr_mes.append(mes_inicio_A[i])
                vr_dia.append(dia_inicio_A_limpio[i] - contador)
        elif dia_inicio_A_limpio[i] - contador < 1 and (mes_inicio_A[i] == 2 or mes_inicio_A[i] == 4 or mes_inicio_A[i] == 6 or mes_inicio_A[i] == 8 or mes_inicio_A[i] == 9):
            cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] - contador + 31))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] - contador + 31))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_inicio_A[i])
                vr_mes.append(mes_inicio_A[i] - 1)
                vr_dia.append(dia_inicio_A_limpio[i] - contador + 31)
        elif dia_inicio_A_limpio[i] - contador < 1 and (mes_inicio_A[i] == 5 or mes_inicio_A[i] == 7 or mes_inicio_A[i] == 10):
            cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] - contador + 30))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] - contador + 30))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_inicio_A[i])
                vr_mes.append(mes_inicio_A[i] - 1)
                vr_dia.append(dia_inicio_A_limpio[i] - contador + 30)
        elif dia_inicio_A_limpio[i] - contador < 1 and mes_inicio_A[i] == 11:
            cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] - contador + 31))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] - contador + 31))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_inicio_A[i])
                vr_mes.append(mes_inicio_A[i] - 1)
                vr_dia.append(dia_inicio_A_limpio[i] - contador + 31)
        elif dia_inicio_A_limpio[i] - contador < 1 and mes_inicio_A[i] == 12:
            cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] - contador + 30))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] - contador + 30))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_inicio_A[i])
                vr_mes.append(mes_inicio_A[i] - 1)
                vr_dia.append(dia_inicio_A_limpio[i] - contador + 30)
        elif dia_inicio_A_limpio[i] - contador < 1 and mes_inicio_A[i] == 3 and np.remainder(año_inicio_A[i],4) != 0:
            cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] - contador + 28))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] - contador + 28))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_inicio_A[i])
                vr_mes.append(mes_inicio_A[i] - 1)
                vr_dia.append(dia_inicio_A_limpio[i] - contador + 28)
        elif dia_inicio_A_limpio[i] - contador < 1 and mes_inicio_A[i] == 3 and np.remainder(año_inicio_A[i],4) == 0:
            cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] - contador + 29))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] - contador + 29))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_inicio_A[i])
                vr_mes.append(mes_inicio_A[i] - 1)
                vr_dia.append(dia_inicio_A_limpio[i] - contador + 29)
        elif dia_inicio_A_limpio[i] - contador < 1 and mes_inicio_A[i] == 1:
            cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]-1))+'12'+str(int(dia_inicio_A_limpio[i] - contador + 31))+'_v04.cdf')
            cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]-1))+'12'+str(int(dia_inicio_A_limpio[i] - contador + 31))+'_v06.cdf')
            for x in range(0,24):
                vr_hora.append(x)
                vr_año.append(año_inicio_A[i] - 1)
                vr_mes.append(12)
                vr_dia.append(dia_inicio_A_limpio[i] - contador + 31)
                
        tv = cdf1['Epoch'][:] #En la primer iteración del for creo la matriz, luego en los siguientes se concatenará a esta matriz los datos correspondientes a los siguientes días.
        Vx = cdf1['V_GSE'][:,0] #En la primer iteración del for creo la matriz, luego en los siguientes se concatenará a esta matriz los datos correspondientes a los siguientes días
        Np = cdf1['Np'][:] #En la primer iteración del for creo la matriz, luego en los siguientes se concatenará a esta matriz los datos correspondientes a los siguientes días
        t = cdf['Epoch'][:] #En la primer iteración del for creo la matriz, luego en los siguientes se concatenará a esta matriz los datos correspondientes a los siguientes días
        Bx = cdf['BGSEc'][:,0] #En la primer iteración del for creo la matriz, luego en los siguientes se concatenará a esta matriz los datos correspondientes a los siguientes días
        By = cdf['BGSEc'][:,1] #En la primer iteración del for creo la matriz, luego en los siguientes se concatenará a esta matriz los datos correspondientes a los siguientes días
        Bz = cdf['BGSEc'][:,2] #En la primer iteración del for creo la matriz, luego en los siguientes se concatenará a esta matriz los datos correspondientes a los siguientes días
        Tpr = cdf1['Tpr'][:]
    
        for j in range(-contador + 1, contador * 2 + 1):
            if j < 0:
                if dia_inicio_A_limpio[i] + j >= 10 and (mes_inicio_A[i] < 10):
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i] + j))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i] + j))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i])
                        vr_dia.append(dia_inicio_A_limpio[i] + j)
                elif dia_inicio_A_limpio[i] + j >= 10 and (mes_inicio_A[i] >= 10):
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i] + j))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i] + j))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i])
                        vr_dia.append(dia_inicio_A_limpio[i] + j)
                elif dia_inicio_A_limpio[i] + j < 10 and dia_inicio_A_limpio[i] + j >= 1 and (mes_inicio_A[i] < 10):
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i] + j))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i] + j))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i])
                        vr_dia.append(dia_inicio_A_limpio[i] + j)
                elif dia_inicio_A_limpio[i] + j < 10 and dia_inicio_A_limpio[i] + j >= 1 and (mes_inicio_A[i] >= 10):
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i] + j))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i] + j))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i])
                        vr_dia.append(dia_inicio_A_limpio[i] + j)
                elif dia_inicio_A_limpio[i] + j < 1 and (mes_inicio_A[i] == 2 or mes_inicio_A[i] == 4 or mes_inicio_A[i] == 6 or mes_inicio_A[i] == 8 or mes_inicio_A[i] == 9):
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] + j + 31))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] + j + 31))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i] - 1)
                        vr_dia.append(dia_inicio_A_limpio[i] + j + 31)
                elif dia_inicio_A_limpio[i] + j < 1 and (mes_inicio_A[i] == 5 or mes_inicio_A[i] == 7 or mes_inicio_A[i] == 10):
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] + j + 30))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_fin_A[i]-1))+str(int(dia_inicio_A_limpio[i] + j + 30))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i] - 1)
                        vr_dia.append(dia_inicio_A_limpio[i] + j + 30)
                elif dia_inicio_A_limpio[i] + j < 1 and mes_inicio_A[i] == 11:
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] + j + 31))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] + j + 31))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i] - 1)
                        vr_dia.append(dia_inicio_A_limpio[i] + j + 31)
                elif dia_inicio_A_limpio[i] + j < 1 and mes_inicio_A[i] == 12:
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] + j + 30))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] + j + 30))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i] - 1)
                        vr_dia.append(dia_inicio_A_limpio[i] + j + 30)
                elif dia_inicio_A_limpio[i] + j < 1 and mes_inicio_A[i] == 3 and np.remainder(año_inicio_A[i],4) != 0:
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] + j + 28))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] + j + 28))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i] - 1)
                        vr_dia.append(dia_inicio_A_limpio[i] + j + 28)
                elif dia_inicio_A_limpio[i] + j < 1 and mes_inicio_A[i] == 3 and np.remainder(año_inicio_A[i],4) == 0:
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] + j + 29))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]-1))+str(int(dia_inicio_A_limpio[i] + j + 29))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i] - 1)
                        vr_dia.append(dia_inicio_A_limpio[i] + j + 29)
                elif dia_inicio_A_limpio[i] + j < 1 and mes_inicio_A[i] == 1:
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]-1))+'12'+str(int(dia_inicio_A_limpio[i] + j + 31))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]-1))+'12'+str(int(dia_inicio_A_limpio[i] + j + 31))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i] - 1)
                        vr_mes.append(12)
                        vr_dia.append(dia_inicio_A_limpio[i] + j + 31)
    
                tv = np.concatenate((tv,cdf1['Epoch'][:]),0)
                Vx = np.concatenate((Vx,cdf1['V_GSE'][:,0]),0)
                Np = np.concatenate((Np,cdf1['Np'][:]),0)
                t = np.concatenate((t,cdf['Epoch'][:]),0)
                Bx = np.concatenate((Bx,cdf['BGSEc'][:,0]),0)
                By = np.concatenate((By,cdf['BGSEc'][:,1]),0) 
                Bz = np.concatenate((Bz,cdf['BGSEc'][:,2]),0)
                Tpr = np.concatenate((Tpr,cdf1['Tpr'][:]),0)
    
            elif j == 0:
                if dia_inicio_A_limpio[i] >= 10 and mes_inicio_A[i] >= 10:
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i]))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i]))+'_v06.cdf')
                elif dia_inicio_A_limpio[i] >= 10 and mes_inicio_A[i] < 10:
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i]))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i]))+'_v06.cdf')
                elif dia_inicio_A_limpio[i] < 10 and mes_inicio_A[i] >= 10:
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i]))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i]))+'_v06.cdf')
                elif dia_inicio_A_limpio[i] < 10 and mes_inicio_A[i] < 10:
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i]))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i]))+'_v06.cdf')
                    
                tv = np.concatenate((tv,cdf1['Epoch'][:]),0)
                Vx = np.concatenate((Vx,cdf1['V_GSE'][:,0]),0)
                Np = np.concatenate((Np,cdf1['Np'][:]),0)
                t = np.concatenate((t,cdf['Epoch'][:]),0)
                Bx = np.concatenate((Bx,cdf['BGSEc'][:,0]),0)
                By = np.concatenate((By,cdf['BGSEc'][:,1]),0) 
                Bz = np.concatenate((Bz,cdf['BGSEc'][:,2]),0)
                Tpr = np.concatenate((Tpr,cdf1['Tpr'][:]),0)
                    
                for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i])
                        vr_dia.append(dia_inicio_A_limpio[i])
    
            else:
                if dia_inicio_A_limpio[i] + j == 32 and (mes_inicio_A[i] == 1 or mes_inicio_A[i] == 3 or mes_inicio_A[i] == 5 or mes_inicio_A[i] == 7 or mes_inicio_A[i] == 8):
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]+1))+'01'+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]+1))+'01'+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i] + 1)
                        vr_dia.append(1)
                elif dia_inicio_A_limpio[i] + j == 31 and (mes_inicio_A[i] == 4 or mes_inicio_A[i] == 6):
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]+1))+'01'+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]+1))+'01'+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i] + 1)
                        vr_dia.append(1)
                elif dia_inicio_A_limpio[i] + j == 32 and mes_inicio_A[i] == 10:
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]+1))+'01'+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]+1))+'01'+'_v06.cdf')                
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i] + 1)
                        vr_dia.append(1)
                elif dia_inicio_A_limpio[i] + j == 31 and (mes_inicio_A[i] == 9 or mes_inicio_A[i] == 11):
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]+1))+'01'+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]+1))+'01'+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i] + 1)
                        vr_dia.append(1)
                elif dia_inicio_A_limpio[i] + j == 32 and mes_inicio_A[i] == 12:
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i])+1)+'0101'+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i])+1)+'0101'+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i] + 1)
                        vr_mes.append(1)
                        vr_dia.append(1)
                elif dia_inicio_A_limpio[i] + j == 29 and mes_inicio_A[i] == 2 and np.remainder(año_inicio_A[i],4) != 0:
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0301'+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0301'+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(3)
                        vr_dia.append(1)
                elif dia_inicio_A_limpio[i] + j == 30 and mes_inicio_A[i] == 2 and np.remainder(año_inicio_A[i],4) == 0:
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0301'+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0301'+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(3)
                        vr_dia.append(1)
                elif dia_inicio_A_limpio[i] + j < 10 and (mes_inicio_A[i] == 1 or mes_inicio_A[i] == 3 or mes_inicio_A[i] == 5 or mes_inicio_A[i] == 7 or mes_inicio_A[i] == 8):
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i]+j))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i]+j))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i])
                        vr_dia.append(dia_inicio_A_limpio[i]+j)
                elif dia_inicio_A_limpio[i] + j < 32 and dia_inicio_A_limpio[i] + j >= 10 and (mes_inicio_A[i] == 1 or mes_inicio_A[i] == 3 or mes_inicio_A[i] == 5 or mes_inicio_A[i] == 7 or mes_inicio_A[i] == 8):
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i]+j))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i]+j))+'_v06.cdf')
                    for x in range(0,24):
                        vr_hora.append(x)
                        vr_año.append(año_inicio_A[i])
                        vr_mes.append(mes_inicio_A[i])
                        vr_dia.append(dia_inicio_A_limpio[i]+j)
                elif dia_inicio_A_limpio[i] + j < 31 and (mes_inicio_A[i] == 4 or mes_inicio_A[i] == 6 or mes_inicio_A[i] == 9):
                    if dia_inicio_A_limpio[i] + j < 10:
                        cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i])
                            vr_mes.append(mes_inicio_A[i])
                            vr_dia.append(dia_inicio_A_limpio[i]+j)
                    elif dia_inicio_A_limpio[i] + j >= 10:
                        cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i])
                            vr_mes.append(mes_inicio_A[i])
                            vr_dia.append(dia_inicio_A_limpio[i]+j)
                elif dia_inicio_A_limpio[i] + j < 32 and mes_inicio_A[i] == 10:
                    if dia_inicio_A_limpio[i] + j < 10:
                        cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i])
                            vr_mes.append(mes_inicio_A[i])
                            vr_dia.append(dia_inicio_A_limpio[i]+j)
                    elif dia_inicio_A_limpio[i] + j >= 10:
                        cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i])
                            vr_mes.append(mes_inicio_A[i])
                            vr_dia.append(dia_inicio_A_limpio[i]+j)
                elif dia_inicio_A_limpio[i] + j < 31 and (mes_inicio_A[i] == 11):
                    if dia_inicio_A_limpio[i] + j < 10:
                        cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i])
                            vr_mes.append(mes_inicio_A[i])
                            vr_dia.append(dia_inicio_A_limpio[i]+j)
                    elif dia_inicio_A_limpio[i] + j >= 10:
                        cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i])
                            vr_mes.append(mes_inicio_A[i])
                            vr_dia.append(dia_inicio_A_limpio[i]+j)
                elif dia_inicio_A_limpio[i] + j < 32 and mes_inicio_A[i] == 12:
                    if dia_inicio_A_limpio[i] + j < 10:
                        cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+'0'+str(int(dia_inicio_A_limpio[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i])
                            vr_mes.append(mes_inicio_A[i])
                            vr_dia.append(dia_inicio_A_limpio[i]+j)
                    elif dia_inicio_A_limpio[i] + j >= 10:
                        cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]))+str(int(dia_inicio_A_limpio[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i])
                            vr_mes.append(mes_inicio_A[i])
                            vr_dia.append(dia_inicio_A_limpio[i]+j)
                elif dia_inicio_A_limpio[i] + j < 29 and mes_inicio_A[i] == 2 and np.remainder(año_inicio_A[i],4) != 0:
                    if dia_inicio_A_limpio[i] + j < 10:                        
                        cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'020'+str(int(dia_inicio_A_limpio[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'020'+str(int(dia_inicio_A_limpio[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i])
                            vr_mes.append(2)
                            vr_dia.append(dia_inicio_A_limpio[i]+j)
                    elif dia_inicio_A_limpio[i] + j >= 10:                        
                        cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'02'+str(int(dia_inicio_A_limpio[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'02'+str(int(dia_inicio_A_limpio[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i])
                            vr_mes.append(2)
                            vr_dia.append(dia_inicio_A_limpio[i]+j)
                elif dia_inicio_A_limpio[i] + j < 30 and mes_inicio_A[i] == 2 and np.remainder(año_inicio_A[i],4) == 0:
                    if dia_inicio_A_limpio[i] + j < 10:                        
                        cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'020'+str(int(dia_inicio_A_limpio[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'020'+str(int(dia_inicio_A_limpio[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i])
                            vr_mes.append(2)
                            vr_dia.append(dia_inicio_A_limpio[i]+j)
                    elif dia_inicio_A_limpio[i] + j >= 10:                        
                        cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'02'+str(int(dia_inicio_A_limpio[i]+j))+'_v04.cdf')
                        cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'02'+str(int(dia_inicio_A_limpio[i]+j))+'_v06.cdf')
                        for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i])
                            vr_mes.append(2)
                            vr_dia.append(dia_inicio_A_limpio[i]+j)
                elif dia_inicio_A_limpio[i] + j > 32 and (mes_inicio_A[i] == 1 or mes_inicio_A[i] == 3 or mes_inicio_A[i] == 5 or mes_inicio_A[i] == 7 or mes_inicio_A[i] == 8):
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]+1))+'0'+str(int(dia_inicio_A_limpio[i]+j-31))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]+1))+'0'+str(int(dia_inicio_A_limpio[i]+j-31))+'_v06.cdf')
                    for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i])
                            vr_mes.append(mes_inicio_A[i] + 1)
                            vr_dia.append(dia_inicio_A_limpio[i] + j - 31)
                elif dia_inicio_A_limpio[i] + j > 31 and (mes_inicio_A[i] == 4 or mes_inicio_A[i] == 6):                    
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]+1))+'0'+str(int(dia_inicio_A_limpio[i]+j-30))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'0'+str(int(mes_inicio_A[i]+1))+'0'+str(int(dia_inicio_A_limpio[i]+j-30))+'_v06.cdf')
                    for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i])
                            vr_mes.append(mes_inicio_A[i] + 1)
                            vr_dia.append(dia_inicio_A_limpio[i] + j - 30)
                elif dia_inicio_A_limpio[i] + j > 32 and mes_inicio_A[i] == 10:                    
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]+1))+'0'+str(int(dia_inicio_A_limpio[i]+j-31))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]+1))+'0'+str(int(dia_inicio_A_limpio[i]+j-31))+'_v06.cdf')
                    for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i])
                            vr_mes.append(mes_inicio_A[i] + 1)
                            vr_dia.append(dia_inicio_A_limpio[i] + j - 31)
                elif dia_inicio_A_limpio[i] + j > 31 and (mes_inicio_A[i] == 9 or mes_inicio_A[i] == 11):
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]+1))+'0'+str(int(dia_inicio_A_limpio[i]+j-30))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+str(int(mes_inicio_A[i]+1))+'0'+str(int(dia_inicio_A_limpio[i]+j-30))+'_v06.cdf')
                    for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i])
                            vr_mes.append(mes_inicio_A[i] + 1)
                            vr_dia.append(dia_inicio_A_limpio[i] + j - 30)
                elif dia_inicio_A_limpio[i] + j > 32 and mes_inicio_A[i] == 12:                    
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]+1))+'01'+'0'+str(int(dia_inicio_A_limpio[i]+j-31))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]+1))+'01'+'0'+str(int(dia_inicio_A_limpio[i]+j-31))+'_v06.cdf')
                    for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i] + 1)
                            vr_mes.append(1)
                            vr_dia.append(dia_inicio_A_limpio[i] + j - 31)
                elif dia_inicio_A_limpio[i] + j > 29 and mes_inicio_A[i] == 2 and np.remainder(año_inicio_A[i],4) != 0:                    
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'03'+'0'+str(int(dia_inicio_A_limpio[i]+j-28))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'03'+'0'+str(int(dia_inicio_A_limpio[i]+j-28))+'_v06.cdf')
                    for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i])
                            vr_mes.append(3)
                            vr_dia.append(dia_inicio_A_limpio[i] + j - 28)
                elif dia_inicio_A_limpio[i] + j > 30 and mes_inicio_A[i] == 2 and np.remainder(año_inicio_A[i],4) == 0:
                    cdf = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_mag_cdf_16seg/ac_h0_mfi_'+str(int(año_inicio_A[i]))+'03'+'0'+str(int(dia_inicio_A_limpio[i]+j-29))+'_v04.cdf')
                    cdf1 = pycdf.CDF('/media/christian/Elements/tesis/datos/ace_swepam_cdf_1min/ac_h0_swe_'+str(int(año_inicio_A[i]))+'03'+'0'+str(int(dia_inicio_A_limpio[i]+j-29))+'_v06.cdf')
                    for x in range(0,24):
                            vr_hora.append(x)
                            vr_año.append(año_inicio_A[i])
                            vr_mes.append(3)
                            vr_dia.append(dia_inicio_A_limpio[i] + j - 29)
                            
                tv = np.concatenate((tv,cdf1['Epoch'][:]),0)
                Vx = np.concatenate((Vx,cdf1['V_GSE'][:,0]),0)
                Np = np.concatenate((Np,cdf1['Np'][:]),0)                                
                t = np.concatenate((t,cdf['Epoch'][:]),0)
                Bx = np.concatenate((Bx,cdf['BGSEc'][:,0]),0)
                By = np.concatenate((By,cdf['BGSEc'][:,1]),0) 
                Bz = np.concatenate((Bz,cdf['BGSEc'][:,2]),0)
                Tpr = np.concatenate((Tpr,cdf1['Tpr'][:]),0)
                
    ###############################################################################
    # En esta parte se eliminan los errores de las matrices
    
        errornp = np.where(Np == -1e+31) #Ubico los errores        
        errorvx = np.where(Vx == -1e+31) #Ubico los errores
        errortpr = np.where(Tpr == -1e+31) #Ubico los errores
        Np = np.delete(Np,errornp) #Borro los errores
        Vx = np.delete(Vx,errorvx) #Borro los errores
        Tpr = np.delete(Tpr,errortpr) #Borro los errores
        tnp = np.delete(tv, errornp) #Borro los errores
        tvx = np.delete(tv, errorvx) #Borro los errores
        ttpr = np.delete(tv, errortpr) #Borro los errores
        
        errory = np.where(By == -1e+31) #Ubico los errores
        errorz = np.where(Bz == -1e+31) #Ubico los errores        
        errorx = np.where(Bx == -1e+31) #Ubico los errores
        Bx = np.delete(Bx,errorx) #Borro los errores
        By = np.delete(By,errory) #Borro los errores
        Bz = np.delete(Bz,errorz) #Borro los errores
        tx = np.delete(t, errorx) #Borro los errores
        ty = np.delete(t, errory) #Borro los errores
        tz = np.delete(t, errorz) #Borro los errores      
        
        B = np.sqrt((Bx * Bx) + (By * By) + (Bz * Bz)) #Calculo el módulo de B, en otras palabras el B total
    
###############################################################################
#En esta parte voy a calcular los índices correspondientes al inicio del dominio
#al inicio del SIR, al final del SIR y al final del dominio, esto se hace para
#poder calcular la media y el máximo correspondiente a las distintas partes del dominio    
###############################################################################
        
        indice_tB_inicio_dominio = []
        indice_tB_inicio_sir = []
        indice_tB_fin_sir = []
        indice_tB_fin_dominio = []
        
        for x in range(0,len(t)):
            if inicio_dominio >= t[x]:
                indice_tB_inicio_dominio = x
            else:
                pass
    
        for x in range(0,len(t)):
            if inicio_sir_datetime >= t[x]:
                indice_tB_inicio_sir = x
            else:
                pass
            
        for x in range(0,len(t)):
            if fin_sir_datetime >= t[x]:
                indice_tB_fin_sir = x
            else:
                pass
    
        for x in range(0,len(t)):
            if fin_dominio >= t[x]:
                indice_tB_fin_dominio = x
            else:
                pass
###############################################################################        
# Ahora calculo los estadísticos que me interesan
# Armo 4 vectores con con dominio pre, sir, post y total y le calculo estadisticos
###############################################################################
                
        B_dominio_pre_sir = [] 
        B_dominio_sir = []
        B_dominio_post_sir = []
        B_dominio_total = []
        
        for x in range(indice_tB_inicio_dominio, indice_tB_inicio_sir + 1):
            B_dominio_pre_sir.append(B[x])
    
        for x in range(indice_tB_inicio_sir, indice_tB_fin_sir + 1):
            B_dominio_sir.append(B[x])
        
        for x in range(indice_tB_fin_sir, indice_tB_fin_dominio + 1):
            B_dominio_post_sir.append(B[x])
    
        for x in range(indice_tB_inicio_dominio, indice_tB_fin_dominio + 1):
            B_dominio_total.append(B[x])
    
        B_mean_pre_sir = np.mean(B_dominio_pre_sir)
        B_max_pre_sir = np.max(B_dominio_pre_sir)
        B_mean_sir = np.mean(B_dominio_sir)
        B_max_sir = np.max(B_dominio_sir) 
        B_max_total = np.max(B_dominio_total)

###############################################################################
#                Ahora hago lo mismo para la velocidad                        #
###############################################################################

        indice_Vx_inicio_dominio = []
        indice_Vx_inicio_sir = []
        indice_Vx_fin_sir = []
        indice_Vx_fin_dominio = []

        for x in range(0,len(tvx)):
            if inicio_dominio >= tvx[x]:
                indice_Vx_inicio_dominio = x
            else:
                pass
    
        for x in range(0,len(tvx)):
            if inicio_sir_datetime >= tvx[x]:
                indice_Vx_inicio_sir = x
            else:
                pass
            
        for x in range(0,len(tvx)):
            if fin_sir_datetime >= tvx[x]:
                indice_Vx_fin_sir = x
            else:
                pass
    
        for x in range(0,len(tvx)):
            if fin_dominio >= tvx[x]:
                indice_Vx_fin_dominio = x
            else:
                pass

        Vx_dominio_pre_sir = [] 
        Vx_dominio_sir = []
        Vx_dominio_post_sir = []
        Vx_dominio_total = []
        
        for x in range(indice_Vx_inicio_dominio, indice_Vx_inicio_sir + 1):
            Vx_dominio_pre_sir.append(Vx[x])
    
        for x in range(indice_Vx_inicio_sir, indice_Vx_fin_sir + 1):
            Vx_dominio_sir.append(Vx[x])
        
        for x in range(indice_Vx_fin_sir, indice_Vx_fin_dominio + 1):
            Vx_dominio_post_sir.append(Vx[x])
    
        for x in range(indice_Vx_inicio_dominio, indice_Vx_fin_dominio + 1):
            Vx_dominio_total.append(Vx[x])
    
        Vx_mean_pre_sir = np.mean(Vx_dominio_pre_sir)
        Vx_max_pre_sir = np.max(Vx_dominio_pre_sir)
        Vx_min_pre_sir = np.min(Vx_dominio_pre_sir)
        Vx_mean_sir = np.mean(Vx_dominio_sir)
        Vx_max_sir = np.max(Vx_dominio_sir)
        Vx_min_sir = np.min(Vx_dominio_sir)
        Vx_max_total = np.max(Vx_dominio_total)
        Vx_min_total = np.min(Vx_dominio_total)

###############################################################################
#             Ahora hago lo mismo para la densidad de partículas              #
###############################################################################

        indice_Np_inicio_dominio = []
        indice_Np_inicio_sir = []
        indice_Np_fin_sir = []
        indice_Np_fin_dominio = []

        for x in range(0,len(tnp)):
            if inicio_dominio >= tnp[x]:
                indice_Np_inicio_dominio = x
            else:
                pass
    
        for x in range(0,len(tnp)):
            if inicio_sir_datetime >= tnp[x]:
                indice_Np_inicio_sir = x
            else:
                pass
            
        for x in range(0,len(tnp)):
            if fin_sir_datetime >= tnp[x]:
                indice_Np_fin_sir = x
            else:
                pass
    
        for x in range(0,len(tnp)):
            if fin_dominio >= tnp[x]:
                indice_Np_fin_dominio = x
            else:
                pass

        Np_dominio_pre_sir = [] 
        Np_dominio_sir = []
        Np_dominio_post_sir = []
        Np_dominio_total = []

###############################################################################
#  Linea importante de código, como tiene mucho dato faltante se dice que si  #
#    el índice siguiente no entra en el intervalo pre sir y ingresa en otro   #
#            posterior entonces se asigna el código de error -9999            #
###############################################################################
        
        if tnp[indice_Np_inicio_dominio + 1] > inicio_sir_datetime:
            Np_dominio_pre_sir.append(-9999)
        else:
            for x in range(indice_Np_inicio_dominio, indice_Np_inicio_sir + 1):
                Np_dominio_pre_sir.append(Np[x])

    
        for x in range(indice_Np_inicio_sir, indice_Np_fin_sir + 1):
            Np_dominio_sir.append(Np[x])
        
        for x in range(indice_Np_fin_sir, indice_Np_fin_dominio + 1):
            Np_dominio_post_sir.append(Np[x])
    
        for x in range(indice_Np_inicio_dominio, indice_Np_fin_dominio + 1):
            Np_dominio_total.append(Np[x])

        Np_mean_pre_sir = np.mean(Np_dominio_pre_sir)
        Np_max_pre_sir = np.max(Np_dominio_pre_sir)
        Np_min_pre_sir = np.min(Np_dominio_pre_sir)    
        Np_mean_sir = np.mean(Np_dominio_sir)
        Np_max_sir = np.max(Np_dominio_sir)
        Np_min_sir = np.min(Np_dominio_sir)
        Np_max_total = np.max(Np_dominio_total)
        Np_min_total = np.min(Np_dominio_total)

###############################################################################
#                   Ahora hago lo mismo para la temperatura                   #
###############################################################################

        indice_Tpr_inicio_dominio = []
        indice_Tpr_inicio_sir = []
        indice_Tpr_fin_sir = []
        indice_Tpr_fin_dominio = []

        for x in range(0,len(ttpr)):
            if inicio_dominio >= ttpr[x]:
                indice_Tpr_inicio_dominio = x
            else:
                pass
    
        for x in range(0,len(ttpr)):
            if inicio_sir_datetime >= ttpr[x]:
                indice_Tpr_inicio_sir = x
            else:
                pass
            
        for x in range(0,len(ttpr)):
            if fin_sir_datetime >= ttpr[x]:
                indice_Tpr_fin_sir = x
            else:
                pass
    
        for x in range(0,len(ttpr)):
            if fin_dominio >= ttpr[x]:
                indice_Tpr_fin_dominio = x
            else:
                pass

        Tpr_dominio_pre_sir = [] 
        Tpr_dominio_sir = []
        Tpr_dominio_post_sir = []
        Tpr_dominio_total = []

###############################################################################
#  Linea importante de código, como tiene mucho dato faltante se dice que si  #
#    el índice siguiente no entra en el intervalo pre sir y ingresa en otro   #
#            posterior entonces se asigna el código de error -9999            #
###############################################################################
        
        if ttpr[indice_Tpr_inicio_dominio + 1] > inicio_sir_datetime:
            Tpr_dominio_pre_sir.append(-9999)
        else:
            for x in range(indice_Tpr_inicio_dominio, indice_Tpr_inicio_sir + 1):
                Tpr_dominio_pre_sir.append(Tpr[x])

    
        for x in range(indice_Tpr_inicio_sir, indice_Tpr_fin_sir + 1):
            Tpr_dominio_sir.append(Tpr[x])
        
        for x in range(indice_Tpr_fin_sir, indice_Tpr_fin_dominio + 1):
            Tpr_dominio_post_sir.append(Tpr[x])
    
        for x in range(indice_Tpr_inicio_dominio, indice_Tpr_fin_dominio + 1):
            Tpr_dominio_total.append(Tpr[x])

        Tpr_mean_pre_sir = np.mean(Tpr_dominio_pre_sir)
        Tpr_max_pre_sir = np.max(Tpr_dominio_pre_sir)
        Tpr_min_pre_sir = np.min(Tpr_dominio_pre_sir)    
        Tpr_mean_sir = np.mean(Tpr_dominio_sir)
        Tpr_max_sir = np.max(Tpr_dominio_sir)
        Tpr_min_sir = np.min(Tpr_dominio_sir)
        Tpr_max_total = np.max(Tpr_dominio_total)
        Tpr_min_total = np.min(Tpr_dominio_total)

###############################################################################
#                                 Grafico                                     #    
###############################################################################        
        fig = plt.figure(figsize=(35, 65))
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, figsize=(24,12))
        
        plt.subplots_adjust(wspace=0.9, hspace=0.3, left=0.05, bottom=0.05, right=0.95, top=0.95)
        props = dict(boxstyle='square', facecolor='silver', alpha=0.5)
        
        ax1.plot(tx,Bx, linewidth=0.25, label = 'Bx')
        ax1.plot(ty,By, linewidth=0.25, label = 'By')
        ax1.plot(tz,Bz, linewidth=0.25, label = 'Bz')
        ax1.plot(tx,B, linewidth=0.25, color='k', label = 'B')
        ax1.set_ylabel('B [nT]', fontsize = 14, position = (0.1,0.5))
        ax1.axvline(x=inicio_sir_datetime, color='r')
        ax1.axvline(x=fin_sir_datetime, color='r')
        ax1.axhline(y=0, color='k', linewidth=2)
        ax1.axhline(y=B_mean_pre_sir, xmin=0, xmax=1/3, color='r', linewidth=1)
        ax1.axhline(y=B_max_sir, xmin=1/3, xmax=2/3, color='red', linestyle = '--', linewidth=1)
        ax1.axhline(y=B_mean_sir, xmin=1/3, xmax=2/3, color='indigo', linewidth=1)
        ax1.set_xlim([inicio_dominio ,fin_dominio])
        ax1.set_ylim([-B_max_total - 1, B_max_total + 1])
        ax1.legend(loc = 2, fontsize = 14, facecolor='lavender')
        ax1.text(0.923, 0.75 , 'B$_{max}$ = ' + str("{:.2f}".format(B_max_sir)) + ' nT\nB$_{mean}$ = '+str("{:.2f}".format(B_mean_sir)) + ' nT', transform = ax1.transAxes, fontsize = 14, bbox = props)
        myFmt = mdates.DateFormatter('%Y-%m-%d %H')
        ax1.xaxis.set_major_formatter(myFmt)
        ax1.tick_params(axis='both', which='major', labelsize=14)
        
        ax2.plot(tvx, -Vx, linewidth=0.25, color='k')
        ax2.set_ylabel('-V$_{x}$ [Km/s]', fontsize = 14, position = (0.1,0.5))
        ax2.axvline(x=inicio_sir_datetime , color='r')
        ax2.axvline(x=fin_sir_datetime, color='r')
        ax2.axhline(y=-Vx_mean_pre_sir, xmin=0, xmax=1/3,  color='r', linewidth=1)
        ax2.axhline(y=-Vx_min_sir, xmin=1/3, xmax=2/3, color='red', linestyle = '--', linewidth=1, label='máximo')
        ax2.axhline(y=-Vx_mean_sir, xmin=1/3, xmax=2/3, color='indigo', linewidth=1)
        ax2.set_xlim([inicio_dominio, fin_dominio])
        ax2.set_ylim([-Vx_max_total * 0.95, -Vx_min_total * 1.05])
        ax2.text(0.003, 0.62 , 'V$_{max}$ = ' + str("{:.0f}".format(Vx_min_sir)) + ' Km/s\nV$_{mean}$ = '+ str("{:.0f}".format(Vx_mean_sir)) + ' Km/s\nGSE coordenate system', transform = ax2.transAxes, fontsize = 14, bbox = props)
        myFmt = mdates.DateFormatter('%Y-%m-%d %H')
        ax2.xaxis.set_major_formatter(myFmt)
        ax2.tick_params(axis='both', which='major', labelbottom=False, labelsize=14)
        
        ax3.plot(tnp,Np, linewidth=0.25, color='k')
        ax3.set_ylabel('Np [cm$^{-3}$]', fontsize = 14,  position = (0.1,0.5))
        ax3.axvline(x=inicio_sir_datetime, color='r')
        ax3.axvline(x=fin_sir_datetime, color='r')
        ax3.axhline(y=Np_mean_pre_sir, xmin=0, xmax=1/3,  color='r', linewidth=1)
        ax3.axhline(y=Np_max_sir, xmin=1/3, xmax=2/3, color='red', linestyle = '--', linewidth=1, label='máximo')
        ax3.axhline(y=Np_mean_sir, xmin=1/3, xmax=2/3, color='indigo', linewidth=1, label='media_total')
        ax3.set_xlim([inicio_dominio, fin_dominio])
        ax3.set_ylim([Np_min_total * 0.98, Np_max_total * 1.02])
        myFmt = mdates.DateFormatter('%Y-%m-%d %H')
        ax3.xaxis.set_major_formatter(myFmt)
        ax3.text(0.003, 0.72 , 'Np$_{max}$ = ' + str("{:.2f}".format(Np_max_sir)) + ' cm$^{-3}$\nNp$_{mean}$ = ' + str("{:.2f}".format(Np_mean_sir)) + ' cm$^{-3}$', transform = ax3.transAxes, fontsize = 14, bbox = props)
        ax3.tick_params(axis='both', which='major', labelbottom=False, labelsize=14)
        
        ax4.plot(ttpr, Tpr, linewidth=0.25, color='k')
        ax4.set_ylabel('Tp [K]', fontsize = 14,  position = (0.1,0.5))
        ax4.axvline(x=inicio_sir_datetime, color='r')
        ax4.axvline(x=fin_sir_datetime, color='r')
        ax4.axhline(y=Tpr_mean_pre_sir, xmin=0, xmax=1/3,  color='r', linewidth=1)
        ax4.axhline(y=Tpr_max_sir, xmin=1/3, xmax=2/3, color='red', linestyle = '--', linewidth=1, label='máximo')
        ax4.axhline(y=Tpr_mean_sir, xmin=1/3, xmax=2/3, color='indigo', linewidth=1)
        ax4.set_xlim([inicio_dominio, fin_dominio])
        ax4.set_ylim([Tpr_min_total * 0.8, Tpr_max_total * 1.5])
        ax4.text(0.003, 0.75, 'Tp$_{max}$ = ' +str("{:.1e}".format(Tpr_max_sir))+' K' + '\nTp$_{mean}$ = ' + str("{:.1e}".format(Tpr_mean_sir)) + ' K', transform = ax4.transAxes, fontsize = 14, bbox = props)
        ax4.xaxis.set_major_formatter(myFmt)
        ax4.set_yscale('log')
        ax4.tick_params(axis='both', which='major', labelbottom=False, labelsize=14)
        
        ax1.set_title(str(año_inicio_A[i])+'/'+str(mes_inicio_A[i])+'/'+str(dia_inicio_A_limpio[i]), fontsize = 'xx-large')
        pp.savefig(fig)