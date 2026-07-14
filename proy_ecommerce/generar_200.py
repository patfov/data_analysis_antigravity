import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import json

# Fijar semilla para reproducibilidad
random.seed(42)

# Categorías y productos originales
categorias = ['Electrónica', 'Hogar', 'Moda', 'Accesorios']
productos_por_cat = {
    'Electrónica': [('Auriculares Bluetooth', 59.99), ('Teclado Mecánico', 89.90), ('Monitor 27 pulgadas', 249.99), ('Ratón Inalámbrico', 25.00), ('Tablet 10 pulgadas', 199.00), ('Altavoz Portátil', 99.99), ('Smartwatch', 179.00), ('Webcam HD', 69.90), ('Disco SSD 1TB', 109.00), ('Router WiFi', 129.00)],
    'Hogar': [('Cafetera Italiana', 34.50), ('Lámpara de Escritorio', 45.00), ('Set de Sartenes', 99.00), ('Aspiradora de Mano', 89.00), ('Lámpara de Techo', 120.00), ('Hervidor Eléctrico', 39.99), ('Tostadora', 29.90)],
    'Moda': [('Camiseta Negra', 15.00), ('Zapatillas Running', 120.00), ('Chaqueta Vaquera', 79.00), ('Sudadera Gris', 49.90), ('Camiseta Blanca', 15.00), ('Pantalón Chino', 55.00), ('Abrigo de Invierno', 149.00), ('Zapatos de Vestir', 89.00), ('Bufanda de Lana', 22.00)],
    'Accesorios': [('Funda iPhone', 19.99), ('Mochila Urbana', 65.00), ('Gorra Deportiva', 18.00), ('Cartera de Piel', 59.00)]
}
segmentos = ['Nuevo', 'Recurrente']
metodos = ['Tarjeta', 'PayPal']
estados = ['Completado', 'Cancelado']
paises = ['España', 'Francia', 'Alemania', 'Italia', 'Portugal']

data = []
start_date = datetime(2027, 1, 1)

