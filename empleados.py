import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import re

st.title('Empleados')
st.header ("Análisis de deserción de empleados")

st.write ("""
Esta aplicación analiza la deserción de empleados de una empresa
""")

st.subheader('Integrantes: Pedro de Jesus Hernandez Rojas')
st.subheader('Cristian Terán Juárez ')

sidebar = st.sidebar
sidebar.title("MENU")


DATA_URL = ('https://raw.githubusercontent.com/Pedrohero13/Empleados/main/employees.csv')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, encoding_errors='ignore')
    return data
data = load_data(1000) #cache para las funciones 
#Cargar datos si se selecciona en el checkbox
agree = sidebar.checkbox("¿Quieres mostrar todos los datos? ",key ="Dataframe")
if agree:
  data_load_state = st.text('Cargando...')
  data = load_data(1000)
  
  data_load_state.text("Cargado! (usando st.cache)")
  st.dataframe(data)
  
sidebar.markdown("___")
#filtrar por employees_ID hometown o unit
@st.cache
def load_data_byEmployeesID(id):
  
  filtered_data_byname = data[data['Employee_ID'].str.contains(id,flags=re.IGNORECASE)]
  
  return filtered_data_byname

@st.cache
def load_data_byHometown(hometown):
  
  filtered_data_byname = data[data['Hometown'].str.contains(hometown,flags=re.IGNORECASE)]
  
  return filtered_data_byname

@st.cache
def load_data_byUnit(unit):
  
  filtered_data_byname = data[data['Unit'].str.contains(unit, flags=re.IGNORECASE)]
  return filtered_data_byname

inputUser = st.sidebar.text_input('Ingrese el id o ciudad o el trabajo: ')
btnFilteredID = sidebar.button('Buscar por ID')
btnFilteredHometown = sidebar.button('Buscar por Ciudad natal')
btnFilteredUnit = sidebar.button('Buscar por Trabajo')

if (btnFilteredID):
  st.write ("ID buscado: "+ inputUser)
  filterbyname = load_data_byEmployeesID(inputUser)
  count_row = filterbyname.shape[0]
  st.write(f'Total: {count_row}')

  st.dataframe(filterbyname)

if (btnFilteredHometown):
  st.write ("Ciudad buscada: "+ inputUser)
  filterbyname = load_data_byHometown(inputUser)
  count_row = filterbyname.shape[0]
  st.write(f'Total: {count_row}')

  st.dataframe(filterbyname)

if (btnFilteredUnit):
  st.write ("Trabajo buscado: "+ inputUser)
  filterbyname = load_data_byUnit(inputUser)
  count_row = filterbyname.shape[0]
  st.write(f'Total: {count_row}')

  st.dataframe(filterbyname)

sidebar.markdown("___")

#Filtrar por nivel educatico por selectBox
@st.cache
def load_data_bydire(level):
  filtered_data_byLevel = data[data['Education_Level'] == level]
  return filtered_data_byLevel

selected = sidebar.selectbox("Selecciona el Nivel educativo", data['Education_Level'].unique())
btnFilterByLevel = sidebar.button('Filtrar por Nivel educativo')

if (btnFilterByLevel): 
  st.write("Empleados con nivel educativo "+ str(selected))
  filterbylevel = load_data_bydire(selected)
  count_row = filterbylevel.shape[0]
  st.write(f'Total: {count_row}')

  st.dataframe(filterbylevel)
sidebar.markdown("___")
#Filtrar por Ciudad natal por selectBox
@st.cache
def load_data_byhome(home):
  filtered_data_byHome = data[data['Hometown'] == home]
  return filtered_data_byHome

selectedHome = sidebar.selectbox("Selecciona la ciudad natal", data['Hometown'].unique())
btnFilterByHometown = sidebar.button('Filtrar por Ciudad')

if (btnFilterByHometown): 
  st.write("Empleados con Ciudad natal "+ str(selectedHome))
  filterbyhome = load_data_byhome(selectedHome)
  count_row = filterbyhome.shape[0]
  st.write(f'Total: {count_row}')

  st.dataframe(filterbyhome)
sidebar.markdown("___")
#Filtrar por Tipo de trabajo por selectBox
@st.cache
def load_data_byUnit(unit):
  filtered_data_byunit = data[data['Unit'] == unit]
  return filtered_data_byunit

selectedUnit = sidebar.selectbox("Selecciona el trabajo", data['Unit'].unique())
btnFilterByUnit = sidebar.button('Filtrar por Trabajo')

if (btnFilterByUnit): 
  st.write("Empleados con el trabajo "+ str(selectedUnit))
  filterbyunit = load_data_byUnit(selectedUnit)
  count_row = filterbyunit.shape[0]
  st.write(f'Total: {count_row}')

  st.dataframe(filterbyunit)
sidebar.markdown("___")

sidebar.subheader("Graficas")

# histograma edades 
agreeHis = sidebar.checkbox("Histograma de edades ",key = "edades")
if agreeHis:
  fig, ax = plt.subplots()

  ax.hist(data['Age'], color='#F2AB6D', rwidth=0.85)
  ax.set_xlabel("Edad")
  ax.set_ylabel("Numero de empleados")
  st.header("Histograma de empleados por edad")

  st.pyplot(fig)

  st.markdown("___")

# frecuencia  
agreeFrecuency = sidebar.checkbox("Frecuencia por trabajo ",key = "frecuencia")
if agreeFrecuency:
  fig, ax = plt.subplots()

  ax.hist(data['Unit'], rwidth=0.85)
  ax.set_xlabel("Trabajo")
  ax.set_ylabel("Numero de empleados")
  st.header("Frecuencia de Empleados por Trabajo ")
  plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
  st.pyplot(fig)
  
  st.markdown("___")

# indice de desercion por ciudad
agreeDesercion = sidebar.checkbox("Indice de deserción por ciudad ",key = "desercion")
if agreeDesercion:
  fig, ax = plt.subplots()

  y_pos = data['Attrition_rate']
  x_pos = data['Hometown']

  ax.bar(x_pos, y_pos)
  ax.set_ylabel("Desercion")
  ax.set_xlabel("Ciudad natal")
  ax.set_title('¿Cuantos empleados desertaron por ciudad?')

  st.header("Indice de deserción por ciudad")

  st.pyplot(fig)

  st.markdown("___")

# indice de desercion por edad

agreeEdad = sidebar.checkbox("Indice de deserción por edad ", key = "desEdad")
if agreeEdad:
  fig, ax = plt.subplots()

  y_pos = data['Attrition_rate']
  x_pos = data['Age']

  ax.barh(x_pos, y_pos)
  ax.set_xlabel("Desercion")
  ax.set_ylabel("Edad")
  ax.set_title('¿Cuantos empleados desertaron por edad?')

  st.header("Indice de deserción por edad")

  st.pyplot(fig)

  st.markdown("___")

# indice de desercion por tiempo de servicio

agreeService = sidebar.checkbox("Indice de deserción por Tiempo de servicio ",key = "service")
if agreeService:
  fig, ax = plt.subplots()

  y_pos = data['Attrition_rate']
  x_pos = data['Time_of_service']

  ax.bar(x_pos, y_pos)
  ax.set_ylabel("Desercion")
  ax.set_xlabel("Tiempo de servicio")
  ax.set_title('¿Cuantos empleados desertaron por tiempo de servicio?')

  st.header("Indice de deserción por tiempo de servicio")

  st.pyplot(fig)

  st.markdown("___")