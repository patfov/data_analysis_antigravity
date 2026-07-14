import json
import pandas as pd

# Load data
df = pd.read_csv('pedidos_ecommerce_200.csv')
df['fecha_pedido'] = pd.to_datetime(df['fecha_pedido'])
df['devuelto_bool'] = df['devuelto'].astype(str).str.lower() == 'true'
df_completados = df[df['estado_pedido'] == 'Completado']

# --- Calculate Insights ---
# 1. Ingresos
ingresos_totales = df_completados['importe_total_usd'].sum()
ventas_por_fecha = df_completados.groupby('fecha_pedido')['importe_total_usd'].sum()
mejor_dia = ventas_por_fecha.idxmax().strftime('%Y-%m-%d')
mejor_dia_ingresos = ventas_por_fecha.max()

# 2. Categorias y clientes
ingresos_cat = df_completados.groupby('categoria_producto')['importe_total_usd'].sum().sort_values(ascending=False)
cat_estrella = ingresos_cat.index[0]
cat_estrella_ingreso = ingresos_cat.iloc[0]
porcentaje_cat_estrella = (cat_estrella_ingreso / ingresos_totales) * 100

ingresos_seg = df_completados.groupby('segmento_cliente')['importe_total_usd'].sum().sort_values(ascending=False)
mejor_segmento = ingresos_seg.index[0]
mejor_segmento_ingreso = ingresos_seg.iloc[0]
porc_seg = (mejor_segmento_ingreso / ingresos_totales) * 100

# 3. Envios
df_completados_copy = df_completados.copy()
df_completados_copy['dias_envio'] = pd.to_numeric(df_completados_copy['dias_envio'], errors='coerce')
envio_pais = df_completados_copy.groupby('pais_envio')['dias_envio'].mean().sort_values(ascending=False)
peor_pais = envio_pais.index[0]
peor_pais_dias = envio_pais.iloc[0]
mejor_pais = envio_pais.index[-1]
mejor_pais_dias = envio_pais.iloc[-1]

# 4. Devoluciones
tasa_devolucion_general = df['devuelto_bool'].mean() * 100
tasa_dev_cat = df.groupby('categoria_producto')['devuelto_bool'].mean().sort_values(ascending=False) * 100
peor_cat_dev = tasa_dev_cat.index[0]
peor_cat_dev_tasa = tasa_dev_cat.iloc[0]

# 5. Metodos de pago
ingresos_metodo = df_completados.groupby('metodo_pago')['importe_total_usd'].sum().sort_values(ascending=False)
metodo_top = ingresos_metodo.index[0]
metodo_top_ingreso = ingresos_metodo.iloc[0]
porc_metodo = (metodo_top_ingreso / ingresos_metodo.sum()) * 100

ingresos_pais_metodo = df_completados.groupby(['pais_envio', 'metodo_pago'])['importe_total_usd'].sum().unstack().fillna(0)
if 'PayPal' in ingresos_pais_metodo.columns:
    pais_paypal = ingresos_pais_metodo['PayPal'].idxmax()
    paypal_monto = ingresos_pais_metodo['PayPal'].max()
else:
    pais_paypal = "N/A"
    paypal_monto = 0

md_content = f"""## 4. Interpretación y Comunicación (Insights)

### Hallazgos Clave (Dataset 200 Pedidos):
- **Ingresos y Tendencias:** Se generaron un total de **${ingresos_totales:.2f} USD** en pedidos completados en este trimestre ficticio. El mejor día de ventas fue el **{mejor_dia}** con ${mejor_dia_ingresos:.2f} USD.
- **Categorías Estrella y Clientes:** La categoría de mayores ingresos es **{cat_estrella}**, facturando **${cat_estrella_ingreso:.2f} USD** ({porcentaje_cat_estrella:.1f}% del total). El segmento de cliente **{mejor_segmento}** representa la mayor fuente de ingresos ({porc_seg:.1f}%).
- **Logística (Envíos):** **{peor_pais}** tiene los envíos más lentos (**{peor_pais_dias:.1f} días** en promedio), mientras que **{mejor_pais}** es el más veloz ({mejor_pais_dias:.1f} días).
- **Devoluciones:** La tasa general de devoluciones se sitúa en un **{tasa_devolucion_general:.1f}%**. La categoría más crítica es **{peor_cat_dev}**, con una tasa de devolución del **{peor_cat_dev_tasa:.1f}%**, destacando sobre el resto.
- **Métodos de Pago:** El método de pago preferido globalmente es **{metodo_top}**, procesando **${metodo_top_ingreso:.2f} USD** ({porc_metodo:.1f}% de la facturación). Destaca **{pais_paypal}** como el país con mayor volumen procesado mediante PayPal (${paypal_monto:.2f} USD).

### Recomendaciones:
1. **Foco Comercial:** Invertir en campañas de fidelización para clientes **{mejor_segmento}** y destacar el inventario de **{cat_estrella}**.
2. **Optimización Logística:** Negociar con los couriers en **{peor_pais}** para mejorar los tiempos de entrega.
3. **Control de Calidad en {peor_cat_dev}:** Debido al alto índice de devoluciones ({peor_cat_dev_tasa:.1f}%), se recomienda inspeccionar las descripciones, tallaje o calidad de los productos de esta categoría.
4. **Estrategia de Pagos:** Diseñar alianzas o absorber comisiones del método **{metodo_top}** por ser el más crítico globalmente, y asegurar una experiencia sin fricciones con PayPal en **{pais_paypal}**."""

# Modificar el notebook
file_path = r'c:\Users\patfo\Documents\VSC\udemy-ag\proy_ecommerce\eda_pedidos_200.ipynb'
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# The last cell is the markdown with insights
if nb['cells'][-1]['cell_type'] == 'markdown':
    nb['cells'][-1]['source'] = [md_content]
else:
    nb['cells'].append({"cell_type": "markdown", "metadata": {}, "source": [md_content]})

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)
