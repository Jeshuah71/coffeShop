from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import JournalEntry
from .serializers import JournalEntrySerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_entries(request):
    qs = JournalEntry.objects.filter(user=request.user).order_by("-visit_date","-created_at")
    return Response(JournalEntrySerializer(qs, many=True).data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_entry(request):
    ser = JournalEntrySerializer(data=request.data)
    if ser.is_valid():
        ser.save(user=request.user)
        return Response(ser.data, status=201)
    return Response(ser.errors, status=400)
