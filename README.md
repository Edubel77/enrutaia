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

## Problema
Las solicitudes de usuarios llegan en texto libre y alguien debe asignarlas al área correcta, lo que retrasa la atención y produce errores de enrutamiento.
**Pregunta del proyecto:** ¿un modelo adaptado con pocos recursos de cómputo clasifica estas solicitudes en 18 dominios mejor que un baseline clásico, y a qué costo?
**Métrica principal:** macro-F1 en validación (todas las áreas pesan igual). El test se evalúa una sola vez, al final de la Semana 3.
## Experimentos (Semana 1)
| ID | Modelo | macro-F1 validación | Semillas | Archivo |
|---|---|---|---|---|
| E0 | TF-IDF (palabras + caracteres) + regresión logística | 0.8725 | determinista | `results/E0_tfidf.json` |
| E1 | Keras: Embedding(64) + promedio + softmax | 0.8732 ± 0.0019 | 42, 123, 2024 | `results/E1_keras.json` |

**Conclusión:** empate técnico (E0 cae dentro de la variación de E1). Ante el empate, la referencia es E0 por ser más simple, determinista y liviano. Los modelos preentrenados (Semanas 2-3) deberán superarlo con claridad.
## Preprocesamiento lingüístico (Día 6)
- Modelo: spaCy `es_core_news_sm` (instalar con `python -m spacy download es_core_news_sm`).
- Los textos de MASSIVE vienen en minúsculas: el NER del modelo pequeño no es confiable (detecta verbos como entidades, p. ej. "pon" como ORG). **Decisión: no se usan entidades como características.**
- 53 % de los tokens son stopwords.

| Variante de E0 | macro-F1 validación | Diferencia |
|---|---|---|
| Texto original | 0.8725 | — |
| Lemas | 0.8764 | +0.0039 |
| Lemas sin stopwords | 0.8451 | −0.0274 |

Quitar stopwords empeora: palabras como "qué", "mi" o "me" son pistas del dominio.
**Decisión:** se mantiene E0 original como referencia. La mejora de E0-lemas (+0.0039) es pequeña y no compensa agregar spaCy como dependencia ni hacer más lento el procesamiento, cuando el modelo base ya funciona bien. Además, los Transformers de la Semana 3 trabajan con texto crudo..

## Representaciones de texto (Día 7)
| Representación | macro-F1 validación |
|---|---|
| BoW (palabras) | 0.8559 |
| TF-IDF (palabras) | 0.8570 |
| TF-IDF (palabras 1-2) | 0.8499 |
| **E0:** TF-IDF palabras 1-2 + caracteres 2-5 | **0.8725** |
| E0-lemas (spaCy) | 0.8764 |
| E1: Embedding aprendido | 0.8732 ± 0.0019 |

- Los fragmentos de caracteres aportan la mayor mejora (+0.0226 sobre TF-IDF palabras 1-2).
- Los embeddings de E1 agrupan palabras **del mismo dominio**, no sinónimos (p. ej. "luz" cerca de "café" y "aspirar", todos de iot).
- Tokenizador de BETO (WordPiece): 0.03 % de tokens [UNK] en validación, frente a 4.7 % de palabras desconocidas en E1.
- **Decisión:** `max_length = 32` para la Semana 3 (percentil 99 = 20 tokens + [CLS] y [SEP], con margen).

   ## Diagnóstico de E0 (Día 8)
- La confusión más frecuente es **general → qa: 30 de 115** textos de general (26 %). La segunda es music → play (9).
- qa funciona como "cajón de sastre": recibe textos de general (30), news (8) y play (7).
- `class_weight="balanced"` **no mejora**: macro-F1 0.8699 frente a 0.8725, y general baja de 0.6047 a 0.5950 (`results/E0_class_weight.json`).
- **Conclusión:** el problema de general no es el desbalance (115 ejemplos en validación), sino la ambigüedad con qa. **Decisión:** E0 se mantiene sin `class_weight`.
- 
## Cómo reproducir
1. Abrir en Colab `notebooks/D5_lab_1_5_keras_texto.ipynb` y ejecutar todo.
2. Los datos se descargan de `data/limpio/` y se verifica su md5 antes de usarlos.
3. E0 debe dar macro-F1 = 0.8725 en validación; E1 ≈ 0.8732 ± 0.0019 (3 semillas).
4. Instalar el modelo de español con `python -m spacy download es_core_news_sm` y ejecutar las pruebas con `python -m pytest tests/ -v` (15 pruebas: 9 de limpieza y 6 de preprocesamiento).
