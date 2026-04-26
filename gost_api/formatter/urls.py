from django.urls import path
from .views import (
    format_spacing_view,
    format_alignment_view,
    format_dashes_view,
    format_hyphenation_view,
)

urlpatterns = [
    path('spacing/', format_spacing_view, name='format_spacing'),
    path('alignment/', format_alignment_view, name='format_alignment'),
    path('dashes/', format_dashes_view, name='format_dashes'),
    path('hyphenation/', format_hyphenation_view, name='format_hyphenation'),
]