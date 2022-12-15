"""
Example of execution.

cd web_service/backend

python3 -m pytest test/

python3 -m pytest test/ -vs
"""

from src.utils.RemoveAccent import RemoveAccent

INPUT_DATA = {
    'Málaga': 'Malaga',
    'Cánada': 'Canada',
}

def test_remove_accent() -> None:
    for word, normalizedWord in INPUT_DATA.items():
        assert normalizedWord == RemoveAccent.normalize(word)
