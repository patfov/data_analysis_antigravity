# Data Analysis Workspace

This repository houses data analysis projects focused on E-Commerce behavior and Kanban task flow metrics. 

## 🤖 Agentic Development

This repository was created, configured, and developed using **Agentic Development with Antigravity**—an agentic AI coding assistant designed by Google DeepMind. The agent assisted in generating the data simulation scripts, structuring the project directories, implementing EDA notebooks, setting up Git configuration, and orchestrating the initial deployment to GitHub.

---

## 📂 Project Structure

The workspace is organized into two main projects:

### 1. E-Commerce Orders Analysis (`proy_ecommerce`)
This project focuses on simulating and analyzing e-commerce transactions, including payment methods, status transitions, and customer insights.
* **Jupyter Notebooks**: Exploratory Data Analysis (EDA) of simulated order histories (`eda_pedidos.ipynb`, `eda_pedidos_200.ipynb`).
* **Python Scripts**: 
  * `generar_200.py` & `generate_notebook.py`: Data generators and template builders.
  * `update_insights.py` & `update_insights_full.py`: Automated parsing of business insights.
  * `update_notebook.py` & `update_notebook_pago.py`: Utilities to update notebooks dynamically.
* **Datasets**: Simulated transaction databases in CSV format.

### 2. Kanban Board Metrics (`proy_kanban`)
This project implements metrics and KPIs to measure development workflow speed, throughput, and bottleneck detection on a Kanban board.
* **Jupyter Notebooks**: Workflow and cycle-time EDA (`eda.ipynb`).
* **Documentation**: Data quality checklists, data schemas, and metric specification standards (`files/`).
* **Python Scripts**: Synthetic Kanban events generator (`files/generar_dataset.py`).

---

## ⚙️ Environment and Dependencies

This project is configured to run inside a Python virtual environment (`.venv`) using the following core libraries for data processing, analysis, and visualization:

* **pandas**: For data manipulation, cleaning, and analysis.
* **numpy**: For numerical computing and mathematical operations.
* **matplotlib**: For generating static and interactive visualizations.
* **seaborn**: For high-level statistical data visualization.
* **jupyter / jupyterlab**: For interactive development and exploratory data analysis (EDA).

