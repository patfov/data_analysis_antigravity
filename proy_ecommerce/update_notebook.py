import pandas as pd
import json

df = pd.read_csv('pedidos_ecommerce.csv')

# Convert dates and booleans
df['fecha_pedido'] = pd.to_datetime(df['fecha_pedido'])
df['devuelto_bool'] = df['devuelto'].astype(str).str.lower() == 'true'

# 1. Ingresos y tendencias
df_completados = df[df['estado_pedido'] == 'Completado']
ingresos_totales = df_completados['importe_total_usd'].sum()
ventas_por_fecha = df_completados.groupby('fecha_pedido')['importe_total_usd'].sum()
mejor_dia = ventas_por_fecha.idxmax().strftime('%Y-%m-%d')
mejor_dia_ingresos = ventas_por_fecha.max()

# 2. Categorías estrella
ingresos_cat = df_completados.groupby('categoria_producto')['importe_total_usd'].sum().sort_values(ascending=False)
cat_estrella = ingresos_cat.index[0]
cat_estrella_ingreso = ingresos_cat.iloc[0]
porcentaje_cat_estrella = (cat_estrella_ingreso / ingresos_totales) * 100

# Segmentos
ingresos_seg = df_completados.groupby('segmento_cliente')['importe_total_usd'].sum().sort_values(ascending=False)
mejor_segmento = ingresos_seg.index[0]
mejor_segmento_ingreso = ingresos_seg.iloc[0]
porc_seg = (mejor_segmento_ingreso / ingresos_totales) * 100

# 3. Logística (Envíos)
envio_pais = df_completados.groupby('pais_envio')['dias_envio'].mean().sort_values(ascending=False)
peor_pais = envio_pais.index[0]
peor_pais_dias = envio_pais.iloc[0]
mejor_pais = envio_pais.index[-1]
mejor_pais_dias = envio_pais.iloc[-1]

# 4. Devoluciones
tasa_devolucion_general = df['devuelto_bool'].mean() * 100
tasa_dev_cat = df.groupby('categoria_producto')['devuelto_bool'].mean().sort_values(ascending=False) * 100
peor_cat_dev = tasa_dev_cat.index[0]
peor_cat_dev_tasa = tasa_dev_cat.iloc[0]

# Construct markdown content
md_content = f"""## 4. Interpretación y Comunicación (Insights)

### Hallazgos Clave (Basados en Datos):
- **Ingresos y Tendencias:** Se generaron un total de **${ingresos_totales:.2f} USD** en pedidos completados. El día con mayores ventas fue el **{mejor_dia}** con ${mejor_dia_ingresos:.2f} USD.
- **Categorías Estrella y Clientes:** La categoría más rentable es **{cat_estrella}**, generando **${cat_estrella_ingreso:.2f} USD** ({porcentaje_cat_estrella:.1f}% del total). Además, el segmento **{mejor_segmento}** es el que más ingresos aporta ({porc_seg:.1f}%).
- **Logística (Envíos):** Los tiempos de envío varían significativamente. **{peor_pais}** tiene los tiempos de entrega promedio más largos (**{peor_pais_dias:.1f} días**), mientras que **{mejor_pais}** es el más rápido ({mejor_pais_dias:.1f} días).
- **Devoluciones:** La tasa general de devoluciones es del **{tasa_devolucion_general:.1f}%**. La categoría con mayor problema de devoluciones es **{peor_cat_dev}**, con una preocupante tasa del **{peor_cat_dev_tasa:.1f}%**.

### Recomendaciones:
1. **Foco Comercial:** Aumentar el presupuesto de marketing dirigido al segmento **{mejor_segmento}** promocionando principalmente productos de **{cat_estrella}**, ya que son los impulsores actuales de ingresos.
2. **Optimización Logística:** Es urgente revisar los acuerdos con los proveedores logísticos en **{peor_pais}**, dado que {peor_pais_dias:.1f} días de promedio pueden afectar severamente la retención de clientes allí.
3. **Control de Calidad en {peor_cat_dev}:** Investigar inmediatamente los productos de la categoría **{peor_cat_dev}** (por ejemplo, tallas, calidad de fotos vs producto real), ya que una tasa de devolución del {peor_cat_dev_tasa:.1f}% destruye el margen de beneficio."""

with open('eda_pedidos.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# The last cell should be the markdown cell
if nb['cells'][-1]['cell_type'] == 'markdown' and 'Hallazgos Clave' in nb['cells'][-1]['source'][0]:
    nb['cells'][-1]['source'] = [md_content]
else:
    nb['cells'].append({"cell_type": "markdown", "metadata": {}, "source": [md_content]})

with open('eda_pedidos.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)
