# 🔍 Auditoría de Calidad de Datos — Dataset Kanban

> **Dataset:** `kanban_dataset.csv` · **Total de filas:** 200 tareas · **Columnas:** 15  
> **Fecha de auditoría:** 2024-08-01 (fecha de referencia del análisis)

---

## Resumen Ejecutivo

| Dimensión | Hallazgos | Severidad |
|-----------|-----------|:---------:|
| Valores faltantes | `date_completed` y `actual_hours` ausentes en el 39.5% de filas (esperado por diseño) | 🟡 Media |
| `assignee` nulo | 11 tareas sin responsable asignado | 🟡 Media |
| Integridad de fechas | **0 violaciones** — todas las reglas R1–R7 se cumplen | 🟢 OK |
| Outliers Cycle Time | 2 tareas con cycle time > 12 días (máx: 22.8 días) | 🟡 Media |
| Outliers Lead Time | 2 tareas con lead time > 14 días (máx: 24.5 días) | 🟡 Media |
| Outliers actual_hours | 4 tareas con horas reales > 36h (máx: 46.2h) | 🟡 Media |
| Tareas estancadas | **43 de 43 tareas "In progress"** llevan >10 días sin moverse | 🔴 Alta |
| Sesgo de distribución | `priority` uniformemente distribuida (irreal) | 🟠 Moderada |
| Sesgo de carga | `Carlos López` tiene 31 tareas vs. `María Fernández` con 16 | 🟠 Moderada |

---

## Problemas Priorizados

---

### 🔴 P1 — CRÍTICO: Todas las tareas "In progress" están estancadas

**Descripción:**  
Las 43 tareas con `status = In progress` llevan entre **10 y 205 días** sin ningún cambio en `date_last_moved`. Las 5 más críticas:

| task_id | Días sin mover |
|---------|---------------:|
| TASK-0170 | 205 días |
| TASK-0010 | 199 días |
| TASK-0046 | 196 días |
| TASK-0045 | 195 días |
| TASK-0068 | 195 días |

**Causa probable:** El `date_last_moved` se fijó al inicio pero nunca se actualizó al avanzar la tarea; o las tareas están genuinamente bloqueadas.

**Cómo corregirlo:**
1. **Auditar manualmente** si las tareas siguen activas o deben cerrarse/rechazarse.
2. Si el campo no se actualiza automáticamente, implementar un **webhook** o trigger que registre cada movimiento de columna.
3. Definir una **política de WIP limits** y una alerta automática para tareas sin movimiento > 5 días.

```python
# Detección de tareas estancadas
from datetime import datetime
REF = datetime(2024, 8, 1)
stagnant = [(r['task_id'], (REF - parse(r['date_last_moved'])).days)
            for r in rows
            if r['status'] == 'In progress' and r['date_last_moved']]
stagnant.sort(key=lambda x: -x[1])
```

---

### 🟠 P2 — MODERADO: Valores faltantes en `assignee` (5.5%)

**Descripción:**  
11 tareas no tienen responsable asignado (`assignee` vacío). Algunas son tareas `Pending`, lo cual es aceptable, pero otras podrían estar en progreso sin owner claro.

```
assignee nulo: 11/200 (5.5%)
```

**Impacto:** Imposible calcular "carga por responsable" correctamente; sesga los promedios de ciclo por persona.

**Cómo corregirlo:**
1. **Regla de negocio:** toda tarea que pase a `In progress` debe tener `assignee` obligatorio (validación en el tablero).
2. **Para el dataset actual:** imputar con categoría `"Unassigned"` para no perder las filas en análisis.

```python
for r in rows:
    if not r['assignee']:
        r['assignee'] = 'Unassigned'
```

---

### 🟠 P3 — MODERADO: Outliers en `actual_hours` (4 casos)

**Descripción:**  
4 tareas reportan más de 36.6 horas reales (fence IQR superior), con un máximo de **46.2 horas**. Esto puede representar tareas de múltiples días, errores de registro, o trabajo concentrado en sprints intensivos.

| Estadística | Valor |
|-------------|------:|
| Media | 13.65 h |
| Mediana | 10.20 h |
| Máximo | **46.20 h** |
| Fence IQR superior | 36.60 h |
| Casos outlier | **4 tareas** |

**Cómo corregirlo:**
1. **Verificar manualmente** si son tareas multi-jornada (aceptable) o errores de entrada de datos.
2. Si son errores, corregir o imputar con la mediana del mismo `task_type`.
3. Añadir una **validación en captura**: `actual_hours` no puede superar `cycle_time_days × 8`.

```python
# Detectar outliers por IQR
import statistics
vals = [float(r['actual_hours']) for r in rows if r['actual_hours']]
q1, q3 = statistics.quantiles(vals, n=4)[0], statistics.quantiles(vals, n=4)[2]
fence = q3 + 1.5 * (q3 - q1)
outliers = [r for r in rows if r['actual_hours'] and float(r['actual_hours']) > fence]
```

---

### 🟡 P4 — MEDIO: Outliers en Cycle Time y Lead Time (2 casos cada uno)

**Descripción:**  
2 tareas superan el fence IQR del Cycle Time (>12.1 días, máx. 22.8 días) y 2 tareas superan el fence del Lead Time (>14.2 días, máx. 24.5 días). Estos pueden ser tareas legítimamente complejas o bloqueadas.

| Métrica | Media | Mediana | Máx | Fence superior | Outliers |
|---------|------:|--------:|----:|---------------:|---------:|
| Cycle Time | 3.74 d | 2.51 d | 22.77 d | 12.12 d | **2** |
| Lead Time | 6.36 d | 5.61 d | 24.52 d | 14.18 d | **2** |

