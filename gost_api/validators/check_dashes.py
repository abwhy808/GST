from pathlib import Path
from typing import Any
import re

from docx import Document
from .helpers import _open_document, _iter_all_paragraphs_with_page, _snippet


def check_dashes(path: str | Path) -> dict[str, Any]:
    """
    Объединённая проверка и корректировка дефисов/тире.
    Если используется ' - ' вместо ' — ' → фиксируем и отмечаем.
    Возвращает формат, совместимый с остальными проверками: dict с полем "violations".
    """

    def _fix_text(text: str) -> str:
        # диапазоны чисел: 1-2 -> 1–2 (en dash)
        text = re.sub(r'(?<=\d)-(?=\d)', '–', text)
        # тире между словами: ' - ' -> ' — '
        text = re.sub(r'\s-\s', ' — ', text)
        return text

    try:
        doc = _open_document(path)
    except (ValueError, FileNotFoundError) as e:
        return {"ok": False, "error": str(e)}

    violations = []

    for para_idx, paragraph, page in _iter_all_paragraphs_with_page(doc):

        text = paragraph.text

        if re.search(r"\s-\s", text) or re.search(r'(?<=\d)-(?=\d)', text):
            fixed = _fix_text(text)
            violations.append({
                "page": page,
                "value": _snippet(text),
                "required": "— (and – for ranges)",
                "suggested": _snippet(fixed)
            })

    if not violations:
        return {"ok": True, "message": "Дефисы и тире используются корректно."}

    return {
        "ok": False,
        "message": "Найдены дефисы/тире, предложены исправления.",
        "violations": violations
    }


def format_dashes(input_path, output_path):
    """Исправить дефисы и тире согласно ГОСТ."""
    doc = Document(input_path)

    for paragraph in doc.paragraphs:
        text = paragraph.text
        
        # Диапазоны чисел: 1-2 -> 1–2 (en dash)
        text = re.sub(r'(?<=\d)-(?=\d)', '–', text)
        # Тире между словами: ' - ' -> ' — '
        text = re.sub(r'\s-\s', ' — ', text)
        
        # Обновляем текст параграфа через runs
        if text != paragraph.text:
            for run in paragraph.runs:
                run.text = ''
            paragraph.text = text

    doc.save(output_path)
