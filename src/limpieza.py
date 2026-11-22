"""Reglas de limpieza de EnrutaIA (decididas en el EDA del Día 3)."""
import pandas as pd


def normalizar(texto: str) -> str:
    """Minúsculas, sin espacios en los extremos y espacios internos reducidos a uno."""
    return " ".join(str(texto).lower().split())


def eliminar_conflictos(df: pd.DataFrame, col_texto="text", col_etiqueta="dominio") -> pd.DataFrame:
    """Regla 2: elimina TODAS las apariciones de un texto que tenga más de una etiqueta."""
    norm = df[col_texto].map(normalizar)
    n_etiquetas = df.groupby(norm)[col_etiqueta].transform("nunique")
    return df[n_etiquetas == 1].reset_index(drop=True)


def deduplicar(df: pd.DataFrame, col_texto="text") -> pd.DataFrame:
    """Regla 3: quita duplicados dentro de un split, conservando la primera aparición."""
    norm = df[col_texto].map(normalizar)
    return df[~norm.duplicated(keep="first")].reset_index(drop=True)


def quitar_presentes_en(df: pd.DataFrame, referencia: pd.DataFrame, col_texto="text") -> pd.DataFrame:
    """Reglas 4 y 5: quita de df los textos que ya aparecen en referencia."""
    vistos = set(referencia[col_texto].map(normalizar))
    return df[~df[col_texto].map(normalizar).isin(vistos)].reset_index(drop=True)


def limpiar_splits(train, val, test, col_texto="text", col_etiqueta="dominio"):
    """Aplica las 5 reglas en orden y devuelve (train, val, test) limpios."""
    # Regla 2: conflictos, mirando el dataset COMPLETO
    todo = pd.concat([train.assign(_split="train"),
                      val.assign(_split="validation"),
                      test.assign(_split="test")], ignore_index=True)
    todo = eliminar_conflictos(todo, col_texto, col_etiqueta)
    train, val, test = (todo[todo["_split"] == s].drop(columns="_split")
                        for s in ["train", "validation", "test"])
    # Regla 3: duplicados dentro de cada split
    train, val, test = (deduplicar(d, col_texto) for d in (train, val, test))
    # Regla 4: validación y test sin textos de train
    val = quitar_presentes_en(val, train, col_texto)
    test = quitar_presentes_en(test, train, col_texto)
    # Regla 5: test sin textos de validación
    test = quitar_presentes_en(test, val, col_texto)
    return train.reset_index(drop=True), val, test
