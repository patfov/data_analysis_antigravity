import json
import os

cells = []

def add_md(text):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": [text]})

def add_code(code):
    cells.append({"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": None, "source": [code]})

add_md("# Análisis Exploratorio de Datos (EDA) - E-commerce\n\nEste notebook contiene el EDA para el dataset de pedidos de e-commerce, siguiendo la metodología para extraer insights accionables de negocio.")

add_md("## 1. Entender el Problema\n\n**Objetivo de negocio:** Identificar patrones de ventas, rendimiento por categorías/países, y analizar devoluciones y tiempos de envío para mejorar las decisiones de negocio.\n**Audiencia:** Gerencia e interesados de negocio.\n**Datos disponibles:** `pedidos_ecommerce.csv` a nivel de pedido.")

add_md("## 2. Exploración y Preparación de Datos")

add_code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración visual
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Carga de datos
df = pd.read_csv('pedidos_ecommerce.csv')
df.head()""")

add_code("""# Verificamos estructura y tipos de datos
df.info()""")

add_md("### Limpieza de Datos\nConvertimos la fecha, revisamos nulos y corregimos tipos.")

add_code("""# Convertir a datetime
df['fecha_pedido'] = pd.to_datetime(df['fecha_pedido'])

# Revisión de nulos
nulos = df.isnull().sum()
nulos[nulos > 0]""")

add_code("""# Verifiquemos si los nulos de dias_envio corresponden a pedidos cancelados
df[df['dias_envio'].isnull()][['estado_pedido', 'dias_envio']]""")

add_md("## 3. Análisis Univariado y Bivariado\n### Ventas y Evolución Temporal")

add_code("""# Filtramos solo pedidos Completados para ingresos reales
df_completados = df[df['estado_pedido'] == 'Completado'].copy()

# Ventas por fecha
ventas_por_fecha = df_completados.groupby('fecha_pedido')['importe_total_usd'].sum().reset_index()

plt.figure(figsize=(12,5))
sns.lineplot(data=ventas_por_fecha, x='fecha_pedido', y='importe_total_usd', marker='o')
plt.title('Evolución de Ingresos a lo largo del tiempo')
plt.xlabel('Fecha')
plt.ylabel('Ingresos (USD)')
plt.show()""")

add_md("### Rendimiento por Categoría y Segmento")

add_code("""# Ingresos por categoría
ingresos_cat = df_completados.groupby('categoria_producto')['importe_total_usd'].sum().sort_values(ascending=False).reset_index()

plt.figure(figsize=(10,5))
sns.barplot(data=ingresos_cat, x='importe_total_usd', y='categoria_producto', palette='viridis')
plt.title('Ingresos Totales por Categoría de Producto')
plt.xlabel('Ingresos (USD)')
plt.ylabel('Categoría')
plt.show()""")

add_code("""# Comparativa Segmento Cliente vs Ingresos
ingresos_seg = df_completados.groupby('segmento_cliente')['importe_total_usd'].sum().reset_index()
sns.barplot(data=ingresos_seg, x='segmento_cliente', y='importe_total_usd', palette='magma')
plt.title('Ingresos por Segmento de Cliente')
plt.show()""")

add_md("### Análisis de Envíos y Devoluciones")

add_code("""# Tiempos de envío promedio por país (solo completados)
envio_pais = df_completados.groupby('pais_envio')['dias_envio'].mean().sort_values().reset_index()

plt.figure(figsize=(10,5))
sns.barplot(data=envio_pais, x='dias_envio', y='pais_envio', palette='Blues_r')
plt.title('Tiempo de Envío Promedio por País')
plt.xlabel('Días')
plt.ylabel('País')
plt.show()""")

add_code("""# Tasa de Devolución
# Las devoluciones son sobre el total o completados (convertimos a booleano real por seguridad)
if df['devuelto'].dtype == object:
    df['devuelto_bool'] = df['devuelto'].str.lower() == 'true'
else:
    df['devuelto_bool'] = df['devuelto'].astype(bool)

# Calculamos tasa sobre el total de pedidos
tasa_devolucion = df['devuelto_bool'].mean() * 100
print(f"Tasa general de devoluciones: {tasa_devolucion:.2f}%")

# Tasa de devolución por categoría
tasa_dev_cat = df.groupby('categoria_producto')['devuelto_bool'].mean().sort_values() * 100
tasa_dev_cat.plot(kind='barh', color='salmon')
plt.title('Tasa de Devoluciones por Categoría (%)')
plt.xlabel('% de Devolución')
plt.show()""")

add_md("## 4. Interpretación y Comunicación (Insights)\n\n### Hallazgos Clave:\n- **Ingresos y Tendencias:** [Ejecuta el código para observar los resultados de ventas temporales].\n- **Categorías Estrella:** [Ejecuta el código para identificar la categoría con mayor facturación].\n- **Logística (Envíos):** [Ejecuta el código para detectar países con mayores tiempos de envío].\n- **Devoluciones:** [Ejecuta el código para identificar la categoría que más se devuelve].\n\n### Recomendaciones (a validar tras ejecutar):\n1. Enfocar presupuestos de marketing en el **segmento de cliente** y **categorías** más rentables.\n2. Revisar los acuerdos logísticos en los países con tiempos de envío más altos.\n3. Investigar la causa raíz de devoluciones en la categoría con mayor tasa para reducir fricciones.")

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('eda_pedidos.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)
