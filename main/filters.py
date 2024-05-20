from .models import *
import django_filters as filters
from django.db.models import Q


class CarrierFilter(filters.FilterSet):
    company = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')
    contact = filters.CharFilter(lookup_expr='icontains')
    mobilephone = filters.CharFilter(lookup_expr='icontains')
    fax = filters.CharFilter(lookup_expr='icontains')
    mcnumber = filters.NumberFilter()
    usdotnumber = filters.NumberFilter()
    feinnumber = filters.NumberFilter()
    hazmat = filters.BooleanFilter()
    hazmatnumber = filters.NumberFilter()
    smartway = filters.BooleanFilter()
    techprovider = filters.CharFilter(lookup_expr='icontains')
    ltl = filters.BooleanFilter()
    ftl = filters.BooleanFilter()
    lastmile = filters.BooleanFilter()
    middlemile = filters.BooleanFilter()
    transloading = filters.BooleanFilter()
    airfreight = filters.BooleanFilter()
    flatbeds = filters.BooleanFilter()
    otr = filters.BooleanFilter()
    refrigerated = filters.BooleanFilter()
    hotshots = filters.BooleanFilter()
    localpickupanddelivery = filters.BooleanFilter()
    expedited = filters.BooleanFilter()
    highvalue = filters.BooleanFilter()
    drayage = filters.BooleanFilter()
    whiteglove = filters.BooleanFilter()
    residential = filters.BooleanFilter()
    insidedelivery = filters.BooleanFilter()
    hemp = filters.BooleanFilter()
    automobileqty = filters.NumberFilter(field_name='automobileqty', lookup_expr='gte')
    highcubedqty = filters.NumberFilter(field_name='highcubedqty', lookup_expr='gte')
    sprinterqty = filters.NumberFilter(field_name='sprinterqty', lookup_expr='gte')
    straughttruckqty = filters.NumberFilter(field_name='straughttruckqty', lookup_expr='gte')
    dryvanqty = filters.NumberFilter(field_name='dryvanqty', lookup_expr='gte')
    reeferqty = filters.NumberFilter(field_name='reeferqty', lookup_expr='gte')
    flatbedqty = filters.NumberFilter(field_name='flatbedqty', lookup_expr='gte')
    warehousesqft = filters.NumberFilter(field_name='warehousesqft', lookup_expr='gte')
    usservice = filters.CharFilter(method='filter_stateus')
    canservice = filters.CharFilter(method='filter_statecan')
    mexservice = filters.CharFilter(method='filter_statemex')
    contractsigned = filters.BooleanFilter()
    tsa = filters.BooleanFilter()
    b2b = filters.BooleanFilter()
    medical = filters.BooleanFilter()
    airport = filters.BooleanFilter()
    courier = filters.BooleanFilter()
    group = filters.ModelMultipleChoiceFilter(queryset=CarrierGroup.objects.all())


    def filter_stateus(self, queryset, name, value):
        states = value.split()  # split input by space to get a list of states
        q_objects = Q()  # create an empty Q object
        for state in states:
            q_objects &= Q(usservice__contains=f"'{state}'")  # add OR condition for each state
        return queryset.filter(q_objects)
    
    def filter_statecan(self, queryset, name, value):
        states = value.split()  # split input by space to get a list of states
        q_objects = Q()  # create an empty Q object
        for state in states:
            q_objects &= Q(canservice__contains=f"'{state}'")  # add OR condition for each state
        return queryset.filter(q_objects)
    
    def filter_statemex(self, queryset, name, value):
        states = value.split()  # split input by space to get a list of states
        q_objects = Q()  # create an empty Q object
        for state in states:
            q_objects &= Q(mexservice__contains=f"'{state}'")  # add OR condition for each state
        return queryset.filter(q_objects)

    class Meta:
        model = Carrier
        fields = ['company', 'email', 'contact', 'mobilephone', 'fax', 'mcnumber', 'usdotnumber', 'feinnumber', 'hazmat', 'hazmatnumber', 'smartway', 'techprovider', 'ltl', 'ftl', 'lastmile', 'middlemile', 'transloading', 'airfreight', 'flatbeds', 'otr', 'refrigerated', 'hotshots', 'localpickupanddelivery', 'expedited', 'highvalue', 'drayage', 'sprinterqty', 'straughttruckqty', 'dryvanqty', 'reeferqty', 'flatbedqty', 'warehousesqft', 'usservice', 'canservice', 'mexservice', 'contractsigned', 'tsa', 'b2b', 'whiteglove', 'residential', 'insidedelivery', 'hemp', 'automobileqty', 'highcubedqty', 'medical', 'airport', 'group']
