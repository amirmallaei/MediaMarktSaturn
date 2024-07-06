from rest_framework import serializers
from security.models import SecurityRecord

class SecurityRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityRecord
        fields = '__all__'