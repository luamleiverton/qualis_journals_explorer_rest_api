from rest_framework import serializers
from qualis.models import Journals

class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journals
        fields = ['issn', 'journal', 'qualis']