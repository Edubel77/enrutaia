# EnrutaIA

Clasificador de solicitudes en español que asigna cada texto a un área de atención.

## Dataset
- **Fuente:** Amazon MASSIVE, subconjunto en español (`mteb/amazon_massive_intent`, config `es`).
- **Tamaño:** 11.500 train / 2.030 validación / 2.970 test (splits oficiales).
- **Objetivo:** Clasificar en 18 dominios (área de atención); las 60 intenciones quedan como extensión opcional.
- **Por qué:** datos limpios, etiquetados y en español; permite enfocar el tiempo en el modelo.
- **Limitación:** son órdenes a un asistente virtual, no trámites ni PQRS reales.
