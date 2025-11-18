from rest_framework import serializers
from .models import JournalEntry

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ["id","user","shop","item","visit_date","my_rating","notes","created_at"]
        read_only_fields = ["user","created_at"]
