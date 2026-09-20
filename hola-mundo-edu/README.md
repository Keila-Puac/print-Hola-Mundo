# 📚 Educación Clara GT

**Herramienta para hacer comprensibles los microdatos de Educación Formal 2024 de Guatemala.**

Proyecto desarrollado para el **Hackaton AI Builders GT 2026**.

---

## 🎯 Problema que resuelve

El dataset oficial del INE contiene **~4.3 millones de registros** de estudiantes del ciclo 2024.  
Los valores vienen codificados (1 = Público, 5 = No promovido, etc.) y el volumen hace imposible abrirlos en Excel o consultarlos directamente.

Este proyecto convierte esos datos opacos en:

1. **Ingesta limpia** → códigos traducidos a palabras + normalización de problemas conocidos.
2. **Dashboard** → gráficas claras + análisis escrito para personas sin formación técnica.
3. **Agente conversacional** → preguntas en lenguaje natural respondidas solo con datos reales.

---

## 🏗️ Arquitectura

```
data/raw/          → archivos .xlsx originales del INE (1 por departamento + diccionario)
       ↓
backend/ingestion.py   → limpia, decodifica y guarda en Parquet
       ↓
backend/analytics.py   → calcula indicadores, brechas e insights
       ↓
data/processed/    → archivos listos para el frontend y el agente
       ↓
frontend/app.py    → Dashboard Streamlit (4 páginas)
backend/agent.py   → Agente (Grok + fallback local)
```

### Componentes

| Componente | Archivo principal | Qué hace |
|------------|-------------------|----------|
| **Ingesta** | `backend/ingestion.py` | Lee Excel, normaliza códigos de establecimiento, traduce códigos numéricos, guarda Parquet |
| **Analytics** | `backend/analytics.py` | KPIs nacionales, resumen por departamento, brechas (área, sector, nivel, pueblo), insights accionables |
| **Dashboard** | `frontend/app.py` | 4 páginas: Panorama Nacional, Por Departamento, Brechas, Chat |
| **Agente** | `backend/agent.py` | Responde en español. Usa Grok si está disponible; si no, motor local basado en los datos agregados |

---

## 🚀 Cómo ejecutarlo

### 1. Clonar e instalar

```bash
git clone https://github.com/Keila-Puac/print-Hola-Mundo-.git
cd print-Hola-Mundo-
pip install -r requirements.txt
```

### 2. Datos

Los archivos raw ya están en `data/raw/` (varios departamentos).  
Si quieres procesar **todos** los departamentos disponibles:

```bash
python scripts/run_pipeline.py --completo
```

Por defecto el pipeline corre en **modo prueba** (3 departamentos pequeños) para desarrollo rápido:

```bash
python scripts/run_pipeline.py
```

### 3. Levantar el dashboard

```bash
streamlit run frontend/app.py
```

Se abrirá en `http://localhost:8501`.

---

## 📊 Páginas del dashboard

1. **🏠 Panorama Nacional**  
   KPIs de promoción / retiro, insights principales, distribución por nivel y departamentos más críticos.

2. **🗺️ Por Departamento**  
   Selector de departamento + métricas + insight automático + comparación visual.

3. **⚖️ Brechas y Desigualdades**  
   Urbano vs Rural, Sector, Pueblo de pertenencia y Nivel educativo, cada uno con explicación escrita.

4. **💬 Pregúntale a los datos**  
   Chat en lenguaje natural. El agente **nunca inventa cifras**.

---

## 🔑 Decisiones técnicas importantes

| Decisión | Motivo |
|----------|--------|
| Parquet en lugar de CSV | ~10× más rápido y liviano para 4+ millones de filas |
| Normalización `00-` → `01-` | ~36 % de los registros de Guatemala tienen este prefijo erróneo. Sin corregirlo se inventan municipios |
| Municipio derivado de `CodEstablecimiento` | La columna `Depto_mupio` es constante dentro de cada archivo y no sirve |
| Insights generados por código (no por LLM) | Garantiza que las cifras cuadren con los datos reales |
| Fallback local en el agente | El dashboard sigue funcionando aunque no haya conexión a Grok |
| Streamlit | Rápido de desarrollar, suficiente para el alcance del hackaton y fácil de explicar |

---

## 📁 Estructura del repositorio

```
├── backend/
│   ├── ingestion.py      # Decodificación y limpieza
│   ├── analytics.py      # Indicadores e insights
│   ├── agent.py          # Agente conversacional
│   └── config.py         # Rutas y mapeos de códigos
├── frontend/
│   ├── app.py            # Punto de entrada Streamlit
│   └── pages/
│       ├── home.py
│       ├── departamentos.py
│       ├── brechas.py
│       └── chat.py
├── data/
│   ├── raw/              # Archivos originales del INE
│   └── processed/        # Parquet + JSON listos para consumo
├── scripts/
│   └── run_pipeline.py
├── docs/
│   └── hackaton.md
├── tests/
├── requirements.txt
└── README.md
```

---

## ⚠️ Limitaciones conocidas

- El dataset solo cubre el ciclo **2024** (no hay serie histórica).
- No hay identificador de estudiante → no se puede seguir trayectorias individuales.
- No incluye edad, calificaciones, discapacidad ni datos socioeconómicos.
- Algunos departamentos pueden faltar en `data/raw/` (depende de la descarga).
- El agente local es basado en reglas; con Grok disponible las respuestas son más naturales.

---

## 📝 Uso de IA en el proyecto

- Desarrollo asistido con IA (Grok / Claude) para generar partes del dashboard y el agente.
- El agente de producción puede usar Grok (vía `grook`) o el motor local.
- **Todas las cifras** que se muestran o se responden provienen de los cálculos de `analytics.py`, nunca de generación libre del modelo.

---

## 👥 Equipo / Hackaton

Proyecto para el **AI Builders Hackathon – Xela 2026**.  
Dataset oficial: [Educación Formal 2024 – INE](https://datos.ine.gob.gt/dataset/educacion-formal-2024).

---

**¿Preguntas o mejoras?** Abre un issue o contacta al equipo.
