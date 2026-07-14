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

## ⚙️ How to Run Locally

### Prerequisites
* Python 3.10+
* Jupyter Notebook / JupyterLab

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/patfov/data_analysis_antigravity.git
   cd data_analysis_antigravity
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```
3. Install dependencies and open Jupyter to explore:
   ```bash
   pip install pandas numpy matplotlib seaborn jupyter
   jupyter lab
   ```
