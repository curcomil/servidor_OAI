import re
import unicodedata
from difflib import SequenceMatcher

FIXED_ORDER = {
    "portada": 1,
    "preliminar": 2,
    "agradecimientos": 3,
    "indice": 4,
    "resumen": 5,
    "prefacio": 6,
    "acronimos": 7,
    "glosario": 8,
    "introduccion": 9,
    "referencias": 12,
    "bibliografia": 13,
    "vita": 15,
    "contenido_multimedia": 16,
}

CAPITULO_ZERO_ORDER = 10
CAPITULO_ORDER = 11
APENDICE_ORDER = 14
UNMATCHED_ORDER = 999

SIMILARITY_THRESHOLD = 0.75

# Toleran separadores opcionales entre el prefijo y el número/letra:
# "capitulo1", "capitulo_1", "capitulo 01" deben resolver igual.
_CAPITULO_RE = re.compile(r"capitulo[\s_-]*(\d+)")
_APENDICE_RE = re.compile(r"apendice[\s_-]*([a-z]+)(?:[\s_-]*(\d+))?")
_FUZZY_TOKENS = list(FIXED_ORDER.keys()) + ["capitulo", "apendice"]


def _normalize(text: str) -> str:
    text = text.lower()
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def _strip_extension(file_name: str) -> str:
    return file_name.rsplit(".", 1)[0] if "." in file_name else file_name


def _letter_rank(letters: str) -> int:
    rank = 0
    for ch in letters:
        rank = rank * 26 + (ord(ch) - ord("a") + 1)
    return rank


def _capitulo_key(n: int) -> tuple[int, int, int]:
    return (CAPITULO_ZERO_ORDER, 0, 0) if n == 0 else (CAPITULO_ORDER, n, 0)


def _apendice_key(letters: str, num: str | None) -> tuple[int, int, int]:
    return (APENDICE_ORDER, _letter_rank(letters), int(num) if num else 0)


def _contains_sequence(words: list[str], seq: list[str]) -> bool:
    n, m = len(words), len(seq)
    return any(words[i : i + m] == seq for i in range(n - m + 1))


def _fuzzy_match(stem: str, words: list[str]) -> tuple[int, int, int] | None:
    best_token, best_score = None, 0.0
    for word in words:
        for token in _FUZZY_TOKENS:
            score = SequenceMatcher(None, word, token).ratio()
            if score > best_score:
                best_score, best_token = score, token

    if not best_token or best_score < SIMILARITY_THRESHOLD:
        return None

    if best_token in FIXED_ORDER:
        return (FIXED_ORDER[best_token], 0, 0)

    if best_token == "capitulo":
        m = re.search(r"\d+", stem)
        return _capitulo_key(int(m.group()) if m else 0)

    # best_token == "apendice"
    m = re.search(r"([a-z]+)[\s_-]*(\d+)?$", stem)
    if m:
        return _apendice_key(*m.groups())
    return (APENDICE_ORDER, 0, 0)


def compute_tesis_order(file_name: str) -> tuple[int, int, int]:
    """Posición semántica de un archivo de tesis según tesis_order_map.

    Match exacto/patrón primero (capitulo N, apendice X[-N], términos fijos);
    si nada calza, similitud difusa (typos); si tampoco, va al final.
    """
    stem = _normalize(_strip_extension(file_name))

    m = _CAPITULO_RE.search(stem)
    if m:
        return _capitulo_key(int(m.group(1)))

    m = _APENDICE_RE.search(stem)
    if m:
        return _apendice_key(*m.groups())

    words = [w for w in re.split(r"[^a-z0-9]+", stem) if w]

    for token, order in FIXED_ORDER.items():
        if _contains_sequence(words, token.split("_")):
            return (order, 0, 0)

    fuzzy = _fuzzy_match(stem, words)
    if fuzzy:
        return fuzzy

    return (UNMATCHED_ORDER, 0, 0)
