"""
Generador de dataset ficticio de tareas Kanban (200 filas)
Columnas: task_id, title, status, date_created, date_start,
          date_completed, date_last_moved, assignee,
          priority, task_type, estimated_hours, actual_hours,
          tags, sprint, ticket_url
"""

import csv
import random
from datetime import datetime, timedelta

# ── Semilla para reproducibilidad ──────────────────────────────────────────────
random.seed(42)

# ── Datos de referencia ────────────────────────────────────────────────────────
RESPONSABLES = [
    "Ana García", "Carlos López", "María Fernández", "Luis Martínez",
    "Elena Rodríguez", "Jorge Sánchez", "Laura Pérez", "David Torres",
]

TIPOS = ["Feature", "Bug", "Improvement", "Tech debt", "Research", "Documentation"]
PRIORIDADES = ["High", "Medium", "Low"]
SPRINTS = [f"Sprint-{i}" for i in range(8, 18)]  # Sprint-8 … Sprint-17

TITULOS_BASE = [
    "Implementar {comp} en módulo {mod}",
    "Corregir bug en {comp}",
    "Refactorizar {comp} de {mod}",
    "Documentar API de {mod}",
    "Optimizar rendimiento de {comp}",
    "Añadir tests unitarios a {mod}",
    "Migrar {comp} a nueva versión",
    "Revisar seguridad en {mod}",
    "Diseñar esquema de {comp}",
    "Integrar {comp} con {mod}",
    "Actualizar dependencias de {mod}",
    "Crear dashboard de {comp}",
    "Configurar pipeline CI/CD para {mod}",
    "Analizar métricas de {comp}",
    "Mejorar UX del formulario de {mod}",
]

COMPONENTES = [
    "autenticación", "pagos", "notificaciones", "reportes", "búsqueda",
    "dashboard", "API REST", "base de datos", "caché", "logging",
    "exportación PDF", "importación CSV", "webhooks", "permisos", "facturación",
]

MODULOS = [
    "usuarios", "pedidos", "productos", "clientes", "inventario",
    "analytics", "administración", "marketing", "soporte", "integraciones",
]

ETIQUETAS_POOL = [
    "backend", "frontend", "api", "auth", "db", "ci-cd", "ux",
    "performance", "seguridad", "tests", "refactor", "docs",
]

# ── Fecha de inicio del proyecto ───────────────────────────────────────────────
FECHA_INICIO_PROYECTO = datetime(2024, 1, 2, 8, 0, 0)


def rand_titulo():
    tpl = random.choice(TITULOS_BASE)
    return tpl.format(
        comp=random.choice(COMPONENTES),
        mod=random.choice(MODULOS),
    )


def rand_etiquetas():
    n = random.randint(1, 3)
    return ";".join(random.sample(ETIQUETAS_POOL, n))


def add_hours(dt, hours):
    return dt + timedelta(hours=hours)


def rand_datetime(base, min_h=1, max_h=120):
    """Devuelve un datetime aleatorio entre base+min_h y base+max_h horas."""
    h = random.uniform(min_h, max_h)
    return add_hours(base, h)


def fmt(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""


# ── Generación de filas ────────────────────────────────────────────────────────
rows = []

for i in range(1, 201):
    task_id = f"TASK-{i:04d}"
    titulo = rand_titulo()
    prioridad = random.choice(PRIORIDADES)
    tipo = random.choice(TIPOS)
    responsable = random.choice(RESPONSABLES)
    sprint = random.choice(SPRINTS)
    estimacion = round(random.choice([2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24]), 1)
    etiquetas = rand_etiquetas()
    url = f"https://jira.empresa.com/browse/{task_id}"

    # Fecha creación: distribuida en los primeros 20 semanas del proyecto
    fecha_creacion = rand_datetime(FECHA_INICIO_PROYECTO, min_h=0, max_h=20 * 7 * 24)

    # Determinar estado con distribución realista
    # ~60% Hecho, ~20% En progreso, ~20% Pendiente
    r = random.random()

    if r < 0.60:
        # ── DONE ───────────────────────────────────────────────────────────────
        estado = "Done"
        # Wait time: 1h a 5 días
        fecha_inicio = rand_datetime(fecha_creacion, min_h=1, max_h=5 * 24)
        # Cycle time: 1 día a 15 días (con sesgo hacia tiempos cortos)
        cycle_days = random.expovariate(1 / 4)  # media ~4 días
        cycle_days = max(0.5, min(cycle_days, 30))
        fecha_completado = add_hours(fecha_inicio, cycle_days * 24)
        fecha_ultimo_mov = fecha_completado
        horas_reales = round(estimacion * random.uniform(0.5, 2.5), 1)

    elif r < 0.80:
        # ── IN PROGRESS ────────────────────────────────────────────────────────
        estado = "In progress"
        fecha_inicio = rand_datetime(fecha_creacion, min_h=1, max_h=5 * 24)
        fecha_completado = None
        horas_reales = None
        # Some tasks stagnant (no movement for > 10 days)
        if random.random() < 0.30:
            fecha_ultimo_mov = rand_datetime(fecha_inicio, min_h=1, max_h=3 * 24)
        else:
            fecha_ultimo_mov = rand_datetime(fecha_inicio, min_h=1, max_h=10 * 24)

    else:
        # ── PENDING ────────────────────────────────────────────────────────────
        estado = "Pending"
        fecha_inicio = None
        fecha_completado = None
        fecha_ultimo_mov = fecha_creacion
        horas_reales = None

    rows.append({
        "task_id": task_id,
        "title": titulo,
        "status": estado,
        "date_created": fmt(fecha_creacion),
        "date_start": fmt(fecha_inicio),
        "date_completed": fmt(fecha_completado),
        "date_last_moved": fmt(fecha_ultimo_mov),
        "assignee": responsable if estado != "Pending" or random.random() > 0.3 else "",
        "priority": prioridad,
        "task_type": tipo,
        "estimated_hours": estimacion,
        "actual_hours": horas_reales if horas_reales is not None else "",
        "tags": etiquetas,
        "sprint": sprint,
        "ticket_url": url,
    })

# ── Guardar CSV ────────────────────────────────────────────────────────────────
OUTPUT = r"c:\Users\patfo\Documents\VSC\udemy-ag\files\kanban_dataset.csv"

CAMPOS = [
    "task_id", "title", "status", "date_created", "date_start",
    "date_completed", "date_last_moved", "assignee",
    "priority", "task_type", "estimated_hours", "actual_hours",
    "tags", "sprint", "ticket_url",
]

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=CAMPOS, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(rows)

# ── Resumen ────────────────────────────────────────────────────────────────────
from collections import Counter

estados = Counter(r["status"] for r in rows)
print(f"[OK] Dataset generado: {OUTPUT}")
print(f"   Total filas: {len(rows)}")
print(f"   Status - Done: {estados['Done']} | In progress: {estados['In progress']} | Pending: {estados['Pending']}")
print(f"   Assignees unicos: {len(set(r['assignee'] for r in rows if r['assignee']))}")
print(f"   Task types: {sorted(set(r['task_type'] for r in rows))}")
