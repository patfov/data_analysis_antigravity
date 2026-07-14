import json

file_path = r'c:\Users\patfo\Documents\VSC\udemy-ag\proy_ecommerce\eda_pedidos_200.ipynb'

with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Create the new cells
md_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Análisis de Métodos de Pago por País y Montos"
    ]
}

code_source = """# Ingresos por país y método de pago
ingresos_pais_metodo = df_completados.groupby(['pais_envio', 'metodo_pago'])['importe_total_usd'].sum().reset_index()

plt.figure(figsize=(12, 6))
sns.barplot(data=ingresos_pais_metodo, x='pais_envio', y='importe_total_usd', hue='metodo_pago', palette='Set2')
plt.title('Ingresos por País y Método de Pago')
plt.xlabel('País')
plt.ylabel('Ingresos Totales (USD)')
plt.legend(title='Método de Pago')
plt.show()"""

code_cell = {
    "cell_type": "code",
    "metadata": {},
    "outputs": [],
    "execution_count": None,
    "source": [code_source]
}

# Insert before the final Interpretacion markdown cell
if nb['cells'][-1]['cell_type'] == 'markdown' and 'Interpretación y Comunicación' in nb['cells'][-1]['source'][0]:
    nb['cells'].insert(-1, md_cell)
    nb['cells'].insert(-1, code_cell)
else:
    nb['cells'].append(md_cell)
    nb['cells'].append(code_cell)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)
