import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

resource_url = "https://es.wikipedia.org/wiki/Anexo:Pel%C3%ADculas_con_las_mayores_recaudaciones"
response = requests.get(resource_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    tax_table = pd.read_html(resource_url)
    df = tax_table[0]
    df = df.dropna()
    df['Presupuesto'] = df['Presupuesto'].str.replace(' ', '', regex=False)

print(tax_table[0].columns)
print(tax_table[0])
print(f'Las tablas son: {len(tax_table)}')
print(df)

conexion = sqlite3.connect('peliculas_taquilleras.db')
cursor = conexion.cursor()

df.to_sql('peliculas', conexion, if_exists='replace', index = False)
conexion. commit()

conexion = sqlite3.connect('peliculas_taquilleras.db')
cursor = conexion.cursor()

cursor.execute('''
    SELECT "Película" FROM peliculas
''')
resultados = cursor.fetchall()
for fila in resultados:
    print(fila)

cursor.execute('''
    SELECT "Película","Presupuesto" FROM peliculas WHERE "Presupuesto" > 400000000
''')
resultados = cursor.fetchall()
for fila in resultados:
    print(fila)

cursor.execute('''
    SELECT "Película","Año de estreno" FROM peliculas WHERE "Año de estreno" < 2000
''')
resultados = cursor.fetchall()
for fila in resultados:
    print(fila)

conexion = sqlite3.connect('peliculas_taquilleras.db')
df = pd.read_sql_query("SELECT * FROM peliculas", conexion)
df['Presupuesto'] = df['Presupuesto'].str.replace(' ', '', regex=False)
print(df['Presupuesto'])
conexion.close()

x = df["Año de estreno"]
y = df["Presupuesto"]
plt.yscale('log')
plt.bar(x, y)
plt.show()

peliculas_comparar = ['Venom', 'Inside Out', 'Aladdín']
df_peliculas_comparar = df[df['Película'].isin(peliculas_comparar)]

x = df_peliculas_comparar["Película"]
y = df_peliculas_comparar["Recaudación mundial"]
plt.bar(x, y, color = "Red")
plt.show()