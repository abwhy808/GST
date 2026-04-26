"""Вспомогательные функции для валидаторов."""
from docx import Document
from pathlib import Path
from typing import Generator, Tuple


def _open_document(path: str | Path) -> Document:
    """
    Открывает DOCX файл и возвращает объект Document.
    Raises ValueError если файл не является валидным DOCX.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")
    
    try:
        return Document(path)
    except Exception as e:
        raise ValueError(f"Ошибка при открытии DOCX: {e}")


def _snippet(text: str, max_length: int = 100) -> str:
    """
    Возвращает сокращённый фрагмент текста для отчёта.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def _is_heading(paragraph) -> bool:
    """
    Проверяет, является ли параграф заголовком.
    """
    style = paragraph.style
    if style is None:
        return False
    return "heading" in style.name.lower()


def _iter_all_paragraphs_with_page(doc: Document) -> Generator[Tuple[int, any, int], None, None]:
    """
    Итератор по всем параграфам документа с номером страницы.
    Yields: (para_idx, paragraph, page_number)
    """
    page_number = 1
    para_idx = 0
    
    for paragraph in doc.paragraphs:
        # Простая логика: новая страница после page break
        if paragraph._element.pPr is not None:
            pPr = paragraph._element.pPr
            # Проверяем наличие page break
            if pPr.find('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pageBreakBefore') is not None:
                page_number += 1
        
        yield para_idx, paragraph, page_number
        para_idx += 1
