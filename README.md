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
