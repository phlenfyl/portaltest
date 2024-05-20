from rest_framework import serializers
from ..models import Order, GeneratedReport

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class GeneratedReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedReport
        fields = '__all__'
