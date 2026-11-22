# EnrutaIA

Clasificador de solicitudes en español que asigna cada texto a un área de atención.

## Dataset
- **Fuente:** Amazon MASSIVE, subconjunto en español (`mteb/amazon_massive_intent`, config `es`).
- **Tamaño:** 11.500 train / 2.030 validación / 2.970 test (splits oficiales).
- **Objetivo:** Clasificar en 18 dominios (área de atención); las 60 intenciones quedan como extensión opcional.
- **Por qué:** datos limpios, etiquetados y en español; permite enfocar el tiempo en el modelo.
- **Limitación:** son órdenes a un asistente virtual, no trámites ni PQRS reales.
## Hallazgos del EDA (Día 3)

- Splits estratificados: la proporción de cada dominio es similar en train, validación y test.
- Textos cortos: mediana de 7 palabras; el 99 % tiene 19 palabras o menos.
- Fugas detectadas: 344 duplicados dentro de train; 110 textos de validación y 136 de test también aparecen en train.
- Conflictos de etiqueta: 13 textos aparecen con más de un dominio (ambigüedad o error de anotación).
- Decisión: splits limpios (opción 2). Se eliminan los textos con conflicto, los duplicados dentro de cada split y los textos de validación/test presentes en train (y de test presentes en validación). Se documentará en DATA_CARD.md cuántos ejemplos se quitaron.

## Datos limpios (Día 4)
Generados con `src/limpieza.py` (reglas del EDA, cubiertas por `tests/test_limpieza.py`).

| Split | Original | Limpio | Eliminados | Mín. por dominio | md5 |
|---|---|---|---|---|---|
| train | 11514 | 11158 | 356 (3.1 %) | 211 | cc0ff7796f8e1d1df56862a9f708d521 |
| validation | 2033 | 1915 | 118 (5.8 %) | 26 | ba68845308293612e717aa7c1a55887c |
| test | 2974 | 2806 | 168 (5.6 %) | 49 | 4aa30d7940052535f5646e420cf8cd48 |

Verificación sobre los datos reales: 0 textos compartidos entre train, validación y test; 18 dominios en cada split.
Archivos: `data/limpio/train.csv`, `data/limpio/validation.csv`, `data/limpio/test.csv`.

## Baseline (E0)
TF-IDF (palabras 1-2 + caracteres 2-5) + regresión logística, entrenado en train limpio y evaluado en validación:
**macro-F1 = 0.873 · exactitud = 0.879** (`results/E0_tfidf.json`). Es la referencia que deben superar los demás modelos.
- Dominio más difícil: general (F1 0.605).
- "qa" funciona como cajón de sastre (precisión 0.702, recall 0.923).
