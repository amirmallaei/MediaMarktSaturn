from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from security.models import SecurityRecord
from security.serializers import SecurityRecordSerializer

class SecurityRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SecurityRecord.objects.all()
    serializer_class = SecurityRecordSerializer