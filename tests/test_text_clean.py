import pytest
import spacy
from src.text_clean import lematizar


@pytest.fixture(scope="module")
def nlp():
    """Carga el modelo de spaCy UNA sola vez para todas las pruebas del archivo."""
    return spacy.load("es_core_news_sm")


def test_lleva_plurales_a_singular(nlp):
    assert "alarma" in lematizar(["pon las alarmas"], nlp)[0].split()


def test_devuelve_minusculas(nlp):
    resultado = lematizar(["Bogotá"], nlp)[0]
    assert resultado == resultado.lower()


def test_conserva_largo_y_orden(nlp):
    textos = ["pon música", "qué hora es", "enciende la luz"]
    salida = lematizar(textos, nlp)
    assert len(salida) == 3
    assert "luz" in salida[2]


def test_elimina_puntuacion(nlp):
    assert "?" not in lematizar(["¿qué hora es?"], nlp)[0]


def test_texto_vacio(nlp):
    assert lematizar([""], nlp) == [""]

def test_lematizar_quitar_stopwords(nlp):
    textos = ["pon la alarma de la mañana"]
    resultado = lematizar(textos, nlp, quitar_stopwords=True)
    palabras = resultado[0].split()

    assert "la" not in palabras
    assert "de" not in palabras
    assert "alarma" in palabras
