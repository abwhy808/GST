import os
import uuid
import traceback

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from validators.check_spacing import format_spacing
from validators.check_alignment import format_alignment
from validators.check_dashes import format_dashes
from validators.check_hyphenation import format_hyphenation

# папка для временных файлов
UPLOAD_DIR = os.path.join(os.getcwd(), "temp")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _cleanup_files(input_path, output_path):
    """Удалить временные файлы."""
    try:
        if os.path.exists(input_path):
            os.remove(input_path)
    except Exception as e:
        print(f"Ошибка при удалении {input_path}: {e}")
    
    try:
        if os.path.exists(output_path):
            os.remove(output_path)
    except Exception as e:
        print(f"Ошибка при удалении {output_path}: {e}")


def _format_document(request, format_func, func_name):
    """
    Универсальная функция для обработки POST-запроса с форматированием.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    if 'file' not in request.FILES:
        return JsonResponse({"error": "No file provided"}, status=400)

    uploaded_file = request.FILES['file']
    
    input_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_input.docx")
    output_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_output.docx")

    try:
        # сохраняем файл
        with open(input_path, 'wb+') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # форматируем
        format_func(input_path, output_path)

        # читаем файл в память
        with open(output_path, 'rb') as f:
            file_data = f.read()

        response = HttpResponse(
            file_data,
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = 'attachment; filename="formatted.docx"'

        return response

    except Exception as e:
        print(f"Ошибка при {func_name}: {traceback.format_exc()}")
        return JsonResponse({
            "error": f"Ошибка при обработке документа: {str(e)}"
        }, status=500)
    
    finally:
        # Удаляем временные файлы в любом случае
        _cleanup_files(input_path, output_path)


@csrf_exempt
def format_spacing_view(request):
    """Форматирование интервалов между абзацами."""
    return _format_document(request, format_spacing, "format_spacing")


@csrf_exempt
def format_alignment_view(request):
    """Форматирование выравнивания текста."""
    return _format_document(request, format_alignment, "format_alignment")


@csrf_exempt
def format_dashes_view(request):
    """Форматирование дефисов и тире."""
    return _format_document(request, format_dashes, "format_dashes")


@csrf_exempt
def format_hyphenation_view(request):
    """Удаление мягких переносов."""
    return _format_document(request, format_hyphenation, "format_hyphenation")