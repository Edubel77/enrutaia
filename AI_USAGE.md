# Registro de uso de IA

| Fecha | Herramienta | Qué pedí | Qué acepté / corregí | Cómo lo validé |
|---|---|---|---|---|
| 2026-11-18 | Claude | Código para verificar versiones del entorno | Aceptado sin cambios | Lo ejecuté en Colab y anoté las versiones en requirements.txt |
| 2026-11-18 | Claude | Tabla de ejemplo ReLU vs Softmax | Corregido: Claude dio 0,71, el valor real es 0,72 | Lo verifiqué con tf.nn.softmax en Colab |
| 2026-11-19 | Claude | Código de pérdida con SparseCategoricalCrossentropy | Corregido: pasaba listas de Python con distinta anidación (ValueError); se convirtieron a np.array | Error reproducido y resuelto en Colab; valores a mano y Keras coinciden |
| 2026-11-19 | Claude | Organizar el texto de conclusiones del Lab 1.2 | Aceptado: estructura y tabla; verifiqué que los 9 valores coinciden con mi salida | Comparé la tabla con la salida del Paso 5 |
| 2026-11-20 | Claude | Comparación de regularización con EarlyStopping | Corregido: se reutilizaba el mismo objeto callback entre experimentos y el segundo paraba en la época 3; se creó uno nuevo por experimento | Diagnóstico con parar_a_tiempo.best y reentrenamiento corregido |