**Cómo corregirlo:**
1. **No eliminarlos:** pueden ser datos válidos (tareas complejas o bloqueadas).
2. **Segmentarlos:** analizar por separado `task_type = 'Research'` o `'Tech debt'` que suelen tener ciclos más largos.
3. **Reportar percentiles** P50/P85/P95 en lugar de media aritmética para que los outliers no distorsionen la métrica.

```python
# Reportar percentiles en lugar de media
import statistics
ct_sorted = sorted(cycle_times)
n = len(ct_sorted)
p50 = ct_sorted[n//2]
p85 = ct_sorted[int(n*0.85)]
p95 = ct_sorted[int(n*0.95)]
```

---

### 🟡 P5 — MEDIO: Nulos esperados pero sin documentar en `date_completed` y `actual_hours` (39.5%)

**Descripción:**  
79 tareas (39.5%) tienen `date_completed` y `actual_hours` vacíos porque su `status` es `Pending` o `In progress`. Esto es **correcto por diseño**, pero puede causar errores si se procesan sin filtrado previo.

**Impacto:** Si se calcula Cycle Time o Lead Time sin filtrar `status = Done`, se obtendrán `NaN` o errores que contaminarán el análisis.

**Cómo corregirlo:**
1. **Documentar explícitamente** que los nulos son estructurales (MCAR — Missing Completely At Random por diseño).
2. **Filtrar siempre** antes de calcular métricas temporales:

```python
done_rows = [r for r in rows if r['status'] == 'Done']
# Solo sobre done_rows calcular cycle_time, lead_time, actual_hours
```

3. Añadir una columna `is_complete` (bool) para facilitar filtrado sin recordar la lógica cada vez.

---

### 🟡 P6 — MEDIO: Distribución de prioridad artificialmente uniforme

**Descripción:**  
La prioridad está distribuida de forma casi perfectamente uniforme:

| Priority | Count | % |
|----------|------:|--:|
| High | 66 | 33% |
| Medium | 65 | 32.5% |
| Low | 69 | 34.5% |

En equipos reales, la distribución típica es asimétrica: más tareas de baja prioridad en backlog, mayor concentración de alta prioridad en progreso.

**Impacto:** Si se usa este dataset para entrenar un modelo de priorización, generará predicciones sesgadas hacia distribuciones uniformes.

**Cómo corregirlo (para dataset real):**
- Capturar prioridad directamente del tablero sin normalización artificial.
- En análisis, segmentar por `status` y `priority` juntos para detectar si la alta prioridad realmente se resuelve antes.

---

### 🟡 P7 — MEDIO: Desbalance de carga entre responsables

**Descripción:**  
La distribución de tareas entre responsables es desigual, con una diferencia del **~2x** entre el más cargado y el menos:

| Assignee | Tareas |
|----------|-------:|
| Carlos López | 31 |
| Luis Martínez | 27 |
| Jorge Sánchez | 25 |
| Elena Rodríguez | 25 |
| Laura Pérez | 25 |
| David Torres | 21 |
| Ana García | 19 |
| María Fernández | 16 |

**Impacto:** Las métricas de Cycle Time promedio por persona pueden estar sesgadas si el tipo de tarea asignada a cada uno difiere sistemáticamente.

**Cómo corregirlo:**
- Al analizar rendimiento individual, controlar siempre por `task_type` y `priority` para comparar "peras con peras".
- No usar el conteo de tareas como proxy directo de carga (una tarea Research puede equivaler a 5 Bug fixes).

---

## Checklist de Limpieza Recomendada

Antes de pasar al análisis exploratorio (EDA), aplicar en este orden:

- [ ] **Filtrar** tareas `Done` para métricas temporales (`date_completed` no nulo)
- [ ] **Imputar** `assignee` nulo → `"Unassigned"`
- [ ] **Auditar** manualmente las 4 tareas con `actual_hours > 36.6h`
- [ ] **Marcar** los 2 outliers de Cycle Time y Lead Time con flag `is_outlier = True` (no eliminar)
- [ ] **Alertar** sobre las 43 tareas `In progress` estancadas para revisión de negocio
- [ ] **Documentar** los nulos en `date_completed` como MCAR estructural (no problema de calidad)
- [ ] **Añadir columna** `cycle_time_days` y `lead_time_days` calculadas y limpias para facilitar el EDA

---

## Supuestos y Limitaciones del Dataset

> [!NOTE]
> Estas limitaciones son propias del dataset **sintético** y deben considerarse al interpretar cualquier resultado.

1. **Dataset sintético:** Los datos fueron generados con distribuciones estadísticas controladas (semilla 42), no reflejan patrones de trabajo real.
2. **Fechas acotadas:** Las tareas se distribuyen entre enero y mayo de 2024 (~20 semanas). No hay suficiente historia para detectar tendencias de largo plazo.
3. **Sin historial de estados:** Solo se captura el estado actual, no la secuencia de transiciones. Imposible detectar si una tarea retrocedió de "In progress" a "Pending".
4. **Títulos genéricos:** Los títulos generados con plantilla no permiten clasificación semántica real.
5. **Sin dependencias entre tareas:** En proyectos reales, el bloqueo de una tarea puede estar causado por la dependencia de otra.
6. **Wait Time artificialmente comprimido:** El tiempo de espera (date_created → date_start) tiene un rango muy estrecho (0.08–4.98 días) comparado con proyectos reales donde puede haber semanas de backlog.
