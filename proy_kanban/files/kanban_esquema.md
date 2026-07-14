# 🗂️ Esquema de Dataset — Ciclo de Vida de Tareas Kanban

> Documento de referencia para estructurar la captura de datos de un tablero Kanban con columnas: `Pending → In progress → Done`

---

## Resumen de Columnas

| # | Columna | Tipo | Obligatorio | Descripción |
|---|---------|------|:-----------:|-------------|
| 1 | `task_id` | String | ✅ | Identificador único de la tarea |
| 2 | `title` | String | ✅ | Descripción corta de la tarea |
| 3 | `status` | Enum | ✅ | Estado actual en el tablero |
| 4 | `date_created` | DateTime (ISO 8601) | ✅ | Momento en que la tarea se añadió al backlog |
| 5 | `date_start` | DateTime (ISO 8601) | ⚠️ Recomendado | Momento en que se movió a "In progress" |
| 6 | `date_completed` | DateTime (ISO 8601) | ⚠️ Recomendado | Momento en que se movió a "Done" |
| 7 | `date_last_moved` | DateTime (ISO 8601) | ⚠️ Recomendado | Último cambio de estado (para detectar estancamiento) |
| 8 | `assignee` | String | ⚠️ Recomendado | Persona asignada a la tarea |
| 9 | `priority` | Enum | Opcional | Prioridad de negocio de la tarea |
| 10 | `task_type` | Enum | Opcional | Categoría funcional de la tarea |
| 11 | `estimated_hours` | Float | Opcional | Estimación inicial en horas |
| 12 | `actual_hours` | Float | Opcional | Horas reales invertidas (si se registran) |
| 13 | `tags` | String (lista sep. por `;`) | Opcional | Tags libres para filtrado |
| 14 | `sprint` | String | Opcional | Nombre o número del sprint/iteración |
| 15 | `ticket_url` | String (URL) | Opcional | Enlace al ticket en la herramienta (Jira, Trello, etc.) |

---

## Detalle por Columna

### 1. `task_id`
- **Tipo:** String
- **Obligatorio:** ✅ Sí
- **Descripción:** Identificador único e inmutable de cada tarea. Nunca debe reutilizarse.
- **Formato recomendado:** `TASK-0001`, `TASK-0002`, …
- **Ejemplo:** `TASK-0042`
- **Restricciones:** No nulo, único en el dataset

---

### 2. `title`
- **Tipo:** String (máx. 150 caracteres)
- **Obligatorio:** ✅ Sí
- **Descripción:** Descripción concisa de lo que hay que hacer. Debe ser autoexplicativa.
- **Ejemplo:** `"Implement OAuth2 authentication endpoint"`
- **Restricciones:** No nulo, longitud > 5 caracteres

---

### 3. `status`
- **Tipo:** Enum (valores controlados)
- **Obligatorio:** ✅ Sí
- **Valores válidos:**

| Valor | Significado |
|-------|-------------|
| `Pending` | Creada pero sin iniciar |
| `In progress` | Asignada y en desarrollo activo |
| `Done` | Completada y entregada |

- **Ejemplo:** `"In progress"`
- **Restricciones:** Solo acepta los tres valores del Enum. Evitar variantes como "Hecho", "Terminado", etc.

---

### 4. `date_created`
- **Tipo:** DateTime (ISO 8601)
- **Obligatorio:** ✅ Sí
- **Descripción:** Timestamp del momento exacto en que la tarea fue creada en el sistema.
- **Formato:** `YYYY-MM-DD HH:MM:SS` o `YYYY-MM-DDTHH:MM:SSZ`
- **Ejemplo:** `2024-03-15 09:23:00`
- **Restricciones:** No nulo; debe ser ≤ `date_start` y ≤ `date_completed`

---

### 5. `date_start`
- **Tipo:** DateTime (ISO 8601)
- **Obligatorio:** ⚠️ Recomendado (nulo si status = `Pending`)
- **Descripción:** Momento en que la tarea pasó a "In progress". Necesario para calcular **Cycle Time** y **Wait Time**.
- **Ejemplo:** `2024-03-18 14:05:00`
- **Restricciones:** Si no es nulo, debe ser ≥ `date_created` y ≤ `date_completed`

---

### 6. `date_completed`
- **Tipo:** DateTime (ISO 8601)
- **Obligatorio:** ⚠️ Recomendado (nulo si status ≠ `Done`)
- **Descripción:** Momento en que la tarea pasó a "Done". Necesario para **Lead Time**, **Cycle Time** y **Throughput**.
- **Ejemplo:** `2024-03-22 17:30:00`
- **Restricciones:** Si no es nulo, debe ser ≥ `date_start` ≥ `date_created`

---

### 7. `date_last_moved`
- **Tipo:** DateTime (ISO 8601)
- **Obligatorio:** ⚠️ Recomendado
- **Descripción:** Última vez que la tarea cambió de estado. Permite detectar tareas estancadas.
- **Ejemplo:** `2024-03-20 10:00:00`
- **Restricciones:** ≥ `date_created`