for i in range(200):
    id_pedido = f"PED-{3000+i}"
    fecha_pedido = (start_date + timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d')
    id_cliente = f"CLI-{random.randint(1, 100):03d}"
    segmento = random.choice(segmentos)
    categoria = random.choice(categorias)
    producto, precio = random.choice(productos_por_cat[categoria])
    unidades = random.choices([1, 2, 3, 4], weights=[70, 20, 8, 2])[0]
    importe = round(precio * unidades, 2)
    metodo = random.choice(metodos)
    estado = random.choices(estados, weights=[90, 10])[0]
    pais = random.choice(paises)
    
    if estado == 'Cancelado':
        dias_envio = ""
        devuelto = "false"
    else:
        dias_envio = str(random.randint(2, 8))
        # Moda podría tener mayor tasa de devolución
        ret_prob = 0.18 if categoria == 'Moda' else 0.04
        devuelto = "true" if random.random() < ret_prob else "false"
        
    data.append([id_pedido, fecha_pedido, id_cliente, segmento, categoria, producto, unidades, precio, importe, metodo, estado, pais, dias_envio, devuelto])

df = pd.DataFrame(data, columns=['id_pedido','fecha_pedido','id_cliente','segmento_cliente','categoria_producto','nombre_producto','unidades','precio_unitario_usd','importe_total_usd','metodo_pago','estado_pedido','pais_envio','dias_envio','devuelto'])

csv_file = 'pedidos_ecommerce_200.csv'
df.to_csv(csv_file, index=False)

# --- ANÁLISIS ---
df['fecha_pedido'] = pd.to_datetime(df['fecha_pedido'])
df['devuelto_bool'] = df['devuelto'].astype(str).str.lower() == 'true'

df_completados = df[df['estado_pedido'] == 'Completado']
ingresos_totales = df_completados['importe_total_usd'].sum()
ventas_por_fecha = df_completados.groupby('fecha_pedido')['importe_total_usd'].sum()
mejor_dia = ventas_por_fecha.idxmax().strftime('%Y-%m-%d')
mejor_dia_ingresos = ventas_por_fecha.max()

ingresos_cat = df_completados.groupby('categoria_producto')['importe_total_usd'].sum().sort_values(ascending=False)
cat_estrella = ingresos_cat.index[0]
cat_estrella_ingreso = ingresos_cat.iloc[0]
porcentaje_cat_estrella = (cat_estrella_ingreso / ingresos_totales) * 100

ingresos_seg = df_completados.groupby('segmento_cliente')['importe_total_usd'].sum().sort_values(ascending=False)
mejor_segmento = ingresos_seg.index[0]
mejor_segmento_ingreso = ingresos_seg.iloc[0]
porc_seg = (mejor_segmento_ingreso / ingresos_totales) * 100

df_completados = df_completados.copy()
df_completados['dias_envio'] = pd.to_numeric(df_completados['dias_envio'], errors='coerce')
envio_pais = df_completados.groupby('pais_envio')['dias_envio'].mean().sort_values(ascending=False)
peor_pais = envio_pais.index[0]
peor_pais_dias = envio_pais.iloc[0]
mejor_pais = envio_pais.index[-1]
mejor_pais_dias = envio_pais.iloc[-1]

tasa_devolucion_general = df['devuelto_bool'].mean() * 100
tasa_dev_cat = df.groupby('categoria_producto')['devuelto_bool'].mean().sort_values(ascending=False) * 100
peor_cat_dev = tasa_dev_cat.index[0]
peor_cat_dev_tasa = tasa_dev_cat.iloc[0]

md_content = f"""## 4. Interpretación y Comunicación (Insights)

### Hallazgos Clave (Dataset 200 Pedidos):
- **Ingresos y Tendencias:** Se generaron un total de **${ingresos_totales:.2f} USD** en pedidos completados en este trimestre ficticio. El mejor día de ventas fue el **{mejor_dia}** con ${mejor_dia_ingresos:.2f} USD.
- **Categorías Estrella y Clientes:** La categoría de mayores ingresos es **{cat_estrella}**, facturando **${cat_estrella_ingreso:.2f} USD** ({porcentaje_cat_estrella:.1f}% del total). El segmento de cliente **{mejor_segmento}** representa la mayor fuente de ingresos ({porc_seg:.1f}%).
- **Logística (Envíos):** **{peor_pais}** tiene los envíos más lentos (**{peor_pais_dias:.1f} días** en promedio), mientras que **{mejor_pais}** es el más veloz ({mejor_pais_dias:.1f} días).
- **Devoluciones:** La tasa general de devoluciones se sitúa en un **{tasa_devolucion_general:.1f}%**. La categoría más crítica es **{peor_cat_dev}**, con una tasa de devolución del **{peor_cat_dev_tasa:.1f}%**, destacando sobre el resto.

### Recomendaciones:
1. **Foco Comercial:** Invertir en campañas de fidelización para clientes **{mejor_segmento}** y destacar el inventario de **{cat_estrella}**.
2. **Optimización Logística:** Negociar con los couriers en **{peor_pais}** para mejorar los tiempos de entrega.
3. **Control de Calidad en {peor_cat_dev}:** Debido al alto índice de devoluciones ({peor_cat_dev_tasa:.1f}%), se recomienda inspeccionar las descripciones, tallaje o calidad de los productos de esta categoría."""

cells = []
def add_md(text): cells.append({"cell_type": "markdown", "metadata": {}, "source": [text]})
def add_code(code): cells.append({"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": None, "source": [code]})

add_md("# Análisis Exploratorio de Datos (EDA) - E-commerce (200 Pedidos)\n\nEste notebook contiene el EDA para el nuevo dataset ampliado de pedidos de e-commerce con 200 filas.")
add_md("## 1. Entender el Problema\n\n**Objetivo:** Analizar 200 pedidos generados aleatoriamente basándose en la estructura original.")
add_md("## 2. Exploración y Preparación de Datos")
add_code("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\nsns.set_theme(style=\"whitegrid\")\nplt.rcParams['figure.figsize'] = (10, 6)\n\ndf = pd.read_csv('pedidos_ecommerce_200.csv')\ndf.head()")
add_code("df.info()")
add_md("### Limpieza de Datos")
add_code("df['fecha_pedido'] = pd.to_datetime(df['fecha_pedido'])\nnulos = df.isnull().sum()\nnulos[nulos > 0]")
add_code("df[df['dias_envio'].isnull()][['estado_pedido', 'dias_envio']].head()")
add_md("## 3. Análisis Univariado y Bivariado\n### Ventas y Evolución Temporal")
add_code("df_completados = df[df['estado_pedido'] == 'Completado'].copy()\n\nventas_por_fecha = df_completados.groupby('fecha_pedido')['importe_total_usd'].sum().reset_index()\n\nplt.figure(figsize=(12,5))\nsns.lineplot(data=ventas_por_fecha, x='fecha_pedido', y='importe_total_usd', marker='o')\nplt.title('Evolución de Ingresos a lo largo del tiempo')\nplt.xlabel('Fecha')\nplt.ylabel('Ingresos (USD)')\nplt.show()")
add_md("### Rendimiento por Categoría y Segmento")
add_code("ingresos_cat = df_completados.groupby('categoria_producto')['importe_total_usd'].sum().sort_values(ascending=False).reset_index()\n\nplt.figure(figsize=(10,5))\nsns.barplot(data=ingresos_cat, x='importe_total_usd', y='categoria_producto', palette='viridis')\nplt.title('Ingresos Totales por Categoría de Producto')\nplt.xlabel('Ingresos (USD)')\nplt.ylabel('Categoría')\nplt.show()")
add_code("ingresos_seg = df_completados.groupby('segmento_cliente')['importe_total_usd'].sum().reset_index()\nsns.barplot(data=ingresos_seg, x='segmento_cliente', y='importe_total_usd', palette='magma')\nplt.title('Ingresos por Segmento de Cliente')\nplt.show()")
add_md("### Análisis de Envíos y Devoluciones")
add_code("envio_pais = df_completados.groupby('pais_envio')['dias_envio'].mean().sort_values().reset_index()\n\nplt.figure(figsize=(10,5))\nsns.barplot(data=envio_pais, x='dias_envio', y='pais_envio', palette='Blues_r')\nplt.title('Tiempo de Envío Promedio por País')\nplt.xlabel('Días')\nplt.ylabel('País')\nplt.show()")
add_code("if df['devuelto'].dtype == object:\n    df['devuelto_bool'] = df['devuelto'].str.lower() == 'true'\nelse:\n    df['devuelto_bool'] = df['devuelto'].astype(bool)\n\ntasa_devolucion = df['devuelto_bool'].mean() * 100\nprint(f\"Tasa general de devoluciones: {tasa_devolucion:.2f}%\")\n\ntasa_dev_cat = df.groupby('categoria_producto')['devuelto_bool'].mean().sort_values() * 100\ntasa_dev_cat.plot(kind='barh', color='salmon')\nplt.title('Tasa de Devoluciones por Categoría (%)')\nplt.xlabel('% de Devolución')\nplt.show()")
add_md(md_content)

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

with open('eda_pedidos_200.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)
