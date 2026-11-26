# Registro de uso de IA

| Fecha | Herramienta | Qué pedí | Qué acepté / corregí | Cómo lo validé |
|---|---|---|---|---|
| 2026-11-18 | Claude | Código para verificar versiones del entorno | Aceptado sin cambios | Lo ejecuté en Colab y anoté las versiones en requirements.txt |
| 2026-11-18 | Claude | Tabla de ejemplo ReLU vs Softmax | Corregido: Claude dio 0,71, el valor real es 0,72 | Lo verifiqué con tf.nn.softmax en Colab |
| 2026-11-19 | Claude | Código de pérdida con SparseCategoricalCrossentropy | Corregido: pasaba listas de Python con distinta anidación (ValueError); se convirtieron a np.array | Error reproducido y resuelto en Colab; valores a mano y Keras coinciden |
| 2026-11-19 | Claude | Organizar el texto de conclusiones del Lab 1.2 | Aceptado: estructura y tabla; verifiqué que los 9 valores coinciden con mi salida | Comparé la tabla con la salida del Paso 5 |
| 2026-11-20 | Claude | Comparación de regularización con EarlyStopping | Corregido: se reutilizaba el mismo objeto callback entre experimentos y el segundo paraba en la época 3; se creó uno nuevo por experimento | Diagnóstico con parar_a_tiempo.best y reentrenamiento corregido |
| 2026-11-20 | Claude | Revisar y reorganizar conclusiones del Lab 1.3 | Corregido: mi borrador atribuía el error al orden y a la paciencia del callback; la causa real fue reutilizar el objeto. Acepté la versión con criterio explícito y limitaciones | Verifiqué la tabla contra mis salidas y que la lección coincide con el diagnóstico de parar_a_tiempo.best |
| 2026-11-21 | Claude | Módulo src/limpieza.py con las 5 reglas | Aceptado tras revisarlo; corregí la premisa de Claude sobre el orden de las reglas 4 y 5 (no cambia el resultado) | 9 pruebas pytest en verde + 0 fugas verificadas sobre los datos reales |
| 2026-11-21 | Claude | 8 pruebas pytest para la limpieza | Aceptadas; escribí yo la prueba de la regla 5 | pytest: 9 passed |
| 2026-11-22 | Claude | Código de E1 (TextVectorization + Embedding) y evaluación con 3 semillas | Aceptado tras revisarlo | md5 de los datos verificado, semilla 42 repetida con resultado idéntico (0.871508), E0 reproducido desde el repo |
| 2026-11-23 | Claude | Módulo src/text_clean.py y 5 pruebas | Aceptado; escribí la 6.ª prueba (quitar_stopwords) y corregí mi propio error al no pedir la fixture nlp | pytest: 6 passed |
| 2026-11-23 | Claude | Experimento E0 con variantes de spaCy | Aceptado; corregí mi atribución de las minúsculas (vienen de MASSIVE, no de la limpieza) | Control E0 original = 0.8725, igual que el Día 4 |
| 2026-11-25 | Claude | Código de comparación BoW/TF-IDF, vecinos de embeddings y tokenizador de BETO | Aceptado; corregí el ejemplo de Claude ("despertadores" no se parte en desperta + ##dores, sino en despertado + ##res) | Salida real de tok.tokenize en Colab |