---

### 8. `assignee`
- **Tipo:** String
- **Obligatorio:** ⚠️ Recomendado
- **Descripción:** Nombre o identificador del miembro del equipo asignado.
- **Ejemplo:** `"Ana García"`, `"agarcia"`, `"U-42"`
- **Restricciones:** Usar un identificador estandarizado (evitar mezclar nombres completos con usernames)

---

### 9. `priority`
- **Tipo:** Enum
- **Obligatorio:** Opcional
- **Valores válidos:** `High`, `Medium`, `Low`
- **Ejemplo:** `"High"`
- **Nota:** Útil para segmentar Cycle Time y detectar si las tareas prioritarias se entregan antes.

---

### 10. `task_type`
- **Tipo:** Enum
- **Obligatorio:** Opcional
- **Valores válidos sugeridos:** `Feature`, `Bug`, `Improvement`, `Tech debt`, `Research`, `Documentation`
- **Ejemplo:** `"Bug"`
- **Nota:** Permite comparar tiempos de ciclo entre tipos de trabajo.

---

### 11. `estimated_hours`
- **Tipo:** Float (≥ 0)
- **Obligatorio:** Opcional
- **Descripción:** Estimación inicial de esfuerzo en horas.
- **Ejemplo:** `8.0`
- **Nota:** Combinado con `actual_hours`, permite calcular precisión de estimaciones.

---

### 12. `actual_hours`
- **Tipo:** Float (≥ 0)
- **Obligatorio:** Opcional
- **Descripción:** Horas reales invertidas en completar la tarea.
- **Ejemplo:** `12.5`
- **Restricciones:** Solo válido si status = `Done`

---

### 13. `tags`
- **Tipo:** String (valores separados por `;`)
- **Obligatorio:** Opcional
- **Descripción:** Tags libres para clasificación adicional.
- **Ejemplo:** `"backend;api;auth"`

---

### 14. `sprint`
- **Tipo:** String
- **Obligatorio:** Opcional
- **Descripción:** Nombre o identificador del sprint o iteración a la que pertenece la tarea.
- **Ejemplo:** `"Sprint-12"`, `"2024-Q1-W3"`

---

### 15. `ticket_url`
- **Tipo:** String (URL)
- **Obligatorio:** Opcional
- **Descripción:** Enlace directo al ticket en la herramienta de gestión (Jira, Trello, Linear, etc.).
- **Ejemplo:** `"https://jira.empresa.com/browse/TASK-42"`

---

## Reglas de Integridad de Datos

| Regla | Condición |
|-------|-----------|
| **R1** | `date_created` ≤ `date_start` (si no nulo) |
| **R2** | `date_start` ≤ `date_completed` (si ambos no nulos) |
| **R3** | Si `status = Done`, entonces `date_completed` NO debe ser nulo |
| **R4** | Si `status = Pending`, entonces `date_start` y `date_completed` deben ser nulos |
| **R5** | `actual_hours` solo puede tener valor si `status = Done` |
| **R6** | `task_id` debe ser único en todo el dataset |
| **R7** | `date_last_moved` ≥ `date_created` |

---

## Ejemplo de Registro Completo

```csv
task_id,title,status,date_created,date_start,date_completed,date_last_moved,assignee,priority,task_type,estimated_hours,actual_hours,tags,sprint,ticket_url
TASK-0001,"Implement OAuth2 login",Done,2024-03-01 09:00:00,2024-03-04 10:00:00,2024-03-08 17:00:00,2024-03-08 17:00:00,Ana García,High,Feature,8.0,10.5,"backend;auth",Sprint-10,https://jira.empresa.com/browse/TASK-1
TASK-0002,"Fix bug in payment form",In progress,2024-03-05 11:30:00,2024-03-06 09:00:00,,2024-03-10 15:00:00,Carlos López,High,Bug,3.0,,"frontend",Sprint-10,
TASK-0003,"Document users API",Pending,2024-03-10 16:00:00,,,2024-03-10 16:00:00,,Low,Documentation,4.0,,,Sprint-11,
```

---

## Métricas que Habilita Este Esquema

| Métrica | Columnas Requeridas |
|---------|---------------------|
| **Throughput** | `task_id`, `date_completed`, `status` |
| **Lead Time** | `date_created`, `date_completed` |
| **Cycle Time** | `date_start`, `date_completed` |
| **Wait Time** | `date_created`, `date_start` |
| **WIP actual** | `status`, `date_start` |
| **Tareas estancadas** | `status`, `date_last_moved` |
| **Carga por responsable** | `assignee`, `status` |
| **Precisión de estimaciones** | `estimated_hours`, `actual_hours` |
| **Cycle Time por tipo** | `task_type`, `date_start`, `date_completed` |
