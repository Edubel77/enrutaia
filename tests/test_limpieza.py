import pandas as pd
from src.limpieza import (normalizar, eliminar_conflictos, deduplicar,
                          quitar_presentes_en, limpiar_splits)


def df(textos, dominios=None):
    """Ayudante: crea un DataFrame pequeño para las pruebas."""
    return pd.DataFrame({"text": textos, "dominio": dominios or ["x"] * len(textos)})


def test_normalizar_minusculas_y_espacios():
    assert normalizar("  Pon   MÚSICA  ") == "pon música"


def test_normalizar_acepta_valores_no_texto():
    assert normalizar(123) == "123"


def test_deduplicar_conserva_la_primera_aparicion():
    entrada = df(["Hola", "hola ", "adiós", "HOLA"], ["a", "b", "c", "d"])
    salida = deduplicar(entrada)
    assert list(salida["text"]) == ["Hola", "adiós"]
    assert list(salida["dominio"]) == ["a", "c"]


def test_eliminar_conflictos_quita_todas_las_apariciones():
    entrada = df(["borrar", "Borrar", "pon música"], ["calendar", "lists", "audio"])
    salida = eliminar_conflictos(entrada)
    assert list(salida["text"]) == ["pon música"]


def test_eliminar_conflictos_conserva_duplicados_con_la_misma_etiqueta():
    entrada = df(["hola", "Hola"], ["general", "general"])
    assert len(eliminar_conflictos(entrada)) == 2


def test_quitar_presentes_en():
    val = df(["pon música", "qué hora es"])
    train = df(["Pon Música"])
    assert list(quitar_presentes_en(val, train)["text"]) == ["qué hora es"]


def test_limpiar_splits_no_deja_fugas():
    train = df(["a", "b", "b", "c"])
    val = df(["c", "d"])
    test = df(["a", "d", "e"])
    tr, va, te = limpiar_splits(train, val, test)
    n = lambda d: set(d["text"].map(normalizar))
    assert n(tr) & n(va) == set()
    assert n(tr) & n(te) == set()
    assert n(va) & n(te) == set()
    assert list(te["text"]) == ["e"]


def test_limpiar_splits_no_modifica_los_datos_originales():
    train = df(["a", "a"])
    limpiar_splits(train, df(["b"]), df(["c"]))
    assert len(train) == 2



def test_regla5_quita_de_test_lo_que_esta_en_validacion():
    train = df(["enciende la luz"])
    val   = df(["qué hora es"])
    test  = df(["qué hora es", "pon música"])
    tr, va, te = limpiar_splits(train, val, test)
    assert "qué hora es" not in list(te["text"])
    assert "pon música" in list(te["text"])
    assert "qué hora es" in list(va["text"])
