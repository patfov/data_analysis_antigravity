# 📊 Medición de Productividad con Tablero Kanban

> **Contexto:** Equipo con tres columnas: `Pendiente → En progreso → Hecho`
> **Fase:** Definición de objetivos y diseño de métricas (sin datos aún)

---

## Fase 1: Entender el Problema

**Pregunta de negocio central:**
> ¿Está nuestro equipo entregando trabajo a un ritmo predecible y sostenible, y dónde están los cuellos de botella?

**Audiencia principal:** Manager de equipo / Product Owner  
**Decisiones que se tomarán con estos datos:**
- Ajustar la capacidad del equipo
- Identificar bloqueos y cuellos de botella
- Mejorar la planificación de sprints o iteraciones
- Detectar miembros del equipo sobrecargados o sub-utilizados

---

## Tabla Principal: Pregunta → Métrica → Datos Necesarios

| # | Pregunta de Negocio | Métrica (KPI) | Definición de la Métrica | Datos Mínimos Necesarios |
|---|---------------------|---------------|--------------------------|--------------------------|
| 1 | ¿Cuántas tareas completa el equipo por semana? | **Throughput** | Nº de tareas movidas a "Hecho" por unidad de tiempo | `task_id`, `fecha_completado`, `estado` |
| 2 | ¿Cuánto tiempo pasa desde que se crea una tarea hasta que se entrega? | **Lead Time** | `fecha_completado` − `fecha_creación` (en días) | `task_id`, `fecha_creación`, `fecha_completado` |
| 3 | ¿Cuánto tiempo tarda una tarea desde que se empieza a trabajar hasta que se termina? | **Cycle Time** | `fecha_completado` − `fecha_inicio` (en días) | `task_id`, `fecha_inicio`, `fecha_completado` |
| 4 | ¿Cuántas tareas hay activas al mismo tiempo? | **WIP (Work In Progress)** | Nº de tareas en estado "En progreso" en un momento dado | `task_id`, `estado`, `fecha_inicio` |
| 5 | ¿Hay tareas bloqueadas o abandonadas en progreso? | **Tasa de tareas estancadas** | % de tareas en "En progreso" con más de N días sin avance | `task_id`, `estado`, `fecha_inicio`, `fecha_último_movimiento` |
| 6 | ¿Estamos entregando más o menos que antes? | **Tendencia de Throughput** | Variación semanal/mensual del throughput (% de cambio) | `task_id`, `fecha_completado`, `estado` |
| 7 | ¿Qué tipo de tareas tarda más en completarse? | **Cycle Time por categoría** | Cycle Time promedio segmentado por tipo o prioridad | `task_id`, `fecha_inicio`, `fecha_completado`, `tipo_tarea` o `prioridad` |
| 8 | ¿Qué personas del equipo tienen más carga de trabajo? | **Distribución de carga por responsable** | Nº de tareas en progreso o completadas por persona | `task_id`, `responsable`, `estado` |
| 9 | ¿Cuál es la predictibilidad del equipo? | **Variabilidad del Cycle Time** | Desviación estándar y percentiles P50/P85/P95 del cycle time | `task_id`, `fecha_inicio`, `fecha_completado` |
| 10 | ¿Estamos acumulando deuda de trabajo sin terminar? | **Tasa de tareas completadas vs. creadas** | Ratio: `tareas_completadas / tareas_creadas` por semana | `task_id`, `fecha_creación`, `fecha_completado`, `estado` |
| 11 | ¿Cuánto tiempo permanece una tarea sin que nadie la tome? | **Tiempo de espera (Wait Time)** | `fecha_inicio` − `fecha_creación` (en días) | `task_id`, `fecha_creación`, `fecha_inicio` |
| 12 | ¿Hay momentos del mes/semana con picos de entrega o bloqueo? | **Patrones temporales de entrega** | Distribución de completados por día de semana / semana del mes | `task_id`, `fecha_completado` |

---

## Esquema Mínimo de Datos a Capturar

Para calcular **todas** las métricas anteriores, cada tarea debe registrar al menos:

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|:-----------:|-------------|
| `task_id` | String / Int | ✅ | Identificador único de la tarea |
| `titulo` | String | ✅ | Descripción corta de la tarea |
| `estado` | Enum (`Pendiente`, `En progreso`, `Hecho`) | ✅ | Estado actual en el tablero |
| `fecha_creacion` | DateTime | ✅ | Cuándo se añadió la tarea al backlog |
| `fecha_inicio` | DateTime | ⚠️ Recomendado | Cuándo se movió a "En progreso" |
| `fecha_completado` | DateTime | ⚠️ Recomendado | Cuándo se movió a "Hecho" |
| `responsable` | String | ⚠️ Recomendado | Persona asignada a la tarea |
| `prioridad` | Enum (`Alta`, `Media`, `Baja`) | Opcional | Prioridad de la tarea |
| `tipo_tarea` | Enum (`Bug`, `Feature`, `Mejora`, etc.) | Opcional | Categoría para segmentación |
| `fecha_ultimo_movimiento` | DateTime | Opcional | Para detectar tareas estancadas |

> ⚠️ **Alerta de diseño:** Si `fecha_inicio` o `fecha_completado` no se registran automáticamente (ej. via webhook del tablero), el 80% de las métricas serán imposibles de calcular o estarán sesgadas por el olvido humano. **Se recomienda automatizar la captura de estos timestamps.**

---

## Relaciones entre Métricas (Ley de Little)

Existe una relación matemática fundamental entre las tres métricas clave:

```
Lead Time = WIP / Throughput
```

Esto significa que si el **WIP sube** sin que el **Throughput** aumente, el **Lead Time crecerá proporcionalmente**. Controlar el WIP es la palanca más directa para mejorar la velocidad de entrega.

---

## Próximos Pasos

1. **Diseñar el esquema de datos** con todas las columnas y tipos (Prompt 2)
2. **Generar un dataset de ejemplo** para practicar los análisis (Prompt 3)
3. **Validar la calidad de datos** antes de calcular métricas (Prompt 4)
4. **EDA + cálculo de métricas base** con los datos limpios (Prompt 5)
5. **Análisis de tendencias** y detección de cambios en el throughput (Prompt 6)
