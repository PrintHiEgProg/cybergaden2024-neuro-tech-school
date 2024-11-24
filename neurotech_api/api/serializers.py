from rest_framework import serializers
from .models import Calibri

class CalibriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calibri
        fields = ['name', 'RR', 'stress_num', 'stress_level']
