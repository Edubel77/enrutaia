"""Preprocesamiento lingüístico de EnrutaIA con spaCy (Día 6)."""


def lematizar(textos, nlp, quitar_stopwords=False):
    """Devuelve cada texto como sus lemas en minúscula, separados por espacios.

    - Elimina la puntuación.
    - Si quitar_stopwords=True, elimina también las palabras vacías ("de", "la"...).
    - Devuelve una lista del mismo largo y en el mismo orden que `textos`.
    """
    salida = []
    for doc in nlp.pipe(list(textos), batch_size=256, disable=["parser", "ner"]):
        lemas = [t.lemma_.lower() for t in doc
                 if not t.is_punct and not t.is_space
                 and not (quitar_stopwords and t.is_stop)]
        salida.append(" ".join(lemas))
    return salida
