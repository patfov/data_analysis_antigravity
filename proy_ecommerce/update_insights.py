import json
import pandas as pd

# Cargar datos
df = pd.read_csv('pedidos_ecommerce_200.csv')
df_completados = df[df['estado_pedido'] == 'Completado']

# Análisis cuantitativo de métodos de pago
ingresos_metodo = df_completados.groupby('metodo_pago')['importe_total_usd'].sum().sort_values(ascending=False)
metodo_top = ingresos_metodo.index[0]
metodo_top_ingreso = ingresos_metodo.iloc[0]
porc_metodo = (metodo_top_ingreso / ingresos_metodo.sum()) * 100

ingresos_pais_metodo = df_completados.groupby(['pais_envio', 'metodo_pago'])['importe_total_usd'].sum().unstack().fillna(0)
# País con más pagos en PayPal
if 'PayPal' in ingresos_pais_metodo.columns:
    pais_paypal = ingresos_pais_metodo['PayPal'].idxmax()
    paypal_monto = ingresos_pais_metodo['PayPal'].max()
else:
    pais_paypal = "N/A"
    paypal_monto = 0

# Modificar el notebook
file_path = r'c:\Users\patfo\Documents\VSC\udemy-ag\proy_ecommerce\eda_pedidos_200.ipynb'
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# La última celda es el markdown con los insights
if nb['cells'][-1]['cell_type'] == 'markdown':
    content = nb['cells'][-1]['source'][0]
    
    insight_text = f"\n- **Métodos de Pago:** El método de pago preferido globalmente es **{metodo_top}**, procesando **${metodo_top_ingreso:.2f} USD** ({porc_metodo:.1f}% de la facturación). Destaca **{pais_paypal}** como el país con mayor volumen procesado mediante PayPal (${paypal_monto:.2f} USD)."
    
    reco_text = f"\n4. **Estrategia de Pagos:** Diseñar alianzas o absorber comisiones del método **{metodo_top}** por ser el más crítico globalmente, y asegurar una experiencia sin fricciones con PayPal en **{pais_paypal}**."
    
    # Dividir e insertar
    if "### Recomendaciones:" in content:
        parts = content.split("### Recomendaciones:")
        new_content = parts[0].rstrip() + insight_text + "\n\n### Recomendaciones:\n" + parts[1].lstrip() + reco_text
    else:
        new_content = content + insight_text + "\n\n" + reco_text
        
    nb['cells'][-1]['source'] = [new_content]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)
