from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

def gost_requirements(request):
    data = {
        "standard": "ГОСТ 7.32-2017",
        "font": {
            "name": "Times New Roman",
            "size_pt": 14,
            "weight": "normal"
        },
        "line_spacing": 1.5,
        "first_line_indent_cm": 1.25,
        "margins_cm": {
            "left": 3,
            "right": 1.5,
            "top": 2,
            "bottom": 2
        },
        "alignment": "justify"
    }

    return JsonResponse(data)
    