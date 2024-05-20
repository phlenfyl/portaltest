from rest_framework import serializers
from .models import *

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class TemplatedFiltersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplatedFilters
        fields = [
            "start_date",
            "end_date",
            "customercity",
            "customerstate",
            "deliverystatus"
        ] 
        # make fields not required
        extra_kwargs = {
            "start_date": {"required": False},
            "end_date": {"required": False},
            "customercity": {"required": False},
            "customerstate": {"required": False},
            "deliverystatus": {"required": False}
        }