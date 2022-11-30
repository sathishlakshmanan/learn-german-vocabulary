import django_filters
from django_filters import CharFilter

from .models import *


class VocabularyFilter(django_filters.FilterSet):

    word_de = CharFilter(field_name="word_de", lookup_expr="icontains")
    word_en = CharFilter(field_name="word_en", lookup_expr="icontains")
    sentence = CharFilter(field_name="sentence", lookup_expr="icontains")

    class Meta:
        model = CreateVocabulary
        fields = "__all__"
        exclude = ["name", "creation_time"]
