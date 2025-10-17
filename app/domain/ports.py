"""
Интерфейсы
"""

from typing import Protocol, Iterable
from pathlib import Path
from app.domain.models import Plate, RecognizeResult


class INumberPlateRecognizer(Protocol):
    def recognize(self, image_bytes: bytes) -> RecognizeResult:
        """Детектирует номера и читает текст. Возвращает структуру с bbox и строками."""


class IImageRenderer(Protocol):
    def draw(self, image_bytes: bytes, plates: Iterable[
        Plate
    ]) -> bytes:
        """Рисует рамки/подписи на картинке и возвращает новые bytes."""


class IStorage(Protocol):
    def save_processed(self, data: bytes, suffix: str = ".jpg") -> str:
        """Сохраняет файл и возвращает публичный id/имя."""
    def path_for(self, file_id: str) -> Path:
        """Локальный путь по id."""