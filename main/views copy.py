import googlemaps
from io import BytesIO
import base64
from django.shortcuts import redirect, render
from django.template import base
from django.db.models import Case, When, Value, IntegerField
from .models import *
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from urllib.parse import urlencode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.viewsets import ModelViewSet
from django.core.mail import send_mail
from django.db.models import Q
from .forms import *
from django.core.paginator import Paginator
from .serializers import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormMixin
from datetime import datetime
from django.contrib import messages
from django.views.generic.edit import UpdateView
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.graphics.barcode import code128
from reportlab.graphics import *
from reportlab.lib.units import mm
from .filters import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from datetime import datetime
from datetime import timedelta
# import openai
import ast
from address.models import Address
from datetime import datetime, date, timedelta
from django.views import View
from django.conf import settings
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
import pandas as pd
import csv
from io import StringIO
from django.shortcuts import render
from .models import WebHook, Order
from django.db.models import Avg, F
from io import BytesIO
import base64

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mpld3
from django.shortcuts import render
from .models import WebHook
import numpy as np



STATES = [
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming')
]

STATE_MAP = {
    'AL': ['AL', 'Alabama', 'ALABAMA'],
    'AK': ['AK', 'Alaska', 'ALASKA'],
    'AZ': ['AZ', 'Arizona', 'ARIZONA'],
    'AR': ['AR', 'Arkansas', 'ARKANSAS'],
    'CA': ['CA', 'California', 'CALIFORNIA'],
    'CO': ['CO', 'Colorado', 'COLORADO'],
    'CT': ['CT', 'Connecticut', 'CONNECTICUT'],
    'DE': ['DE', 'Delaware', 'DELAWARE'],
    'FL': ['FL', 'Florida', 'FLORIDA'],
    'GA': ['GA', 'Georgia', 'GEORGIA'],
    'HI': ['HI', 'Hawaii', 'HAWAII'],
    'ID': ['ID', 'Idaho', 'IDAHO'],
    'IL': ['IL', 'Illinois', 'ILLINOIS'],
    'IN': ['IN', 'Indiana', 'INDIANA'],
    'IA': ['IA', 'Iowa', 'IOWA'],
    'KS': ['KS', 'Kansas', 'KANSAS'],
    'KY': ['KY', 'Kentucky', 'KENTUCKY'],
    'LA': ['LA', 'Louisiana', 'LOUISIANA'],
    'ME': ['ME', 'Maine', 'MAINE'],
    'MD': ['MD', 'Maryland', 'MARYLAND'],
    'MA': ['MA', 'Massachusetts', 'MASSACHUSETTS'],
    'MI': ['MI', 'Michigan', 'MICHIGAN'],
    'MN': ['MN', 'Minnesota', 'MINNESOTA'],
    'MS': ['MS', 'Mississippi', 'MISSISSIPPI'],
    'MO': ['MO', 'Missouri', 'MISSOURI'],
    'MT': ['MT', 'Montana', 'MONTANA'],
    'NE': ['NE', 'Nebraska', 'NEBRASKA'],
    'NV': ['NV', 'Nevada', 'NEVADA'],
    'NH': ['NH', 'New Hampshire', 'NEW HAMPSHIRE'],
    'NJ': ['NJ', 'New Jersey', 'NEW JERSEY'],
    'NM': ['NM', 'New Mexico', 'NEW MEXICO'],
    'NY': ['NY', 'New York', 'NEW YORK'],
    'NC': ['NC', 'North Carolina', 'NORTH CAROLINA'],
    'ND': ['ND', 'North Dakota', 'NORTH DAKOTA'],
    'OH': ['OH', 'Ohio', 'OHIO'],
    'OK': ['OK', 'Oklahoma', 'OKLAHOMA'],
    'OR': ['OR', 'Oregon', 'OREGON'],
    'PA': ['PA', 'Pennsylvania', 'PENNSYLVANIA'],
    'RI': ['RI', 'Rhode Island', 'RHODE ISLAND'],
    'SC': ['SC', 'South Carolina', 'SOUTH CAROLINA'],
    'SD': ['SD', 'South Dakota', 'SOUTH DAKOTA'],
    'TN': ['TN', 'Tennessee', 'TENNESSEE'],
    'TX': ['TX', 'Texas', 'TEXAS'],
    'UT': ['UT', 'Utah', 'UTAH'],
    'VT': ['VT', 'Vermont', 'VERMONT'],
    'VA': ['VA', 'Virginia', 'VIRGINIA'],
    'WA': ['WA', 'Washington', 'WASHINGTON'],
    'WV': ['WV', 'West Virginia', 'WEST VIRGINIA'],
    'WI': ['WI', 'Wisconsin', 'WISCONSIN'],
    'WY': ['WY', 'Wyoming', 'WYOMING']
}


#Carrier detail view - admin use
class CarrierDetailView(DetailView):
    model = Carrier
    template_name = 'carrier_detail.html'

# webhook from the signing API
def save_carriers_from_api_response(response):
    data = response.json()
    carriers = data.get('partner_carriers', [])

    for carrier_data in carriers:
        try:
            address = ' '.join([
                carrier_data.get('address_1', ''),
                carrier_data.get('address_2', ''),
                carrier_data.get('city', ''),
                carrier_data.get('state', ''),
                carrier_data.get('postal', ''),
                carrier_data.get('country', '')
            ]).strip()

            carrier = Carrier(
                company=carrier_data.get('name'),
                email=carrier_data.get('email'),
                contact=carrier_data.get('dispatch_contact_name'),
                address=address,
                mainphone=carrier_data.get('phone'),
                fax=carrier_data.get('fax'),
                mcnumber=int(carrier_data.get('motor_carrier_id', 0)) if carrier_data.get('motor_carrier_id') else None,
                usdotnumber=int(carrier_data.get('dept_of_transportation_id', 0)) if carrier_data.get('dept_of_transportation_id') else None
            )

            carrier.full_clean()  # This will raise ValidationError if the instance is not valid
            carrier.save()  # Save the instance to the database

        except Exception as e:
            print(f"Error when saving carrier: {e}")


# Index view mainly redirects users based on access
def index(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admindashboard')
        # elif request.user.is_demo:
        #     return redirect('demodashboard')

        return redirect('dashboard')
    return render(request, 'index.html', context)


# EXTERNAL view that allows users to get order details by inputting the "external_id" or "order_id" - no need for authentication
def get_externalId_order_view(request):
    externalId = request.GET.get('external_id')
    orderId = request.GET.get('orderID')
    context = {}
    if externalId or orderId:
        try:
            orderDetail = Order.objects.get(externalid=externalId)
            # orderDetail = DummyOrder.objects.get(externalid=externalId)
            gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
            if orderDetail.longitude and orderDetail.latitude:
                latitude = orderDetail.latitude
                longitude = orderDetail.longitude  
                context["latitude"] = latitude
                context["longitude"] = longitude 
            else:  
                address = orderDetail.customeraddress + " " + orderDetail.customercity + " " + orderDetail.customerstate + " " + orderDetail.customerzip
                try:
                    result = gmaps.geocode(address)[0]
                    
                    latitude = result['geometry']['location']['lat']
                    longitude = result['geometry']['location']['lng']
                    place_id = result['place_id']
                    context["latitude"] = latitude
                    context["longitude"] = longitude

                except Exception as e:
                    print(f"Error geocoding address: {e}")
                
            context["orderDetail"] = orderDetail
            context["key"] = settings.GOOGLE_API_KEY
            
            return render(request, 'order_detail.html', context)
        except ObjectDoesNotExist:
            messages.error(request, f"Order with ID {externalId or orderId} not found")
            return redirect('dashboard')
    messages.error(request, f"please provide an order ID")
    return redirect('dashboard')


class DemoDashboard(LoginRequiredMixin, View):
    template_name = 'demodashboard.html'
    
    def get(self, request):
        if not request.user.is_authenticated:
            # Assuming there's a login page to redirect to
            return redirect('login')

        if request.user.is_staff:
            return redirect('admindashboard')
        

        context = {}

        # modal detail logic 
        externalId = request.GET.get('external_id')
        orderId = request.GET.get('orderID')
        if externalId or orderId:
            try:
                orderDetail = Order.objects.get(user = request.user, externalid=externalId or orderId.strip())
                
                gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
                
                if orderDetail.longitude and orderDetail.latitude:
                    latitude = orderDetail.latitude
                    longitude = orderDetail.longitude  
                     
                    context["latitude"] = latitude
                    context["longitude"] = longitude
                else:  
                    address = orderDetail.customeraddress + " " + orderDetail.customercity + " " + orderDetail.customerstate + " " + orderDetail.customerzip
                    try:
                        result = gmaps.geocode(address)[0]
                        
                        latitude = result['geometry']['location']['lat']
                        longitude = result['geometry']['location']['lng']
                        place_id = result['place_id']
                        
                        context["latitude"] = latitude
                        context["longitude"] = longitude

                    except Exception as e:
                        print(f"Error geocoding address: {e}")
                    
                
                context["orderDetail"] = orderDetail
                context["key"] = settings.GOOGLE_API_KEY
            except ObjectDoesNotExist:
                messages.error(request, f"Order with ID {orderId} not found")
  
        orders = Order.objects.filter(user=request.user)
        
        # hits when the user decides to use a saved template        
        template_id = request.GET.get('template_id')
        if template_id:
            
            template_qs = TemplatedFilters.objects.filter(id=template_id, user=request.user)
            if template_qs.exists():
                template = template_qs[0]
                data = {
                    'start_date': template.start_date,
                    'end_date': template.end_date,
                    'customercity': template.customercity,
                    'customerstate': template.customerstate,
                    'deliverystatus': template.deliverystatus, 
                    'address' : template.address, 
                    'customername' : template.customername
                }
                if str(data['deliverystatus']).lower() == "delivered" or str(data['deliverystatus']).lower() == "pickedup" or str(data['deliverystatus']).lower() == "comfirmed" or str(data['deliverystatus']).lower() == "attempted" or str(data['deliverystatus']).lower() == "statusCodeAdded" and (data['start_date'] and data['end_date']):
                    orders = orders.filter(
                        Q(delivery__gte=data['start_date'], delivery__lte=data['end_date']) | 
                        Q(departed__gte=data['start_date'], departed__lte=data['end_date'])
                    )
                
                # if data['deliverystatus'] :
                #     orders = orders.filter(deliverystatus__in=data['deliverystatus'])
                
                if data['address']:
                    # a Q query to search for the address in the customeraddress, customercity, customerstate, and customerzip fields
                    orders = orders.filter(
                        Q(customeraddress__icontains=str(data['address']).strip()) | 
                        Q(customercity__icontains=str(data['address']).strip()) | 
                        Q(customerstate__icontains=str(data['address']).strip()) | 
                        Q(customeraddress2__icontains=str(data['address']).strip()) | 
                        Q(customerzip__icontains=str(data['address']).strip())
                    )
                    
                if data['customercity']:
                    orders = orders.filter(customercity__icontains=str(data['customercity']).strip())
                if data['customerstate']:
                    orders = orders.filter(customerstate__icontains=str(data['customerstate']).strip())

                if data["customername"]:
                    orders = orders.filter(customername__icontains=str(data['customername']).strip())
                    
                sort = request.GET.get('sort')
                if sort == 'id':
                    orders = orders.order_by('-id')
                elif sort == 'status':
                    orders = orders.order_by('deliverystatus')
                elif sort == 'date':
                    orders = orders.order_by('delivery')
                    
                filter_form = ReportFilterForm(initial=data)
                report_form = GeneratedReportForm()
                paginator = Paginator(orders, 10)  # Show 10 orders per page.
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                total_orders = orders.count()
                calender = ['Daily', 'Weekly', 'Bi-Weekly', 'Monthly']
                context["orders"] = page_obj
                context["total_orders"] = total_orders
                context["filter_form"] = filter_form
                context["report_form"] = report_form
                context["calender"] = calender

                if not any(data.values()):
                    context["orders"] = None
                
                return render(request, 'dashboard.html', context)
        
        data = {
            "deliverystatus" : request.GET.getlist('deliverystatus'), 
            "customerstate" : request.GET.get('customerstate'),
            "customercity" : request.GET.get('customercity'),
            "start_date" : request.GET.get('start_date'),
            "end_date" : request.GET.get('end_date'),
            "address" : request.GET.get('address'), 
            "customername" : request.GET.get('customername')
        }
    
        filter_form = ReportFilterForm(initial = data)
        report_form = GeneratedReportForm(request.POST or None)
        total_orders = orders.count()
        
        # filter login fo regular requests
        if data["deliverystatus"]:
            deliverystatus = data["deliverystatus"]
            print(deliverystatus)
            print(data['start_date'])
            print(data['end_date'])
            # if deliverystatus
            orders = orders.filter(deliverystatus__in=deliverystatus)
            if str(data['deliverystatus']).lower() == "delivered" and (data['start_date'] and data['end_date']):
                orders = orders.filter(
                    Q(delivery__gte=data['start_date'], delivery__lte=data['end_date']) | 
                    Q(departed__gte=data['start_date'], departed__lte=data['end_date'])
                )
            elif "pickedup" in str(data['deliverystatus']).lower() and (data['start_date'] and data['end_date']):
                orders = orders.filter(
                    Q(delivery__gte=data['start_date'], delivery__lte=data['end_date']) | 
                    Q(departed__gte=data['start_date'], departed__lte=data['end_date'])
                )
            if deliverystatus in ["delivered", "statusCodeAdded", "attempted", "pickedup", "confirmed", "placed"] and (data['start_date'] and data['end_date']):
                start_date_str = data["start_date"]
                end_date_str = data["end_date"]
                orders = orders.filter(
                    Q(delivery__gte=start_date_str, delivery__lte=end_date_str) | 
                    Q(departed__gte=start_date_str, departed__lte=end_date_str)
                )
            if deliverystatus in ["delivered", "statusCodeAdded", "attempted", "pickedup", "confirmed", "placed"]:
                start_date_str = data["start_date"]
                end_date_str = data["end_date"]

                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

                if start_date and end_date:
                    orders = orders.filter(
                        Q(delivery__gte=start_date, delivery__lte=end_date) | 
                        Q(departed__gte=start_date, departed__lte=end_date)
                    )

                if start_date and not end_date:
                    end_date = start_date + timedelta(days=1)
                    orders = orders.filter(
                        Q(delivery__range=(start_date, end_date)) | 
                        Q(departed__range=(start_date, end_date)))
        else:
            start_date_str = data["start_date"]
            end_date_str = data["end_date"]
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
            if start_date and end_date:
                orders = orders.filter(
                    Q(delivery__gte=start_date, delivery__lte=end_date) | 
                    Q(departed__gte=start_date, departed__lte=end_date) |
                    Q(placed__gte=start_date, placed__lte=end_date))
                
            if start_date and not end_date:
                    end_date = start_date + timedelta(days=1)
                    orders = orders.filter(
                        Q(delivery__gte=start_date, delivery__lte=end_date) | 
                        Q(departed__gte=start_date, departed__lte=end_date) |
                        Q(placed__gte=start_date, placed__lte=end_date))

        if data["customerstate"]:
            orders = orders.filter(customerstate__icontains=str(data["customerstate"]).strip())
        if data["customercity"]:
            orders = orders.filter(customercity__icontains=str(data["customercity"]).strip())
        
        if data['address']:
            orders = orders.filter(
                Q(customeraddress__icontains=str(data['address']).strip()) | 
                Q(customercity__icontains=str(data['address']).strip()) | 
                Q(customerstate__icontains=str(data['address']).strip()) | 
                Q(customeraddress2__icontains=str(data['address']).strip()) | 
                Q(customerzip__icontains=str(data['address']).strip())
            )
        # orders = orders.order_by('-id')
        if data['customername']:
            orders = orders.filter(customername__icontains=str(data['customername']).strip())
        
        orders = orders.annotate(
            status_order=Case(
                When(deliverystatus='Delivered', then=Value(1)),
                When(deliverystatus='Pickedup', then=Value(2)),
                When(deliverystatus='StatusCodeAdded', then=Value(0)),
                When(deliverystatus='Confirmed', then=Value(4)),
                When(deliverystatus='Placed', then=Value(5)),
                default=Value(6),
                output_field=IntegerField(),
            )
        ).order_by('-delivery')
        
        sort = request.GET.get('sort')
        if sort == 'id':
            orders = orders.order_by('-id')
        elif sort == 'status':
            orders = orders.order_by('deliverystatus')
        elif sort == 'date':
            orders = orders.order_by('delivery')
        
        # Pagination
        paginator = Paginator(orders, 10)  # Show 10 orders per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        calender = ['Daily', 'Weekly', 'Bi-Weekly', 'Monthly']
        
        
        
        context['calender'] = calender
        context['filter_form'] = filter_form
        context['report_form'] = report_form
        context['orders'] = page_obj
        context['total_orders'] = total_orders

        if data["deliverystatus"] and data['start_date'] == '' and data['end_date'] == '':
            context["orders"] = None

        if not any(data.values()):
            context["orders"] = None
        

        return render(request, self.template_name, context)
    
    def post(self, request):
        # when generate report data is submitted   
        orders = Order.objects.filter(user=request.user)
        filter_form = ReportFilterForm(request.POST or None)
        report_form = GeneratedReportForm(request.POST or None)
        
        if report_form.is_valid() and filter_form.is_valid():
            
            deliverystatus = filter_form.cleaned_data['deliverystatus']
            start_date = filter_form.cleaned_data['start_date']
            end_date = filter_form.cleaned_data['end_date']
            customerstate = filter_form.cleaned_data['customerstate']
            customercity = filter_form.cleaned_data['customercity']
            fileFormat = report_form.cleaned_data['report_type']
            address = filter_form.cleaned_data['address']
            customername = filter_form.cleaned_data['customername']
            
            
            if deliverystatus:
                print(deliverystatus)
                print(start_date)
                print(end_date)
                orders = orders.filter(deliverystatus__in=deliverystatus)
                if str(data['deliverystatus']).lower() == "delivered" and (start_date and end_date):
                    orders = orders.filter(
                        Q(delivery__gte=start_date, delivery__lte=end_date) | 
                        Q(departed__gte=start_date, departed__lte=end_date)
                    )
                elif "pickedup" in str(data['deliverystatus']).lower() and (start_date and end_date):
                    orders = orders.filter(
                        Q(delivery__gte=start_date, delivery__lte=end_date) | 
                        Q(departed__gte=start_date, departed__lte=end_date)
                    )
                if deliverystatus in ["delivered", "statusCodeAdded", "attempted", "pickedup", "confirmed", "placed"] and (start_date and end_date):
                    orders = orders.filter(
                        Q(delivery__gte=start_date, delivery__lte=end_date) | 
                        Q(departed__gte=start_date, departed__lte=end_date)
                    )
                if deliverystatus in ["delivered", "statusCodeAdded", "attempted", "pickedup", "confirmed", "placed"]:
                    if start_date and end_date:
                        orders = orders.filter(
                            Q(delivery__gte=start_date, delivery__lte=end_date) | 
                            Q(departed__gte=start_date, departed__lte=end_date)
                        )
                if start_date and not end_date:
                    end_date = start_date + timedelta(days=1)
                    orders = orders.filter(
                        Q(delivery__range=(start_date, end_date)) | 
                        Q(departed__range=(start_date, end_date))
                    )
            else:
                if start_date and end_date:
                    orders = orders.filter(
                        Q(delivery__gte=start_date, delivery__lte=end_date) | 
                        Q(departed__gte=start_date, departed__lte=end_date) |
                        Q(placed__gte=start_date, placed__lte=end_date))
                if start_date and not end_date:
                    end_date = start_date + timedelta(days=1)
                    orders = orders.filter(
                        Q(delivery__gte=start_date, delivery__lte=end_date) | 
                        Q(departed__gte=start_date, departed__lte=end_date) |
                        Q(placed__gte=start_date, placed__lte=end_date))


            if customerstate:
                orders = orders.filter(customerstate__icontains=str(customerstate).strip())
            if customercity:
                orders = orders.filter(customercity__icontains=str(customercity).strip())
            if address:
                orders = orders.filter(
                    Q(customeraddress__icontains=str(address).strip()) | 
                    Q(customercity__icontains=str(address).strip()) | 
                    Q(customerstate__icontains=str(address).strip()) | 
                    Q(customeraddress2__icontains=str(address).strip()) | 
                    Q(customerzip__icontains=str(address).strip())
                )
                
            if customername:
                orders = orders.filter(customername__icontains=str(customername).strip())        

            report_instance = report_form.save(commit=False)
            report_instance.user = request.user            
            
            report_instance.save()

            filter_instance = filter_form.save(commit=False)
            filter_instance.report = report_instance
            
            filter_instance.save()
            
            if fileFormat == "csv":
                return download_csv_report(request, orders)

            else:
                return download_excel_report(request, orders)
            
        else:
            errorResponse = []
            if report_form.errors:
                for field, errors in report_form.errors.items():
                    # messages.error(request, f"{field}: {errors}")
                    for error in errors:
                        errorResponse.append(f"{field}: {error}") 
                        print(f"- {field}: {error}")
            
            if filter_form.errors:
                for field, errors in filter_form.errors.items():
                    for error in errors:
                        # messages.error(request, f"{field}: {errors}")
                        errorResponse.append(f"{field}: {error}") 
                        print(f"- {field}: {error}")
                        
        # return render(request, 'data-report.html', {"orders": orders, 'calendar': calender, "filter_form": filter_form,
        #          "report_form": report_form,})
            return JsonResponse({"error" : errorResponse}, status=400)
       
        
        
   

class Dashboard(LoginRequiredMixin, View):
    template_name = 'dashboard.html'
    
    def get(self, request):
        if not request.user.is_authenticated:
            # Assuming there's a login page to redirect to
            return redirect('login')
        
        # if request.user.is_demo:
        #     return redirect('demodashboard')

        if request.user.is_staff:
            return redirect('admindashboard')
        
        context = {}
        
        # modal detail logic 
        externalId = request.GET.get('external_id')
        orderId = request.GET.get('orderID')
        if externalId or orderId:
            try:
                orderDetail = Order.objects.get(user = request.user, externalid=externalId or orderId.strip())
                # orderDetail = DummyOrder.objects.get(user = request.user, externalid=externalId or orderId.strip())
                
                gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
                
                if orderDetail.longitude and orderDetail.latitude:
                    latitude = orderDetail.latitude
                    longitude = orderDetail.longitude  
                     
                    context["latitude"] = latitude
                    context["longitude"] = longitude
                else:  
                    address = orderDetail.customeraddress + " " + orderDetail.customercity + " " + orderDetail.customerstate + " " + orderDetail.customerzip
                    try:
                        result = gmaps.geocode(address)[0]
                        
                        latitude = result['geometry']['location']['lat']
                        longitude = result['geometry']['location']['lng']
                        place_id = result['place_id']
                        
                        context["latitude"] = latitude
                        context["longitude"] = longitude

                    except Exception as e:
                        print(f"Error geocoding address: {e}")
                    
                
                context["orderDetail"] = orderDetail
                context["key"] = settings.GOOGLE_API_KEY
            except ObjectDoesNotExist:
                messages.error(request, f"Order with ID {orderId} not found")
  
        orders = Order.objects.filter(user=request.user)
        # orders = DummyOrder.objects.filter(user=request.user)
        
        # hits when the user decides to use a saved template        
        template_id = request.GET.get('template_id')
        if template_id:
            
            template_qs = TemplatedFilters.objects.filter(id=template_id, user=request.user)
            if template_qs.exists():
                template = template_qs[0]
                deliverystatus = template.deliverystatus.split(",")
                data = {
                    'start_date': template.start_date,
                    'end_date': template.end_date,
                    'customercity': template.customercity,
                    'customerstate': template.customerstate,
                    'deliverystatus': deliverystatus, 
                    'address' : template.address, 
                    'customername' : template.customername
                }
                if "delivered" in str(data['deliverystatus']).lower() or "pickedup" in str(data['deliverystatus']).lower() or "confirm" in  str(data['deliverystatus']).lower() or  "attempted" in str(data['deliverystatus']).lower() or "statusCodeAdded" in str(data['deliverystatus']).lower() and (data['start_date'] and data['end_date']):
                    orders = orders.filter(
                        Q(delivery__gte=data['start_date'], delivery__lte=data['end_date']) | 
                        Q(departed__gte=data['start_date'], departed__lte=data['end_date'])
                    )
                
                if data['deliverystatus'] :
                    orders = orders.filter(deliverystatus__in=data['deliverystatus'])
                
                if data['address']:
                    # a Q query to search for the address in the customeraddress, customercity, customerstate, and customerzip fields
                    orders = orders.filter(
                        Q(customeraddress__icontains=str(data['address']).strip()) | 
                        Q(customercity__icontains=str(data['address']).strip()) | 
                        Q(customerstate__icontains=str(data['address']).strip()) | 
                        Q(customeraddress2__icontains=str(data['address']).strip()) | 
                        Q(customerzip__icontains=str(data['address']).strip())
                    )
                    
                if data['customercity']:
                    orders = orders.filter(customercity__icontains=str(data['customercity']).strip())
                if data['customerstate']:
                    orders = orders.filter(customerstate__icontains=str(data['customerstate']).strip())

                if data["customername"]:
                    orders = orders.filter(customername__icontains=str(data['customername']).strip())
                    
                sort = request.GET.get('sort')
                if sort == 'id':
                    orders = orders.order_by('-id')
                elif sort == 'status':
                    orders = orders.order_by('deliverystatus')
                elif sort == 'date':
                    orders = orders.order_by('delivery')
                    
                filter_form = ReportFilterForm(initial=data)
                report_form = GeneratedReportForm()
                paginator = Paginator(orders, 10)  # Show 10 orders per page.
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                total_orders = orders.count()
                calender = ['Daily', 'Weekly', 'Bi-Weekly', 'Monthly']
                context["orders"] = page_obj
                context["total_orders"] = total_orders
                context["filter_form"] = filter_form
                context["report_form"] = report_form
                context["calender"] = calender

                if not any(data.values()):
                    context["orders"] = None
                
                return render(request, 'dashboard.html', context)
        
        data = {
            "deliverystatus" : request.GET.getlist('deliverystatus'), 
            "customerstate" : request.GET.get('customerstate'),
            "customercity" : request.GET.get('customercity'),
            "start_date" : request.GET.get('start_date'),
            "end_date" : request.GET.get('end_date'),
            "address" : request.GET.get('address'), 
            "customername" : request.GET.get('customername')
        }
    
        filter_form = ReportFilterForm(initial = data)
        report_form = GeneratedReportForm(request.POST or None)
        total_orders = orders.count()
        
        # filter login fo regular requests
        if data["deliverystatus"]:
            deliverystatus = data["deliverystatus"]
            # if deliverystatus
            orders = orders.filter(deliverystatus__in=deliverystatus)
            if "delivered" in str(deliverystatus).lower() and (data['start_date'] and data['end_date']):
                orders = orders.filter(
                    Q(delivery__gte=data['start_date'], delivery__lte=data['end_date']) | 
                    Q(departed__gte=data['start_date'], departed__lte=data['end_date'])
                )
            elif "pickedup" in str(deliverystatus).lower() and (data['start_date'] and data['end_date']):
                orders = orders.filter(
                    Q(delivery__gte=data['start_date'], delivery__lte=data['end_date']) | 
                    Q(departed__gte=data['start_date'], departed__lte=data['end_date'])
                )
            if deliverystatus in ["delivered", "statusCodeAdded", "attempted", "pickedup", "confirmed", "placed"] and (data['start_date'] and data['end_date']):
                start_date_str = data["start_date"]
                end_date_str = data["end_date"]
                orders = orders.filter(
                    Q(delivery__gte=start_date_str, delivery__lte=end_date_str) | 
                    Q(departed__gte=start_date_str, departed__lte=end_date_str)
                )
            if deliverystatus in ["delivered", "statusCodeAdded", "attempted", "pickedup", "confirmed", "placed"]:
                start_date_str = data["start_date"]
                end_date_str = data["end_date"]

                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

                if start_date and end_date:
                    orders = orders.filter(
                        Q(delivery__gte=start_date, delivery__lte=end_date) | 
                        Q(departed__gte=start_date, departed__lte=end_date)
                    )

                if start_date and not end_date:
                    end_date = start_date + timedelta(days=1)
                    orders = orders.filter(
                        Q(delivery__range=(start_date, end_date)) | 
                        Q(departed__range=(start_date, end_date)))
        else:
            start_date_str = data["start_date"]
            end_date_str = data["end_date"]
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
            if start_date and end_date:
                orders = orders.filter(
                    Q(delivery__gte=start_date, delivery__lte=end_date) | 
                    Q(departed__gte=start_date, departed__lte=end_date) |
                    Q(placed__gte=start_date, placed__lte=end_date))
                
            if start_date and not end_date:
                    end_date = start_date + timedelta(days=1)
                    orders = orders.filter(
                        Q(delivery__gte=start_date, delivery__lte=end_date) | 
                        Q(departed__gte=start_date, departed__lte=end_date) |
                        Q(placed__gte=start_date, placed__lte=end_date))

        if data["customerstate"]:
            orders = orders.filter(customerstate__icontains=str(data["customerstate"]).strip())
        if data["customercity"]:
            orders = orders.filter(customercity__icontains=str(data["customercity"]).strip())
        
        if data['address']:
            orders = orders.filter(
                Q(customeraddress__icontains=str(data['address']).strip()) | 
                Q(customercity__icontains=str(data['address']).strip()) | 
                Q(customerstate__icontains=str(data['address']).strip()) | 
                Q(customeraddress2__icontains=str(data['address']).strip()) | 
                Q(customerzip__icontains=str(data['address']).strip())
            )
        # orders = orders.order_by('-id')
        if data['customername']:
            orders = orders.filter(customername__icontains=str(data['customername']).strip())
        
        orders = orders.annotate(
            status_order=Case(
                When(deliverystatus='Delivered', then=Value(1)),
                When(deliverystatus='Pickedup', then=Value(2)),
                When(deliverystatus='StatusCodeAdded', then=Value(0)),
                When(deliverystatus='Confirmed', then=Value(4)),
                When(deliverystatus='Placed', then=Value(5)),
                default=Value(6),
                output_field=IntegerField(),
            )
        ).order_by('-delivery')
        
        sort = request.GET.get('sort')
        if sort == 'id':
            orders = orders.order_by('-id')
        elif sort == 'status':
            orders = orders.order_by('deliverystatus')
        elif sort == 'date':
            orders = orders.order_by('delivery')
        
        # Pagination
        paginator = Paginator(orders, 10)  # Show 10 orders per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        calender = ['Daily', 'Weekly', 'Bi-Weekly', 'Monthly']
        
        
        
        context['calender'] = calender
        context['filter_form'] = filter_form
        context['report_form'] = report_form
        context['orders'] = page_obj
        context['total_orders'] = total_orders

        if data["deliverystatus"] and data['start_date'] == '' and data['end_date'] == '':
            context["orders"] = None

        if not any(data.values()):
            context["orders"] = None
        

        return render(request, self.template_name, context)
    
    def post(self, request): 
        orders = Order.objects.filter(user=request.user)
        # orders= DummyOrder.objects.filter(user=request.user)
        filter_form = ReportFilterForm(request.POST or None)
        report_form = GeneratedReportForm(request.POST or None)        

        if not filter_form.is_valid() or not report_form.is_valid():
            try:
                status = request.POST.get('deliverystatus')
                if isinstance(status, str):
                    statuss = status
                statuss = status.split(",")

                print(statuss)
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
                customerstate = request.POST.get('customerstate')
                customercity = request.POST.get('customercity')
                address = request.POST.get('address')
                customername = request.POST.get('customername')
                fileFormat = request.POST.get('report_type')
                if statuss:
                    orders = orders.filter(deliverystatus__in=statuss)
                    if statuss in ["delivered", "statusCodeAdded", "attempted", "pickedup", "confirmed", "placed"] and (start_date and end_date):
                        orders = orders.filter(
                            Q(delivery__gte=start_date, delivery__lte=end_date) | 
                            Q(departed__gte=start_date, departed__lte=end_date))
                    elif start_date and not end_date:
                        end_date = start_date + timedelta(days=1)
                        orders = orders.filter(
                            Q(delivery__range=(start_date, end_date)) | 
                            Q(departed__range=(start_date, end_date)))
                
                if customerstate:
                    orders = orders.filter(customerstate__icontains=str(customerstate).strip())
                if customercity:
                    orders = orders.filter(customercity__icontains=str(customercity).strip())
                if address:
                    orders = orders.filter(
                        Q(customeraddress__icontains=str(address).strip()) | 
                        Q(customercity__icontains=str(address).strip()) | 
                        Q(customerstate__icontains=str(address).strip()) | 
                        Q(customeraddress2__icontains=str(address).strip()) | 
                        Q(customerzip__icontains=str(address).strip())
                    )                    
                if customername:
                    orders = orders.filter(customername__icontains=str(customername).strip())
                print(orders)
                if fileFormat == "csv":
                    return download_csv_report(request, orders)
                else:
                    return download_excel_report(request, orders) 
            except:
                errorResponse = []
                if report_form.errors:
                    for field, errors in report_form.errors.items():
                        # messages.error(request, f"{field}: {errors}")
                        for error in errors:
                            errorResponse.append(f"{field}: {error}") 
                            print(f"- {field}: {error}")
            
                if filter_form.errors:
                    for field, errors in filter_form.errors.items():
                        for error in errors:
                            # messages.error(request, f"{field}: {errors}")
                            errorResponse.append(f"{field}: {error}") 
                            print(f"- {field}: {error}")

                return JsonResponse({"error" : errorResponse}, status=400)

        data = filter_form.cleaned_data
        start_date = data.get('start_date')
        status = data.get('deliverystatus')
        end_date = data.get('end_date')
        customerstate = data.get('customerstate')
        customercity = data.get('customercity')
        address = data.get('address')
        customername = data.get('customername')
        fileFormat = report_form.cleaned_data['report_type']

        orders = orders.filter(deliverystatus__in=status) if status else orders
        
        if start_date and end_date:
            date_range = Q(delivery__range=(start_date, end_date)) | Q(departed__range=(start_date, end_date)) | Q(placed__range=(start_date, end_date))
            orders = orders.filter(date_range)

        if not end_date:
            end_date = start_date + timedelta(days=1)
            orders = orders.filter(Q(delivery__range=(start_date, end_date)) | Q(departed__range=(start_date, end_date)) | Q(placed__range=(start_date, end_date)))

        if customerstate:
            orders = orders.filter(customerstate__icontains=str(customerstate).strip())
        if customercity:
            orders = orders.filter(customercity__icontains=str(customercity).strip())
        if address:
            address_filter = Q(customeraddress__icontains=str(address).strip()) | Q(customercity__icontains=str(address).strip()) | Q(customerstate__icontains=str(address).strip()) | Q(customeraddress2__icontains=str(address).strip()) | Q(customerzip__icontains=str(address).strip())
            orders = orders.filter(address_filter)
        if customername:
            orders = orders.filter(customername__icontains=str(customername).strip())

        if fileFormat == "csv":
            return download_csv_report(request, orders)

        else:
            return download_excel_report(request, orders)
               
        

  
#map function for locating orders
def map(request, external_id):
    orderDetail = Order.objects.get(user = request.user, externalid=external_id)
    # orderDetail = DummyOrder.objects.get(user = request.user, externalid=external_id)
    if not orderDetail:
        return HttpResponse(status=404)
    
    latitude = orderDetail.latitude
    longitude = orderDetail.latitude
    zoom = 14
    google_maps_url = f"https://www.google.com/maps/embed/v1/view?key={settings.GOOGLE_API_KEY}&center={4.8167},{7.0333}&zoom={zoom}"
    response = requests.get(google_maps_url)
    # print(response.text)
    
    return render(request, 'map.html', {'response' : response.content})


@login_required
def order_detail(request):
    form = OrderDetailForm(request.GET)
    if form.is_valid():
        external_id = form.cleaned_data['external_id']
        order = Order.objects.filter(externalid=external_id).first()
        # order = DummyOrder.objects.filter(externalid=external_id).first()

        #digital ocean function for images (viewable via DO login)
        if order:
            if order.imageid:
                url = "https://faas-nyc1-2ef2e6cc.doserverless.co/api/v1/namespaces/fn-3ae9e148-dfdc-42d9-8b98-f7f927f85284/actions/ET/images?blocking=true&result=true"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Basic NTU5MTMwNTAtMDIwNi00ZWVlLWJjZDgtZDMxYjdjNjlkNTIwOjdncmpuUDhZNTg5Nng4Z2VlYU8wRGI3b3lhcGlKa1NzeGh2QlYxeU1vZW0yUG9URk9uOVNLdkhVUkVwRHZUaHE="
                }
                data = {
                    "imageid": order.imageid
                }
                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 200:
                    response_data = response.json()
                    image_data = base64.b64decode(response_data['imagedata'])
                    # Convert image to data URL
                    data_url = "data:image/png;base64," + base64.b64encode(image_data).decode()
                    return render(request, 'order_detail.html', {'order': order, 'image_data': data_url})
                else:
                    return HttpResponse(status=404)
            return render(request, 'order_detail.html', {'order': order})
    return redirect('dashboard')

#downloading the report
@login_required
def download_report(request, report_id):
    report = GeneratedReport.objects.get(id=report_id, user = request.user)
    
    if report:
        delivery_status = report.report_filter.statuss
        start_date = report.report_filter.start_date
        end_date = report.report_filter.end_date
        customer_city = report.report_filter.customercity
        customer_state = report.report_filter.customerstate
        reportFormat = report.report_type
        
        orders = Order.objects.filter(user=request.user)
        print(delivery_status)
        # orders = DummyOrder.objects.filter(user=request.user)
        # filte by the report filter if the filter is not empty using
        if delivery_status:
            orders = orders.filter(deliverystatus__in=delivery_status)
        if start_date:
            orders = orders.filter(departed__gte=start_date)
        if end_date:
            orders = orders.filter(delivery__lte=end_date)
        if customer_city:
            orders = orders.filter(customercity__icontains=customer_city)
        if customer_state:
            orders = orders.filter(customerstate__icontains=customer_state)
        
        if reportFormat == "csv": 
            return download_csv_report(request, orders)
        else:
            return download_excel_report(request, orders)
    
    messages.error(request, 'Report not found')    
    return redirect('report_history')
    

#Creating the links for confirmation images in reports - using similar digital ocean flow
def confirmation_image(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    # order = DummyOrder.objects.filter(id=order_id).first()
    if order and order.imageid:
        url = "https://faas-nyc1-2ef2e6cc.doserverless.co/api/v1/namespaces/fn-3ae9e148-dfdc-42d9-8b98-f7f927f85284/actions/ET/images?blocking=true&result=true"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic NTU5MTMwNTAtMDIwNi00ZWVlLWJjZDgtZDMxYjdjNjlkNTIwOjdncmpuUDhZNTg5Nng4Z2VlYU8wRGI3b3lhcGlKa1NzeGh2QlYxeU1vZW0yUG9URk9uOVNLdkhVUkVwRHZUaHE="
        }
        data = {
            "imageid": order.imageid
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            response_data = response.json()
            image_data = base64.b64decode(response_data['imagedata'])
            return HttpResponse(image_data, content_type='image/jpeg')
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=404)

#downloading csv
@login_required
def download_csv(request):
    absolute_url = request.build_absolute_uri()

    today = date.today()
    start_of_month = today.replace(day=1)  
    # Retrieve the date range filter from the request parameters
    start_date_str = request.GET.get('start', start_of_month.strftime('%Y-%m-%d'))
    end_date_str = request.GET.get('end', today.strftime('%Y-%m-%d'))  
    # Parse the date strings into datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()  
    # Filter the orders by user and delivery date range
    queryset = Order.objects.filter(user=request.user)
    queryset = queryset.filter(delivery__gte=start_date)
    queryset = queryset.filter(delivery__lte=end_date)

    state = request.GET.get('state')
    if state:
        state_variants = STATE_MAP.get(state.upper(), [state])
        query = Q()
        for variant in state_variants:
            query |= Q(customerstate__iexact=variant)
        queryset = queryset.filter(query)          

    header_names = [
      "id",
      "externalid",
      "deliverystatus",
      "statuscode",
      "delivery",
      "estimateddelivery",
      "departed",
      "note",
      "signature",
      "latitude",
      "longitude",
      "imageid",
      "confirmationimage",
      "customername",
      "customerphone",
      "customeraddress",
      "customeraddress2",
      "customercity",
      "customerstate",
      "customerzip",
    ]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    # the csv writer
    # csvfile = StringIO()
    writer = csv.writer(response, delimiter=",")
    writer.writerow(header_names)
    for row in queryset:
        # Extract delivery statuses as a list
        delivery_statuses = row.deliverystatus.split(',') if ',' in row.deliverystatus else [row.deliverystatus]

        # Write a separate row for each delivery status
        for delivery_status in delivery_statuses:
            values = [
                row.id,
                row.externalid,
                delivery_status.strip(),
                row.statuscode,
                row.delivery,
                row.estimateddelivery,
                row.departed,
                row.note,
                row.signature,
                row.latitude,
                row.longitude,
                row.imageid,
                row.confirmationimage,
                row.customername,
                row.customerphone,
                row.customeraddress,
                row.customeraddress2,
                row.customercity,
                row.customerstate,
                row.customerzip,
            ]
            writer.writerow(values)  
    return response

#NOT IN USE AUTOMATIONS LOGIC
@login_required
def automations(request):
    reports = GeneratedReport.objects.filter(user=request.user, is_automated=True)
    context = {
        "reports": reports
    }
    return render(request, 'automation.html', context)

def update_automation(request, report_id):
    report = GeneratedReport.objects.get(id=report_id, user=request.user)
    print(report)
    if report:
        report.is_automated = not report.is_automated
        report.save()
        return JsonResponse({"message": "Automation updated successfully"}, status=200)
    return JsonResponse({"message": "Report not found"}, status=404)

#REPORT HISTORY TAB
@login_required
def report_history(request):
    if request.user.is_staff:
        return redirect('admindashboard')

    data = {
        "delivery_status" : request.GET.getlist('deliverystatus'), 
        "start_date" : request.GET.get('start_date'), 
        "end_date" : request.GET.get('end_date'), 
        "customerState" : request.GET.get('customerstate'), 
        "customerCity" : request.GET.get('customercity'), 
    }
    delivery_status = data["delivery_status"]
    start_date = data["start_date"]
    end_date = data["end_date"]
    customerState = data["customerState"]
    customerCity = data["customerCity"]
    # shipper = request.GET.get('shipper')
    
    q_objects = Q(user=request.user)

    # add shipper after getting info
    if delivery_status:
        q_objects &= Q(report_filter__deliverystatus=delivery_status)
    if start_date:
        q_objects &= Q(report_filter__start_date__gte=start_date)
    if end_date:
        q_objects &= Q(report_filter__end_date__lte=end_date)
    if customerState:
        q_objects &= Q(report_filter__customerstate__icontains=customerState)
    if customerCity:
        q_objects &= Q(report_filter__customercity__icontains=customerCity)

    reports = GeneratedReport.objects.filter(q_objects).order_by("-created_at")

    form = FilterForm(initial=data)
    
    paginator = Paginator(reports, 16) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'reports': page_obj, 
        'form': form,
    }
    return render(request, 'report-history.html', context)

# an api that gets template information
def add_report_template(request):
    status = request.POST.get('deliverystatus')
    deliverystatus = status.join(" ")
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    customerstate = request.POST.get('customerstate')
    customercity = request.POST.get('customercity')
    address = request.POST.get('address')
    customername = request.POST.get('customername')

    template_form = TemplatedFiltersForm()
    template_form.deliverystatus = deliverystatus
    template_form.start_date = start_date
    template_form.end_date = end_date
    template_form.customerstate = customerstate
    template_form.customercity = customercity
    template_form.address = address
    template_form.customername = customername
    template_form.user = request.user

    try:
        template_form.save()
        # return json django json response
        return JsonResponse({'message': 'Template added successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'message': f"{str(e)}"}, status=400)

@login_required
def report_templates(request):
    templates = TemplatedFilters.objects.filter(user=request.user).order_by("-id")
    
    context = {
        'templates': templates
    }
    return render(request, 'report-templates.html', context)


#this view could be depreciated - do not know for sure
def generate_csv(queryset):
    header_names = [
      "id",
      "externalid",
      "deliverystatus",
      "statuscode",
      "delivery",
      "estimateddelivery",
      "departed",
      "note",
      "signature",
      "latitude",
      "longitude",
      "imageid",
      "confirmationimage",
      "customername",
      "customerphone",
      "customeraddress",
      "customeraddress2",
      "customercity",
      "customerstate",
      "customerzip",
    ]

    # Create a CSV file in memory
    csvfile = StringIO()
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerow(header_names)
    for row in queryset:
        # Extract delivery statuses as a list
        delivery_statuses = row.deliverystatus.split(',') if ',' in row.deliverystatus else [row.deliverystatus]

        # Write a separate row for each delivery status
        for delivery_status in delivery_statuses:
            values = [
                row.id,
                row.externalid,
                delivery_status.strip(),
                row.statuscode,
                row.delivery,
                row.estimateddelivery,
                row.departed,
                row.note,
                row.signature,
                row.latitude,
                row.longitude,
                row.imageid,
                row.confirmationimage,
                row.customername,
                row.customerphone,
                row.customeraddress,
                row.customeraddress2,
                row.customercity,
                row.customerstate,
                row.customerzip,
            ]
            writer.writerow(values)           
    return csvfile


# def generate_csv(queryset):
    #     header_names = [
    #       "id",
    #       "externalid",
    #       "deliverystatus",
    #       "statuscode",
    #       "delivery",
    #       "estimateddelivery",
    #       "departed",
    #       "note",
    #       "signature",
    #       "latitude",
    #       "longitude",
    #       "imageid",
    #       "confirmationimage",
    #       "customername",
    #       "customerphone",
    #       "customeraddress",
    #       "customeraddress2",
    #       "customercity",
    #       "customerstate",
    #       "customerzip",
    #   ]

    #     # Create a CSV file in memory
    #     csvfile = StringIO()
    #     writer = csv.writer(csvfile, delimiter=",")
    #     writer.writerow(header_names)
    #     for row in queryset:
    #         delivery_list = row.deliverystatus.split(',') if ',' in row.deliverystatus else [row.deliverystatus]
    #         for delivery in delivery_list:
    #             values = []
    #             for field in header_names:
    #                 value = getattr(row, name)
    #                 if callable(value):
    #                     try:
    #                         value = value() or ''
    #                     except:
    #                         value = 'Error retrieving value'
    #                 if field == 'deliverystatus':
    #                     value = delivery.strip()

    #                 if value is None:
    #                     value = ''

    #                 if field == 'confirmationimage':
    #                     value = 'https://portal.357company.com/confirmation_image/' + str(values[0]) + '/'

    #                 values.append(value)
    #             writer.writerow(values)
                
    #     return csvfile

#generate excel
def generate_excel(queryset):
    header_names = [
      "id",
      "externalid",
      "deliverystatus",
      "statuscode",
      "delivery",
      "estimateddelivery",
      "departed",
      "note",
      "signature",
      "latitude",
      "longitude",
      "imageid",
      "confirmationimage",
      "customername",
      "customerphone",
      "customeraddress",
      "customeraddress2",
      "customercity",
      "customerstate",
      "customerzip",
    ]

    data = []
    for row in queryset:
        values = []
        for field in header_names:
            value = getattr(row, field)
            if callable(value):
                try:
                    value = value() or ''
                except:
                    value = 'Error retrieving value'
            if value is None:
                value = ''
                
                # excel doesn't support timezone-aware datetimes, so convert them to naive datetimes 
            if isinstance(value, datetime):
                value = str(value)

            if isinstance(value, list):
                value = ','.join(value)

            if field == 'confirmationimage':
                value = 'https://portal.357company.com/confirmation_image/' + str(values[0]) + '/'

            values.append(value)
        data.append(values)

    # Create a DataFrame and write it to an Excel file in memory
    df = pd.DataFrame(data, columns=header_names)
    excel_file = BytesIO()
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    
    return excel_file

#download excel
def download_excel_report(request, queryset):
    header_names = [
      "id",
      "externalid",
      "deliverystatus",
      "statuscode",
      "delivery",
      "estimateddelivery",
      "departed",
      "note",
      "signature",
      "latitude",
      "longitude",
      "imageid",
      "confirmationimage",
      "customername",
      "customerphone",
      "customeraddress",
      "customeraddress2",
      "customercity",
      "customerstate",
      "customerzip",
    ]

    data = []
    for row in queryset:
        values = []
        for field in header_names:
            value = getattr(row, field)
            if callable(value):
                try:
                    value = value() or ''
                except:
                    value = 'Error retrieving value'
            if value is None:
                value = ''
            
            # excel doesn't support timezone-aware datetimes, so convert them to naive datetimes 
            if isinstance(value, datetime):
                value = str(value)
            
            if isinstance(value, list):
                value = ','.join(value)
            
            if field == 'confirmationimage':
                value = 'https://portal.357company.com/confirmation_image/' + str(values[0]) + '/'

            values.append(value)
        data.append(values)

    # Create a DataFrame and write it to an Excel file in memory
    df = pd.DataFrame(data, columns=header_names)
    excel_file = BytesIO()
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Create a response with the Excel data
    response = HttpResponse(excel_file.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="orders.xlsx"'

    return response

#download CSV
def download_csv_report(request, queryset):
    header_names = [
      "id",
      "externalid",
      "deliverystatus",
      "statuscode",
      "delivery",
      "estimateddelivery",
      "departed",
      "note",
      "signature",
      "latitude",
      "longitude",
      "imageid",
      "confirmationimage",
      "customername",
      "customerphone",
      "customeraddress",
      "customeraddress2",
      "customercity",
      "customerstate",
      "customerzip",
    ]

    # Create a CSV file in memory
    csvfile = StringIO()
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerow(header_names)
    for row in queryset:
        try:
            # Extract delivery statuses as a list
            delivery_statuses = row.deliverystatus.split(',') if ',' in row.deliverystatus else [row.deliverystatus]
            for delivery_status in delivery_statuses:
                values = [
                    row.id,
                    row.externalid,
                    delivery_status.strip(),
                    row.statuscode,
                    row.delivery,
                    row.estimateddelivery,
                    row.departed,
                    row.note,
                    row.signature,
                    row.latitude,
                    row.longitude,
                    row.imageid,
                    row.confirmationimage,
                    row.customername,
                    row.customerphone,
                    row.customeraddress,
                    row.customeraddress2,
                    row.customercity,
                    row.customerstate,
                    row.customerzip,
                ]
                writer.writerow(values)  
        except:
            values = []
            for field in header_names:
                value = getattr(row, field)
                if callable(value):
                    try:
                        value = value() or ''
                    except:
                        value = 'Error retrieving value'
                if value is None:
                    value = ''

                if field == 'confirmationimage':
                    value = 'https://portal.357company.com/confirmation_image/' + str(values[0]) + '/'

                values.append(value)
            writer.writerow(values) 

    # Create a response with the CSV dat
    response = HttpResponse(csvfile.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    return response

def send_csv_report(emails, subject, description, orders):
    csv_file = generate_csv(orders)
    emails = emails.split(',')
    
    if emails[-1] == '': emails.pop()
    email = EmailMessage(
            subject,
            description,
            "info@357company.com",
            emails
            )
    
    email.attach('orders.csv', csv_file.getvalue(), 'text/csv')
    email.send(fail_silently=False)

def send_excel_report(emails, subject, description, orders):
    excel_file = generate_excel(orders)
    emails = emails.split(',')
    if emails[-1] == '': emails.pop()
    email = EmailMessage(
            subject,
            description,
            "info@357company.com",
            emails
            )

    # Attach the Excel file to the email
    email.attach('orders.xlsx', excel_file.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send(fail_silently=False)
    

#unsure what this view does
def data_report(request):
    
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_staff:
        return redirect('admindashboard')
    
    calender = ['Daily', 'Weekly', 'Bi-Weekly', 'Monthly']
    context = {}
    
    if request.method == "GET":
        # orders = Order.objects.filter(user=request.user).order_by('-id')
        orders = ""
        
        filter_form = ReportFilterForm()
        if request.GET.get('external_id'):
            
            orderDetail = Order.objects.get(user = request.user, externalid=request.GET.get('external_id'))
            
            gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
            
            if orderDetail.longitude and orderDetail.latitude:
                latitude = orderDetail.latitude
                longitude = orderDetail.longitude   
            else:  
                address = orderDetail.customeraddress + " " + orderDetail.customercity + " " + orderDetail.customerstate + " " + orderDetail.customerzip
                try:
                    result = gmaps.geocode(address)[0]
                    
                    latitude = result['geometry']['location']['lat']
                    longitude = result['geometry']['location']['lng']
                    place_id = result['place_id']

                except Exception as e:
                    print(f"Error geocoding address: {e}")
                
                
            context["orderDetail"] = orderDetail
            context["key"] = settings.GOOGLE_API_KEY
            context["latitude"] = latitude
            context["longitude"] = longitude
            
        
        
        template_id = request.GET.get('template_id')
        if template_id:
            print
            orders = Order.objects.filter(user=request.user).order_by('-id')
            template = TemplatedFilters.objects.get(id=template_id, user=request.user)
            data = {
                'start_date': template.start_date,
                'end_date': template.end_date,
                'customercity': template.customercity,
                'customerstate': template.customerstate,
                'deliverystatus': template.deliverystatus
            }
            if str(data['deliverystatus']).lower() == "delivered" and (data['start_date'] and data['end_date']):
                orders = Order.objects.filter(
                    Q(delivery__gte=data['start_date'], delivery__lte=data['end_date']) | 
                    Q(departed__gte=data['start_date'], departed__lte=data['end_date'])
                )
            
            if data['deliverystatus'] :
                orders = Order.objects.filter(deliverystatus__in=data['deliverystatus'])
                
            if data['customercity']:
                orders = Order.objects.filter(customercity__icontains=data['customercity'])
            if data['customerstate']:
                orders = Order.objects.filter(customerstate__icontains=data['customerstate'])
            
            filter_form = ReportFilterForm(initial=data)
        
        
        context["filter_form"] = filter_form
        context["calender"] = calender
            
        paginator = Paginator(orders, 10)  # Show 10 orders per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context["orders"] = page_obj
        print(context)
        return render(request, 'dashboard.html', context )
    
    
    if request.method == 'POST':      
        orders = Order.objects.filter(user=request.user).order_by('-id')
        
        
        filter_form = ReportFilterForm(request.POST or None)
        report_form = GeneratedReportForm(request.POST or None)
        
        if report_form.is_valid() and filter_form.is_valid():
            
            deliverystatus = filter_form.cleaned_data['deliverystatus']
            start_date = filter_form.cleaned_data['start_date']
            end_date = filter_form.cleaned_data['end_date']
            customerstate = filter_form.cleaned_data['customerstate']
            customercity = filter_form.cleaned_data['customercity']
            
            deliverystatus = filter_form.cleaned_data['deliverystatus']
            start_date_str = filter_form.cleaned_data['start_date']
            end_date_str = filter_form.cleaned_data['end_date']
            customerstate = filter_form.cleaned_data['customerstate']
            customercity = filter_form.cleaned_data['customercity']
            
          
            if deliverystatus:
                orders = orders.filter(deliverystatus__in=deliverystatus)

            if deliverystatus in ["delivered", "statusCodeAdded", "attempted"]:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

                if start_date and end_date:
                    orders = orders.filter(
                        Q(delivery__gte=start_date, delivery__lte=end_date) | 
                        Q(departed__gte=start_date, departed__lte=end_date)
                    )

            if customerstate:
                orders = orders.filter(customerstate__icontains=customerstate)
            if customercity:
                orders = orders.filter(customercity__icontains=customercity)
            
            
            orders = orders.order_by('-id')
            
            is_automated = request.POST.get("addAutomation", "false").lower() == "true"

            
            
            report_instance = report_form.save(commit=False)
            report_instance.user = request.user
            report_instance.email = report_form.cleaned_data['emailList']  # Use the cleaned email list
            report_instance.is_automated = is_automated
            report_instance.automate = is_automated
            report_instance.save()

            filter_instance = filter_form.save(commit=False)
            filter_instance.report = report_instance
            
            filter_instance.save()
            
            messages.success(request, 'Report and filter saved successfully!')
            
            if report_form.cleaned_data['emailList']:
              if report_form.cleaned_data['report_type'] == "csv":
                send_csv_report(
                    report_form.cleaned_data['emailList'],
                    report_form.cleaned_data['subject'], 
                    report_form.cleaned_data['description'],  
                    orders
                )
            else:
                send_excel_report(
                    report_form.cleaned_data['emailList'],
                    report_form.cleaned_data['subject'], 
                    report_form.cleaned_data['description'],  
                    orders
                )
            
            # if addAutomation:
            #     automationFrequency = request.POST.get('calendarOption')
            #     pass
            
            paginator = Paginator(orders, 2)  # Show 10 orders per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {
                 "orders": page_obj,
                 "filter_form": filter_form,
                 "report_form": report_form,
                 "calender": calender
            }
            
            return redirect('data_report')
            
            # return render(request, 'data-report.html', context)
            
        else:
            if report_form.errors:
                for field, errors in report_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {errors}")
                        
            
            if filter_form.errors:
                for field, errors in filter_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {errors}")
                        
        # return render(request, 'data-report.html', {"orders": orders, 'calendar': calender, "filter_form": filter_form,
        #          "report_form": report_form,})
        return redirect('data_report')
    return render(request, 'data-report.html', {})
############## DEV END #################

#Not really in use tool to parse emails
# def parse_email_text(request):
#     if request.method == 'POST':
#         form = EmailTextForm(request.POST)
#         if form.is_valid():
#             email_text = form.cleaned_data['email_text']
            
#             # Process the email_text using the OpenAI API
#             parsed_data = parse_email_with_gpt(email_text)

#             # Redirect to the QuoteCreateView with the parsed data
#             request.session['parsed_data'] = parsed_data
#             return HttpResponseRedirect(reverse('adminquote'))

#     else:
#         form = EmailTextForm()

#     return render(request, 'parse_email_text.html', {'form': form})


#View to update a carrier
class CarrierUpdateView(UpdateView):
    model = Carrier
    form_class = CarrierDetailForm
    template_name = 'carrier_update.html'  # name of your template
    success_url = reverse_lazy('carrier_list')  # redirect to the list view after successful update

    def form_valid(self, form):
        # You can add any extra operations here if required.
        form.save()
        return super().form_valid(form)

#onboarded carrier view
class CarrierListView(ListView):
    model = Carrier
    template_name = 'carrier_list.html'
    context_object_name = 'carriers'

    def get_queryset(self):
        filter_type = self.request.GET.get('filter', '')
        search_term = self.request.GET.get('search', '').strip()

        # Start with a default queryset
        from django.db.models import Case, When, Value, CharField

        queryset = Carrier.objects.annotate(
            status=Case(
                When(onboarded=True, courier=False, then=Value('Onboarded Carrier')),
                When(contractsigned=False, courier=False, then=Value('Unsigned Carrier')),
                When(contractsigned=True, courier=False, then=Value('Signed Carrier')),
                When(onboarded=True, courier=True, then=Value('Onboarded Courier')),
                When(contractsigned=False, courier=True, then=Value('Unsigned Courier')),
                When(contractsigned=True, courier=True, then=Value('Signed Courier')),
                default=Value('unknown'),
                output_field=CharField(),
            )
        )

        
        if search_term:
            queryset = queryset.filter(company__icontains=search_term)
            
        if filter_type == 'unsigned_carriers':
            queryset = queryset.filter(contractsigned=False, courier=False)
        elif filter_type == 'signed_carriers':
            queryset = queryset.filter(contractsigned=True, courier=False)
        elif filter_type == 'onboarded_carriers':
            queryset = queryset.filter(onboarded=True, courier=False)
        elif filter_type == 'unsigned_couriers':
            queryset = queryset.filter(contractsigned=False, onboarded=False, courier=True)
        elif filter_type == 'signed_couriers':
            queryset = queryset.filter(contractsigned=True, onboarded=False, courier=True)
        elif filter_type == 'onboarded_couriers':
            queryset = queryset.filter(onboarded=True, courier=True)
            
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        counts = {}
        counts[0] = Carrier.objects.filter(contractsigned=False, courier=False).count()
        counts[1] = Carrier.objects.filter(contractsigned=True, courier=False).count()
        counts[2] = Carrier.objects.filter(onboarded=True, courier=False).count()
        counts[3] = Carrier.objects.filter(contractsigned=False, courier=True).count()
        counts[4] = Carrier.objects.filter(contractsigned=True, courier=True).count()
        counts[5] = Carrier.objects.filter(onboarded=True, courier=True).count()

        context['counts'] = counts
        context['fields'] = ['company', 'email', 'phone', 'contact', 'mcnumber', 'usdotnumber', 'feidnumber']
        return context


#staff admin dashboard view
@login_required
def admindashboard(request):
    context = {}
    if not request.user.is_staff:
        # If the user doesn't have the is_staff field set to True, return a denial message
        return HttpResponse("Access denied: You must be a staff member to access this page.")
    
    context['usercount'] = NewUser.objects.count()
    context['carriercount'] = Carrier.objects.count()
    acceptedquotes = Quote.objects.filter(accepted=True)
    context['acceptedquotes'] = len(acceptedquotes)

    # quote = requests.get('https://zenquotes.io/api/today')
    # quote = quote.json()
    # context['quotetext'] = quote[0]['q']
    # context['quoteauthor'] = quote[0]['a']

    revenue = 0
    for quote in acceptedquotes:
        revenue += quote.cost

    context['quoterevenue'] = revenue

    context['ordercount'] = Order.objects.count()

    
    # If the user has the is_staff field set to True, allow access
    return render(request, 'admindashboard.html', context)

#login view
class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')

#signup page
class RegisterPage(FormView):
    redirect_authenticated_user = True
    template_name = 'register.html'
    form_class = Registration
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        
        return super(RegisterPage, self).form_valid(form)

#Upload view for shipping label creation
class InboundUpload(LoginRequiredMixin, CreateView):
    model = InboundOrderCSV
    template_name = 'csvupload.html'
    fields = ['csv']
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

#helper view to actually generate the pdf lables
def generate_pdf(request, group_id):
    # Get the LabelGroup object
    largegroup = LabelGroup.objects.get(id=group_id)

    # Set the response headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{largegroup.user}.pdf"'

    # Create the PDF file
    buffer = BytesIO()

    pdf_file = canvas.Canvas(buffer, pagesize=(letter))

    # Loop over the Label objects and add a new page for each one
    labels = Label.objects.filter(group=largegroup)
    for label in labels:
        # Render the label data in an HTML template

        # set font style and size
        pdf_file.setFont("Helvetica", 10)

        # add a border around the shipping label
        pdf_file.rect(0.5*inch, 4.5*inch, 4*inch, 6*inch)

        # add label text to the PDF file
        pdf_file.drawString(.55*inch, 10.2*inch, "From")
        pdf_file.drawString(1*inch, 10*inch, "Tangelo Group")
        pdf_file.drawString(1*inch, 9.8*inch, str(label.from_address.street_number) + ' ' + str(label.from_address.route))
        pdf_file.drawString(1*inch, 9.6*inch, str(label.from_address.locality.name) + ', ' +  str(label.from_address.locality.state.name) + ', ' + str(label.from_address.locality.postal_code))
        pdf_file.drawString(1*inch, 9.4*inch, str(label.from_address.locality.state.country.name))

        pdf_file.line(0.5*inch, 9.2*inch, 4.5*inch, 9.2*inch)

        pdf_file.drawString(.55*inch, 9*inch, "To")
        pdf_file.drawString(1*inch, 8.8*inch, str(label.name))
        pdf_file.drawString(1*inch, 8.6*inch, str(label.address1) + ' ' + str(label.address2))
        pdf_file.drawString(1*inch, 8.4*inch, str(label.city) + ', ' + str(label.state) + ' ' + str(label.zip))
        pdf_file.drawString(1*inch, 8.2*inch, 'United States')

        # add a horizontal line to separate address and tracking information
        pdf_file.line(0.5*inch, 8*inch, 4.5*inch, 8*inch)

        # add tracking information to the PDF file
        pdf_file.setFont("Helvetica", 8)
        pdf_file.drawString(.55*inch, 7.8*inch, "Date:")
        pdf_file.drawString(1*inch, 7.8*inch, str(label.expected_delivery_date))

        pdf_file.drawString(.55*inch, 7.6*inch, "Ref1:")
        pdf_file.drawString(1*inch, 7.6*inch, str(label.ref1))

        pdf_file.drawString(.55*inch, 7.4*inch, "Ref2:")
        pdf_file.drawString(1*inch, 7.4*inch, str(label.ref2))

        pdf_file.drawString(.55*inch, 7.2*inch, "Ref3:")
        pdf_file.drawString(1*inch, 7.2*inch, str(label.ref3))

        pdf_file.setFont("Helvetica", 10)

        pdf_file.drawString(.55*inch, 7.0*inch, "Ref4:")
        pdf_file.drawString(1*inch, 7.0*inch, str(label.tangelogroup))

        pdf_file.drawString(.55*inch, 6.8*inch, "BoxIds:")

        if label.tangelonumbers:
            if len(label.tangelonumbers) < 50:
                pdf_file.drawString(1.1*inch, 6.8*inch, str(label.tangelonumbers))
            else:
                segments = []
                for i in range(0, len(label.tangelonumbers), 50):
                    segments.append(label.tangelonumbers[i:i+50])

                value = 0
                for string in segments:
                    pdf_file.drawString(1.1*inch, (6.8 - value )*inch, string)
                    value += .2

        pdf_file.setFont("Helvetica", 8)

        pdf_file.drawString(.55*inch, 6.4*inch, "Instr:")

        if len(label.instr) < 60:
            pdf_file.drawString(1*inch, 6.4*inch, str(label.instr))
        else:
            segments = []
            for i in range(0, len(label.instr), 60):
                segments.append(label.instr[i:i+60])

            value = 0
            for string in segments:
                pdf_file.drawString(1*inch, (6.4 - value )*inch, string)
                value += .2

        
        #pdf_file.drawString(.55*inch, 4.55*inch, str(label.tangelogroup) + ' - ' + str(label.tangelonumbers))


        pdf_file.drawString(2*inch, 5.5*inch, str(label.city) + ' - ' + str(label.zip))


        final_size = 100 # arbitrary
        # setting barWidth to 1
        initial_width = 1

        barcode128 = code128.Code128(str(label.ref1), humanReadable=True, barWidth=initial_width,
                                    barHeight=50)
        # creates the barcode, computes the total size
        barcode128._calculate()
        # the quiet space before and after the barcode
        quiet = barcode128.lquiet + barcode128.rquiet
        # total_wid = barWidth*charWid + quiet_space
        # char_wid = (total_width - quiet) / bar_width
        char_width = (barcode128._width - quiet) / barcode128.barWidth
        # now that we have the char width we can calculate the bar width
        bar_width = (final_size - quiet) / char_width
        # set the new bar width
        barcode128.barWidth = bar_width
        # re-calculate
        barcode128._calculate()
        
        wid, hgt = barcode128._width, barcode128._height
        x_pos = 1.75*inch
        y_pos = 4.75*inch
        barcode128.drawOn(pdf_file, x_pos, y_pos)

        # Add a new page for the next label
        pdf_file.showPage()

    # Save the PDF to the buffer and add it to the response
    pdf_file.save()
    buffer.seek(0)
    pdf = buffer.read()
    buffer.close()
    response.write(pdf)

    return response

#not really in use view to parse emails
# def parse_email_with_gpt(email_text):

#     prompt = f'Given the following email text: \n\n {email_text} \n\n, Extract the the following: Ship From Address, Ship To Address, pieces, weight, and dimensions. \n Format the Addresses in the following way: 1 Somewhere Ave, Northcote, VIC 3070, AU. \n Return everything in a python dictionary without any newlines, ready to be converted. /n Call the Ship From Address: pickup in the dictionary and the Ship To Address: dropoff.'




#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=prompt,
#         temperature=0.6,
#         max_tokens=1000,
#         )


#     response = response["choices"][0]["text"]

#     response = response.strip()

#     # Convert the string representation to a Python dictionary
#     response_dict = ast.literal_eval(response)

#     return response_dict

# Another plugin view to upload spreadsheets to upload orders for a specific trucking company
class UDSOrderCreateView(FormView, LoginRequiredMixin):
    template_name = 'udsupload.html'
    form_class = UDSCreate
    success_url = reverse_lazy('admindashboard')

    def form_valid(self, form):

        csv_file = form.cleaned_data['csv']

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        next(reader)

        date_format = "%m/%d/%Y"

        for row in reader:
            order = UDSOrder()
            order.externalid = row[10]
            date_obj = datetime.strptime(row[9], date_format)
            order.date = date_obj
            order.save()

        return redirect(self.get_success_url())


#Creating the labels view
class LabelGroupCreateView(CreateView, LoginRequiredMixin):
    model = LabelGroup
    template_name = 'labelupload.html'
    form_class = LabelGroupForm
    success_url = reverse_lazy('admindashboard')



    def form_valid(self, form):

        # Get the uploaded CSV file from the form
        csv_file = form.cleaned_data['csv']

        # Parse the CSV file
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        next(reader)  # Skip the header row

        # Save the LabelGroup instance
        group = form.save()

        char_to_int = {
            'A': 0,
            'B': 1,
            'C': 2,
            'D': 3,
            'E': 4,
            'F': 5,
            'G': 6,
            'H': 7,
            'I': 8,
            'J': 9,
            'K': 10,
            'L': 11,
            'M': 12,
            'N': 13,
            'O': 14,
            'P': 15,
            'Q': 16,
            'R': 17,
            'S': 18,
            'T': 19,
            'U': 20,
            'V': 21,
            'W': 22,
            'X': 23,
            'Y': 24,
            'Z': 25
        }

        def get_column_index(col_letter, mapping_dict):
            if not col_letter:
                return None
            return mapping_dict.get(col_letter)



        # Create a new Label instance for each row in the CSV file
        for row in reader:
            def get_value(row, index):
                if index is None:
                    return ''
                try:
                    return row[index]
                except IndexError:
                    return ''
            Label.objects.create(
                group=group,
                name=get_value(row, get_column_index(group.namecol, char_to_int)),
                from_address=group.from_address,
                address1=get_value(row, get_column_index(group.address1col, char_to_int)),
                address2=get_value(row, get_column_index(group.address2col, char_to_int)),
                city=get_value(row, get_column_index(group.citycol, char_to_int)),
                state=get_value(row, get_column_index(group.statecol, char_to_int)),
                zip=get_value(row, get_column_index(group.zipcol, char_to_int)),
                expected_delivery_date=group.expected_delivery_date,
                ref1=get_value(row, get_column_index(group.ref1col, char_to_int)),
                ref2=get_value(row, get_column_index(group.ref2col, char_to_int)),
                ref3=get_value(row, get_column_index(group.ref3col, char_to_int)),
                instr=get_value(row, get_column_index(group.istrcol, char_to_int)),
                tangelogroup=get_value(row, get_column_index(group.tangelogroupcol, char_to_int)),
                tangelonumbers=get_value(row, get_column_index(group.tangelonumberscol, char_to_int))
            )



        url = reverse('generate_pdf', args=[group.id])
        response = HttpResponseRedirect(url)

        return response

            #return HttpResponseRedirect(f"{self.request.path}?success=True")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        success = self.request.GET.get('success')
        if success == 'True':
            context['notification'] = 'Form submitted successfully!'
        return context

    
#Update view for carriers
class CarrierFollowUp(UpdateView):
    model = Carrier
    form_class = CarrierForm
    template_name = 'carrier_follow_up.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        carrier = form.save(commit=False)

        manualbrokercarrier = self.request.FILES.get('manualbrokercarrier', None)
        if manualbrokercarrier is not None:
            carrier.contractsigned = True

            self.request.session['skip_signal'] = True
            mutable_post = self.request.POST.copy() 
            mutable_post['skip_signal'] = True 
            self.request.POST = mutable_post 


        carrier.update = False
        carrier.save()
        form.save_m2m()
        
        response = super().form_valid(form)

        # Redirect to the saved sign_page_url
        sign_page_url = self.object.sign_page_url
        if sign_page_url:
            return redirect(sign_page_url)
        else:
            return response
        
    def post(self, request, *args, **kwargs):
        carrier = self.get_object()  # Get the current Carrier object

        if 'save' in request.POST:
            request.session['skip_signal'] = True
            mutable_post = request.POST.copy() 
            mutable_post['skip_signal'] = True 
            request.POST = mutable_post

            # Use carrier.email as the recipient
            send_mail(
                'Your Carrier Onboarding Form has been Saved.',
                'Quote Accepted for ' + str(carrier.cost),
                'info@357company.com',
                [carrier.email],  # Using the email of the carrier
                f'Your form data is saved and you can continue the form at anytime with this link: https://portal.357company.com/carrier/{carrier.id}/followup/')
        else:
            mutable_post = request.POST.copy() 
            request.session['skip_signal'] = False
            mutable_post['skip_signal'] = False
            request.POST = mutable_post 


            return super().post(request, *args, **kwargs)

#Main carrier signup view
class CarrierCreate(CreateView):
    model = Carrier
    template_name = 'carrier.html'
    form_class = CarrierForm

    def form_valid(self, form):
        carrier = form.save(commit=False)
        carrier.update = False
        carrier.save()
        form.save_m2m()

        response = super().form_valid(form)

        # Redirect to the saved sign_page_url
        sign_page_url = self.object.sign_page_url
        if sign_page_url:
            return redirect(sign_page_url)
        else:
            return response

    def get_success_url(self):
        if self.request.session.get('skip_signal', False):
            return reverse('carriers') + '?success=false'
        else:
            return reverse('carriers') + '?success=true'
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)  # or do something else with the errors
        return response
    
    def post(self, request, *args, **kwargs):
        carrier = self.get_object()  # Get the current Carrier object

        if 'save' in request.POST:  
            request.session['skip_signal'] = True
            mutable_post = request.POST.copy() 
            mutable_post['skip_signal'] = True 
            request.POST = mutable_post 

                    # Use carrier.email as the recipient
            send_mail(
                'Your Carrier Onboarding Form has been Saved.',
                'Quote Accepted for ' + str(carrier.cost),
                'info@357company.com',
                [carrier.email],  # Using the email of the carrier
                f'Your form data is saved and you can continue the form at anytime with this link: https://portal.357company.com/carrier/{carrier.id}/followup/')

        else:

            mutable_post = request.POST.copy() 
            request.session['skip_signal'] = False
            mutable_post['skip_signal'] = False
            request.POST = mutable_post 

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if the success parameter is present in the URL query string
        if self.request.GET.get('success') == 'true':
            # Add a success message to the context data
            messages.add_message(self.request, messages.SUCCESS, 'Carrier was created successfully.')

        if self.request.GET.get('success') == 'false':
            # Add a success message to the context data
            messages.add_message(self.request, messages.SUCCESS, 'Your form has been saved, a you have been emailed a link with your data saved into the fields. If you need assistance please contact info@357company.com.')

        return context
    
#View to create groups for all the carriers
class CarrierGroupListView(ListView, FormView):
    model = CarrierGroup
    form_class = CarrierGroupForm
    template_name = 'carrier_group_list.html'
    success_url = reverse_lazy('carrier-group-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CarrierGroupForm()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

#When a quote gets rejected this view is hit to collect a reason as to why
class ReasonCreate(CreateView):
    model = RejectedQuote
    template_name = 'rejected.html'
    fields = ['reason']


    def get_context_data(self, **kwargs):
        context = super(ReasonCreate, self).get_context_data(**kwargs)

        if self.request.GET.get('complete') == 'true':
            context['show'] = False
        else:
            context['show'] = True

        return context
    def get_success_url(self):
        url = reverse('rejectedreason')
        query_kwargs = {'complete' : 'true'}

        return f'{url}?{urlencode(query_kwargs)}'

    def get_form(self, form_class=None):
        form = super(ReasonCreate, self).get_form(form_class)
        form.fields['reason'].required = False
        return form

    def form_valid(self, form):
        quote = self.request.GET.get('id')
        quotemodel = Quote.objects.get(id = quote)
        instance = form.save(commit=False)
        instance.quote = quotemodel
        instance.save()
        return super().form_valid(form)

#Not in use API for orders - serves view JSON
class OrderViewSet(ModelViewSet):
    model = Order
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def pre_save(self, obj):
        obj.user = self.request.user


#View to see orders
def QuoteDashboard(request):
    # Check if user is staff
    if not request.user.is_staff:
        return HttpResponse("Access denied")

    # Find all quotes that don't have a responded value, are true livequotes, and the current date is before the expires date field
    current_date = timezone.now()
    open_quotes = Quote.objects.filter(responded=None, livequote=True, expires__gte=current_date)

    # Find all accepted quotes where the accepted value is set to true
    accepted_quotes = Quote.objects.filter(accepted=True)

    # Find all denied quotes where the accepted value is set to false
    denied_quotes = Quote.objects.filter(accepted=False)

    # Find all live quotes
    live_quotes = Quote.objects.filter(livequote=True)

    # Find all not live quotes
    not_live_quotes = Quote.objects.filter(livequote=False)

    # Create a context dictionary with all the queried data
    context = {
        'open_quotes': open_quotes,
        'accepted_quotes': accepted_quotes,
        'denied_quotes': denied_quotes,
        'all_live_quotes': live_quotes,
        'not_live_quotes': not_live_quotes,
    }

    return render(request, 'quote_dashboard.html', context)

#View to submit support requests
class SupportRequestView(CreateView, LoginRequiredMixin):
    model = SupportMessage
    form_class = SupportRequestForm
    template_name = 'support_request.html'
    success_url = reverse_lazy('support_request')

    def form_valid(self, form):
        instance = form.save(commit = False)
        instance.sender = self.request.user
        instance.save()
        response = super().form_valid(form)

        messages.success(self.request, 'Your support request has been submitted successfully.')

        return response

    def get_success_url(self):
        success_url = super().get_success_url()
        query_string = urlencode({'success': True})
        return f"{success_url}?{query_string}"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        success = self.request.GET.get('success', False)
        context['success'] = success
        return context

def shipperlist(request):
    return render(request, 'shipperlist.html', {})

#View to create quotes
class QuoteCreateView(CreateView):
    form_class = QuoteCreate
    template_name = 'quote_create.html'
    success_url = reverse_lazy('quote_dashboard')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_data = None

    def get_initial(self):
        self.initial_data = self.request.session.pop('parsed_data', None)
        if self.initial_data:

            # Create the Address instances for pickup and dropoff
            pickup_address = Address(raw=self.initial_data['pickup'])
            pickup_address.save()

            dropoff_address = Address(raw=self.initial_data['dropoff'])
            dropoff_address.save()

            # Add the created Address instances to the initial data for the form
            self.initial_data['pickup'] = pickup_address
            self.initial_data['dropoff'] = dropoff_address


            return self.initial_data
        return super().get_initial()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.initial_data:
            context['pickup_address'] = self.initial_data.get('pickup', '')
            context['dropoff_address'] = self.initial_data.get('dropoff', '')

        return context


#View to create quote accounts
class QuoteAccountView(CreateView):
    model = QuoteAccount
    fields = '__all__'
    template_name = 'quote_accountcreate.html'
    success_url = reverse_lazy('quote_dashboard')

#Quote details
class QuoteDetail(DetailView, FormMixin):
    template_name='quotedetail.html'
    model = Quote
    form_class = QuoteForm

    def get_success_url(self):
        url = reverse('quotedetail', args=[str(self.get_object().pk)])
        if self.get_object().accepted == True:
            query_kwargs = {'accepted' : 'true', 'id' : str(self.get_object().id)}
        else:
            url = reverse('rejectedreason')
            query_kwargs = {'accepted' : 'false', 'id' : str(self.get_object().id)}

        return f'{url}?{urlencode(query_kwargs)}'

    def get_context_data(self, **kwargs):
        context = super(QuoteDetail, self).get_context_data(**kwargs)
        context['form'] = QuoteForm(instance=self.get_object())
        context['live'] = self.get_object().livequote

        if timezone.now() > self.get_object().expires:
            context['live'] = False
        
        if self.get_object().hempinsurance != None:
            value = self.get_object().hempinsurance
            isover = False
            if value > 75000:
                isover = True

            cost = (value / 100) * .5

            if isover:
                after = cost - 375
                before = cost
                saved = 375
                context['before'] = int(before)
                context['after'] = int(after)
                context['saved'] = int(saved)
                context['isover'] = isover
            else:
                after = 0
                before = cost
                saved = cost
                context['before'] = int(before)
                context['after'] = int(after)
                context['saved'] = int(saved)
                context['isover'] = isover
   

        
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        if self.request.POST.get('accepted') == 'yes':
            instance.accepted = True
            send_mail(
                str(self.get_object().account.company) + ' Quote Accepted',
                'Quote Accepted for ' + str(self.get_object().cost),
                'info@357company.com',
                ['richard@357company.com', 'jp@357company.com'],
                fail_silently=False
            )
        else:
            instance.accepted = False
            send_mail(
                str(self.get_object().account.company) + 'Quote Rejected',
                'Quote Rejected for ' + str(self.get_object().cost),
                'info@357company.com',
                ['richard@357company.com', 'jp@357company.com'],
                fail_silently=False
            )
        instance.responded = timezone.now()
        instance.pk = self.get_object().pk
        instance.save(update_fields=['accepted', 'responded'])
        return super(QuoteDetail, self).form_valid(form)


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


#Carrier filter view
class CarrierFilterView(ListView):
    model = Carrier
    template_name = 'carrierfilter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        filtered_queryset = CarrierFilter(self.request.GET, queryset=queryset).qs
        context['filter'] = CarrierFilter(self.request.GET, queryset=queryset)
        context['carrier_emails'] = list(filtered_queryset.values_list('email', flat=True))
        if context['carrier_emails']:
            email_query = urlencode({'emails': ','.join(context['carrier_emails'])})
            context['email_url'] = reverse('auction-create') + '?' + email_query
        return context
    
#View to see live auctions - not in use
class AuctionListView(ListView):
    model = Auction
    context_object_name = 'auctions'
    template_name = 'auction_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Queryset for active auctions
        active_auctions = Auction.objects.filter(complete=False)
        context['active_auctions'] = active_auctions
        context['active_auctions_accepted'] = active_auctions.filter(quote__accepted=True)
        context['active_auctions_open'] = active_auctions.filter(quote__accepted=None)
        
        # Queryset for completed auctions
        completed_auctions = Auction.objects.filter(complete=True)
        context['completed_auctions'] = completed_auctions
        
        return context


from django.core.mail import send_mail

#details view for acutions - not in use
class AuctionDetailView(FormMixin, DetailView):
    model = Auction
    context_object_name = 'auction'
    template_name = 'auction_detail.html'
    form_class = AuctionCompleteForm

    def get_success_url(self):
        return reverse('auction-detail', kwargs={'pk': self.object.pk})
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.GET.get('cancel', '') == 'true':
            # Send email notifications to all bidders that they lost the auction
            for bid in self.object.bids.all():
                if not bid.accepted:
                    recipient_email = bid.carrier.email
                    subject = f'Sorry, you did not get the load RFQ #357{self.object.quote.pk}.'
                    message = f'Thank you for your bid of ${bid.price} for RFQ #357{self.object.quote.pk}. Unfortunately, you did not get this load.'
                    send_mail(subject, message, 'info@357company.com', [recipient_email], fail_silently=False)
            # Delete the auction object
            self.object.delete()
            # Redirect to the homepage
            return redirect('auction-list')
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            self.object.complete = True
            self.object.save()

            # Get the winning bid for the auction
            winning_bid = self.object.bids.filter(accepted=True).first()

            if winning_bid:
                # Send an email to the carrier who won the auction
                recipient_email = winning_bid.carrier.email
                subject = 'You won the auction!'
                message = f'Congratulations! You won the load for RFQ #357{self.object.quote.pk} with a bid of ${winning_bid.price}. Our operations team will be in contact soon.'
                send_mail(subject, message, 'info@357company.com', [recipient_email], fail_silently=False)

                            # Send an email to all other carriers who did not win the auction
            bids = self.object.bids.exclude(accepted=True)
            for bid in bids:
                recipient_email = bid.carrier.email
                subject = f'Sorry, you did not win the load RFQ #357{self.object.quote.pk}.'
                message = f'Thank you for your bid of ${bid.price} for RFQ #357{self.object.quote.pk}. Unfortunately, you did not win this load.'
                send_mail(subject, message, 'info@357company.com', [recipient_email], fail_silently=False)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)



#view to create auctions - not in use
class AuctionCreateView(CreateView):
    model = Auction
    form_class = AuctionCreateForm
    template_name = 'auction_create.html'
    success_url = reverse_lazy('auction-create')

    def form_valid(self, form):
        # Get the list of carrier email addresses from the URL parameter
        email_list = self.request.GET.get('emails', '').split(',')

        # Create the Auction object
        auction = form.save(commit=False)
        auction.complete = False
        auction.save()

        # Get the Carrier objects with those email addresses
        carriers = Carrier.objects.filter(email__in=email_list)

        # Add the Carrier objects to the Auction object
        auction.carriers.set(carriers)

        # Send email to each carrier with link to bid form
        for carrier in carriers:
            bid_form_url = self.request.build_absolute_uri(
                reverse_lazy('bid-create', kwargs={'auction_id': auction.id, 'carrier_id': carrier.id})
            )
            send_mail(
                subject='357 RFQ #357{}'.format(auction.id),
                message = 'RFQ #357' + str(auction.id) + '{}: {}'.format(auction.id, bid_form_url),
                from_email='info@357company.com',
                recipient_list=[carrier.email],
                fail_silently=False
            )

        # Call the parent class's form_valid method to save the form instance
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the list of carrier email addresses from the URL parameter
        email_list = self.request.GET.get('emails', '').split(',')

        # Get the Carrier objects with those email addresses
        carriers = Carrier.objects.filter(email__in=email_list)

        # Add the carriers to the context
        context['carriers'] = carriers

        return context

from datetime import datetime
from django.db.models import Count, DateTimeField, ExpressionWrapper, F
from django.db.models.functions import TruncDate, Cast
from django.db.models.functions import Substr
from django.db.models import CharField, Value as V

#Helper func
def convert_datetime_string(datetime_string):
    try:
        # First, try the ISO 8601 format
        dt_format = "%Y-%m-%dT%H:%M:%S"
        return datetime.strptime(datetime_string, dt_format)
    except Exception:
        try:
            # If the first format fails, try the "2023-08-30 20:18:00" format
            dt_format = "%Y-%m-%d %H:%M:%S"
            return datetime.strptime(datetime_string, dt_format)
        except Exception:
            # If both formats fail, return None
            return None

# not in use for analytics testgins
def analytics(request):
    context = {}

    delivered_webhooks = WebHook.objects.filter(EventType='Delivered')

    total_deliveries = delivered_webhooks.count()
    on_time_count = 0
    on_time_pickup = 0

    for webhook in delivered_webhooks:
        due_time = convert_datetime_string(webhook.DueTimeTo)
        delivered_time = convert_datetime_string(webhook.Delivered)
        duepickup = convert_datetime_string(webhook.ReadyTimeTo)
        pickup = convert_datetime_string(webhook.PickedUp)

        
        if due_time and delivered_time and delivered_time <= due_time:
            on_time_count += 1

        if duepickup and pickup and pickup <= duepickup:
            on_time_pickup += 1

    # Calculate percentage
    if total_deliveries == 0:  # Avoid division by zero
        on_time_percentage = 0
    else:
        on_time_percentage = (on_time_count / total_deliveries) * 100
        on_time_percentage_pickup = (on_time_pickup / total_deliveries) * 100

    

    context['on_time_percentage'] = on_time_percentage
    context['on_time_percentage_pickup'] = on_time_percentage_pickup


    print(context)

    return render(request, 'analytics.html', context)
    
#View to see bids in autions
class BidDetailView(FormMixin, DetailView):
    model = Bid
    template_name = 'bid_detail.html'
    form_class = BidAcceptForm
    success_url = reverse_lazy('auction_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            auction = self.object.auction
            auction.bids.exclude(pk=self.object.pk).update(accepted=False)
            self.object.accepted = True
            self.object.save()
            return redirect('auction-detail', pk=auction.pk)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('auction-detail', kwargs={'pk': self.object.auction.pk})

#creating a bid view
class BidCreateView(CreateView):
    model = Bid
    fields = ['price']
    template_name = 'bid_create.html'

    def dispatch(self, request, *args, **kwargs):
        self.auction = get_object_or_404(Auction, id=self.kwargs['auction_id'])
        self.carrier = get_object_or_404(Carrier, id=self.kwargs['carrier_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auction'] = self.auction
        context['carrier'] = self.carrier
        context['quote'] = self.auction.quote
        return context

    def form_valid(self, form):
        # Create the Bid object
        bid = form.save(commit=False)
        bid.auction = self.auction
        bid.carrier = self.carrier
        bid.save()

        # Redirect to the same view with success=true parameter
        return redirect(reverse('bid-create', kwargs={'auction_id': self.auction.id, 'carrier_id': self.carrier.id}) + '?success=true')
    
#BE CAREFUL WITH THIS VIEW WILL SEND OUT AUTO EMAILS
class CarrierCsvUploadView(View):
    template_name = 'carrier_csv_upload.html'
    form_class = CarrierUploadCSVForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'CSV file has been uploaded and processed.')
        else:
            messages.error(request, 'An error occurred.')
        return render(request, self.template_name, {'form': form})

#Document signing webhool
@csrf_exempt
def esign_webhooks(request):
    if request.method == 'POST':
        try:
            payload = request.body
            event = json.loads(payload)

            if event['status'] == 'contract-signed':
                carrier = Carrier.objects.get(carrierbroker=event['data']['contract']['id'])

                carrier.contractsigned = True
                carrier.sign_page_url = event['data']['contract']['contract_pdf_url']

                carrier.save()
            return JsonResponse({"success": True}, status=200)
        except ValueError as e:
            return JsonResponse({"success": True}, status=400)

#MAIN PLUGIN FOR WEBHOOKS WITH CXT TRUCKING COMPANY SOFTWARE

# dop_v1_0f0bdcf0ceab5d3ec522bf7854c6e78b97a533080c7d4412e9244d78a48059cd    for D0
@csrf_exempt
def cxt_webhooks(request):
    if request.method == 'POST':
        try:
            payload = request.body
            event = json.loads(payload)

            print(event)

            date_format = '%Y-%m-%dT%H:%M:%S'

            if event['WebHooks']['Order']['CustID'] != 903726:
                return JsonResponse({"user" : "doesNotExist"})


            instance = WebHook()

            try:
                instance.EventType = event['WebHooks']['Order']['EventType']
            except Exception:
                instance.EventType = ''
            try:
                instance.OrderID = event['WebHooks']['Order']['OrderID']
            except Exception:
                instance.OrderID = ''
            try:
                instance.CustID = event['WebHooks']['Order']['CustID']
            except Exception:
                instance.CustID = ''
            try:
                instance.Status = event['WebHooks']['Order']['Status']
            except Exception:
                instance.Status = ''
            try:
                instance.Caller = event['WebHooks']['Order']['Caller']
            except Exception:
                instance.Caller = ''
            try:
                instance.CustomerBillingGroup = event['WebHooks']['Order']['CustomerBillingGroup']
            except Exception:
                instance.CustomerBillingGroup = ''
            try:
                instance.CSR = event['WebHooks']['Order']['CSR']
            except Exception:
                instance.CSR = ''
            try:
                instance.OrderDate = event['WebHooks']['Order']['OrderDate']
            except Exception:
                instance.OrderDate = ''
            try:
                instance.ReadyTimeFrom = event['WebHooks']['Order']['ReadyTimeFrom']
            except Exception:
                instance.ReadyTimeFrom = ''
            try:
                instance.ReadyTimeTo = event['WebHooks']['Order']['ReadyTimeTo']
            except Exception:
                instance.ReadyTimeTo = ''
            try:
                instance.DueTimeFrom = event['WebHooks']['Order']['DueTimeFrom']
            except Exception:
                instance.DueTimeFrom = ''
            try:
                instance.DueTimeTo = event['WebHooks']['Order']['DueTimeTo']
            except Exception:
                instance.DueTimeTo = ''
            try:
                instance.Reference1 = event['WebHooks']['Order']['Reference1']
            except Exception:
                instance.Reference1 = ''
            try:
                instance.Reference2 = event['WebHooks']['Order']['Reference2']
            except Exception:
                instance.Reference2 = ''
            try:
                instance.OriginName = event['WebHooks']['Order']['OriginName']
            except Exception:
                instance.OriginName = ''
            try:
                instance.OriginAddress = event['WebHooks']['Order']['OriginAddress']
            except Exception:
                instance.OriginAddress = ''
            try:
                instance.OriginCity = event['WebHooks']['Order']['OriginCity']
            except Exception:
                instance.OriginCity = ''
            try:
                instance.OriginState = event['WebHooks']['Order']['OriginState']
            except Exception:
                instance.OriginState = ''
            try:
                instance.OriginZip = event['WebHooks']['Order']['OriginZip']
            except Exception:
                instance.OriginZip = ''
            try:
                instance.OriginPlus4 = event['WebHooks']['Order']['OriginPlus4']
            except Exception:
                instance.OriginPlus4 = ''
            try:
                instance.OriginPhone = event['WebHooks']['Order']['OriginPhone']
            except Exception:
                instance.OriginPhone = ''
            try:
                instance.OriginComments = event['WebHooks']['Order']['OriginComments']
            except Exception:
                instance.OriginComments = ''
            try:
                instance.OriginValidated = event['WebHooks']['Order']['OriginValidated']
            except Exception:
                instance.OriginValidated = ''
            try:
                instance.DestName = event['WebHooks']['Order']['DestName']
            except Exception:
                instance.DestName = ''
            try:
                instance.DestAddress = event['WebHooks']['Order']['DestAddress']
            except Exception:
                instance.DestAddress = ''
            try:
                instance.DestCity = event['WebHooks']['Order']['DestCity']
            except Exception:
                instance.DestCity = ''
            try:
                instance.DestState = event['WebHooks']['Order']['DestState']
            except Exception:
                instance.DestState =''
            try:
                instance.DestZip = event['WebHooks']['Order']['DestZip']
            except Exception:
                instance.DestZip = ''
            try:
                instance.DestPlus4 = event['WebHooks']['Order']['DestPlus4']
            except Exception:
                instance.DestPlus4 = ''
            try:
                instance.DestPhone = event['WebHooks']['Order']['DestPhone']
            except Exception:
                instance.DestPhone = ''
            try:
                instance.DestComments = event['WebHooks']['Order']['DestComments']
            except Exception:
                instance.DestComments = ''
            try:
                instance.DestValidated = event['WebHooks']['Order']['DestValidated']
            except Exception:
                instance.DestValidated = ''
            try:
                instance.Pieces = event['WebHooks']['Order']['Pieces']
            except Exception:
                instance.Pieces = ''
            try:
                instance.ParcelType = event['WebHooks']['Order']['ParcelType']
            except Exception:
                instance.ParcelType = ''
            try:
                instance.ParcelLength = event['WebHooks']['Order']['ParcelLength']
            except Exception:
                instance.ParcelLength = ''
            try:
                instance.ParcelWidth = event['WebHooks']['Order']['ParcelWidth']
            except Exception:
                instance.ParcelWidth = ''
            try:
                instance.ParcelHeight = event['WebHooks']['Order']['ParcelHeight']
            except Exception:
                instance.ParcelHeight = ''
            try:
                instance.Weight = event['WebHooks']['Order']['Weight']
            except Exception:
                instance.Weight = ''
            try:
                instance.OrderType = event['WebHooks']['Order']['OrderType']
            except Exception:
                instance.OrderType = ''
            try:
                instance.SpecialInst = event['WebHooks']['Order']['SpecialInst']
            except Exception:
                instance.SpecialInst = ''
            try:
                instance.Distance = event['WebHooks']['Order']['Distance']
            except Exception:
                instance.Distance = ''
            try:
                instance.Route = event['WebHooks']['Order']['Route']
            except Exception:
                instance.Route = ''
            try:
                instance.RouteStop = event['WebHooks']['Order']['RouteStop']
            except Exception:
                instance.RouteStop = ''
            try:
                instance.IsParent = event['WebHooks']['Order']['IsParent']
            except Exception:
                instance.IsParent = ''
            try:
                instance.EmailPod = event['WebHooks']['Order']['EmailPod']
            except Exception:
                instance.EmailPod = ''
            try:
                instance.Workstation = event['WebHooks']['Order']['Workstation']
            except Exception:
                instance.Workstation = ''
            try:
                instance.ReadyToDay = event['WebHooks']['Order']['ReadyToDay']
            except Exception:
                instance.ReadyToDay = ''
            try:
                instance.DueFromDay = event['WebHooks']['Order']['DueFromDay']
            except Exception:
                instance.DueFromDay = ''
            try:
                instance.DueToDay = event['WebHooks']['Order']['DueToDay']
            except Exception:
                instance.DueToDay = ''
            try:
                instance.CreatedBy = event['WebHooks']['Order']['CreatedBy']
            except Exception:
                instance.CreatedBy = ''
            try:
                instance.CreatedWhen = event['WebHooks']['Order']['CreatedWhen']
            except Exception:
                instance.CreatedWhen = ''
            try:
                instance.UpdatedBy = event['WebHooks']['Order']['UpdatedBy']
            except Exception:
                instance.UpdatedBy = ''
            try:
                instance.UpdatedWhen = event['WebHooks']['Order']['UpdatedWhen']
            except Exception:
                instance.UpdatedWhen = ''
            try:
                instance.RateLockedBy = event['WebHooks']['Order']['RateLockedBy']
            except Exception:
                instance.RateLockedBy = ''
            try:
                instance.SettlementStatus = event['WebHooks']['Order']['SettlementStatus']
            except Exception:
                instance.SettlementStatus = ''
            try:
                instance.EmailPODChecked = event['WebHooks']['Order']['EmailPODChecked']
            except Exception:
                instance.EmailPODChecked = ''
            try:
                instance.EmailPOPChecked = event['WebHooks']['Order']['EmailPOPChecked']
            except Exception:
                instance.EmailPOPChecked = ''
            try:
                instance.EmailOrderConfirmationChecked = event['WebHooks']['Order']['EmailOrderConfirmationChecked']
            except Exception:
                instance.EmailOrderConfirmationChecked = ''
            try:
                instance.OriginLat = event['WebHooks']['Order']['OriginLat']
            except Exception:
                instance.OriginLat = ''
            try:
                instance.OriginLon = event['WebHooks']['Order']['OriginLon']
            except Exception:
                instance.OriginLon = ''
            try:
                instance.DestLat = event['WebHooks']['Order']['DestLat']
            except Exception:
                instance.DestLat = ''
            try:
                instance.DestLon = event['WebHooks']['Order']['DestLon']
            except Exception:
                instance.DestLon = ''
            try:
                instance.DriverPayLockedBy = event['WebHooks']['Order']['DriverPayLockedBy']
            except Exception:
                instance.DriverPayLockedBy = ''
            try:
                instance.DispatchFlag = event['WebHooks']['Order']['DispatchFlag']
            except Exception:
                instance.DispatchFlag = ''
            try:
                instance.BOL = event['WebHooks']['Order']['BOL']
            except Exception:
                instance.BOL = ''
            try:
                instance.MasterBOL = event['WebHooks']['Order']['MasterBOL']
            except Exception:
                instance.MasterBOL = ''
            try:
                instance.OrderCount = event['WebHooks']['Order']['OrderCount']
            except Exception:
                instance.OrderCount = ''
            try:
                instance.OriginCountry = event['WebHooks']['Order']['OriginCountry']
            except Exception:
                instance.OriginCountry = ''
            try:
                instance.DestCountry = event['WebHooks']['Order']['DestCountry']
            except Exception:
                instance.DestCountry = ''
            try:
                instance.OriginAddress2 = event['WebHooks']['Order']['OriginAddress2']
            except Exception:
                instance.OriginAddress2 = ''
            try:
                instance.DestAddress2 = event['WebHooks']['Order']['DestAddress2']
            except Exception:
                instance.DestAddress2 = ''
            try:
                instance.RequiredDriverInput = event['WebHooks']['Order']['RequiredDriverInput']
            except Exception:
                instance.RequiredDriverInput = ''
            try:
                instance.RequiredDriverInputTypeDescription = event['WebHooks']['Order']['RequiredDriverInputTypeDescription']
            except Exception:
                instance.RequiredDriverInputTypeDescription = ''
            try:
                instance.Signature = event['WebHooks']['Order']['Signature']
            except Exception:
                instance.Signature = ''
            try:
                instance.AssignedFleet = event['WebHooks']['Order']['OrderStatus']['AssignedFleet']
            except Exception:
                instance.AssignedFleet = ''
            try:
                instance.Barcode = event['WebHooks']['Order']['OrderStatus']['Barcode']
            except Exception:
                instance.Barcode = ''
            try:
                instance.Ordered = event['WebHooks']['Order']['OrderStatus']['Ordered']
            except Exception:
                instance.Ordered = ''
            try:
                instance.Dispatched = datetime.strptime(event['WebHooks']['Order']['OrderStatus']['Dispatched'], date_format)
            except Exception:
                instance.Dispatched = None
            try:
                instance.Confirmed = datetime.strptime(event['WebHooks']['Order']['OrderStatus']['Confirmed'], date_format)
            except Exception:
                instance.Confirmed = None
            try:
                instance.AtOrigin = event['WebHooks']['Order']['OrderStatus']['AtOrigin']
            except Exception:
                instance.AtOrigin = None
            try:
                instance.ScannedAtPickup = event['WebHooks']['Order']['OrderStatus']['ScannedAtPickup']
            except Exception:
                instance.ScannedAtPickup = None
            try:
                instance.PickedUp = datetime.strptime(event['WebHooks']['Order']['OrderStatus']['PickedUp'], date_format)
            except Exception:
                instance.PickedUp = None
            try:
                instance.AtDestination = event['WebHooks']['Order']['OrderStatus']['AtDestination']
            except Exception:
                instance.AtDestination = None
            try:
                instance.ScannedAtDelivery = event['WebHooks']['Order']['OrderStatus']['ScannedAtDelivery']
            except Exception:
                instance.ScannedAtDelivery = None
            try:
                instance.Delivered = datetime.strptime(event['WebHooks']['Order']['OrderStatus']['Delivered'], date_format)
            except Exception:
                instance.Delivered = None
            try:
                instance.Pod = event['WebHooks']['Order']['OrderStatus']['Pod']
            except Exception:
                instance.Pod = ''
            try:
                instance.PodComments = event['WebHooks']['Order']['OrderStatus']['PodComments']
            except Exception:
                instance.PodComments = ''
            try:
                instance.PaidDocument = event['WebHooks']['Order']['OrderStatus']['PaidDocument']
            except Exception:
                instance.PaidDocument = ''
            try:
                instance.CreatedBy = event['WebHooks']['Order']['OrderStatus']['CreatedBy']
            except Exception:
                instance.CreatedBy = ''
            try:
                instance.CreatedWhen = event['WebHooks']['Order']['OrderStatus']['CreatedWhen']
            except Exception:
                instance.CreatedWhen = ''
            try:
                instance.UpdatedBy = event['WebHooks']['Order']['OrderStatus']['UpdatedBy']
            except Exception:
                instance.UpdatedBy =''
            try:
                instance.UpdatedWhen = event['WebHooks']['Order']['OrderStatus']['UpdatedWhen']
            except Exception:
                instance.UpdatedWhen = ''
            try:
                instance.DepotScan = event['WebHooks']['Order']['OrderStatus']['AssignedFleet']
            except Exception:
                instance.DepotScan = ''
            try:
                instance.LocalName = event['WebHooks']['Order']['Customer']['LocalName']
            except Exception:
                instance.LocalName = ''
            try:
                instance.LocalAddress = event['WebHooks']['Order']['Customer']['LocalAddress']
            except Exception:
                instance.LocalAddress = ''
            try:
                instance.LocalAddress2 = event['WebHooks']['Order']['Customer']['LocalAddress2']
            except Exception:
                instance.LocalAddress2 = ''
            try:
                instance.LocalCity = event['WebHooks']['Order']['Customer']['LocalCity']
            except Exception:
                instance.LocalCity = ''
            try:
                instance.LocalState = event['WebHooks']['Order']['Customer']['LocalState']
            except Exception:
                instance.LocalState = ''
            try:
                instance.LocalZip = event['WebHooks']['Order']['Customer']['LocalZip']
            except Exception:
                instance.LocalZip = ''
            try:
                instance.LocalPlus4 = event['WebHooks']['Order']['Customer']['LocalPlus4']
            except Exception:
                instance.LocalPlus4 = ''
            try:
                instance.LocalPhone1 = event['WebHooks']['Order']['Customer']['LocalPhone1']
            except Exception:
                instance.LocalPhone1 = ''
            try:
                instance.LocalPhone2 = event['WebHooks']['Order']['Customer']['LocalPhone2']
            except Exception:
                instance.LocalPhone2 = ''
            try:
                instance.LocalEmail = event['WebHooks']['Order']['Customer']['LocalEmail']
            except Exception:
                instance.LocalEmail = ''
            try:
                instance.LocalContact = event['WebHooks']['Order']['Customer']['LocalContact']
            except Exception:
                instance.LocalContact = ''
            try:
                instance.ParcelPKID = event['WebHooks']['Order']['Parcels']['Parcel']['PKID']
            except Exception:
                instance.ParcelPKID = ''
            try:
                instance.ParcelPieces = event['WebHooks']['Order']['Parcels']['Parcel']['Pieces']
            except Exception:
                instance.ParcelPieces = ''
            try:
                instance.ParcelWeight = event['WebHooks']['Order']['Parcels']['Parcel']['Weight']
            except Exception:
                instance.ParcelWeight = ''
            try:
                instance.ParcelReference = event['WebHooks']['Order']['Parcels']['Parcel']['Reference']
            except Exception:
                instance.ParcelReference = ''
            try:
                instance.ParcelType = event['WebHooks']['Order']['Parcels']['Parcel']['Type']
            except Exception:
                instance.ParcelType = ''
            try:
                instance.DriverPKID = event['WebHooks']['Order']['Drivers']['Driver']['PKID']
            except Exception:
                instance.DriverPKID = ''
            try:
                instance.DriverOrderID = event['WebHooks']['Order']['Drivers']['Driver']['OrderID']
            except Exception:
                instance.DriverOrderID = ''
            try:
                instance.DriverDriverID = event['WebHooks']['Order']['Drivers']['Driver']['DriverID']
            except Exception:
                instance.DriverDriverID = ''
            try:
                instance.DriverDriverPercent = event['WebHooks']['Order']['Drivers']['Driver']['DriverPercent']
            except Exception:
                instance.DriverDriverPercent = ''
            try:
                instance.DriverCreatedBy = event['WebHooks']['Order']['Drivers']['Driver']['CreatedBy']
            except Exception:
                instance.DriverCreatedBy = ''
            try:
                instance.DriverCreatedWhen = event['WebHooks']['Order']['Drivers']['Driver']['CreatedWhen']
            except Exception:
                instance.DriverCreatedWhen = ''
            try:
                instance.DriverUpdatedBy = event['WebHooks']['Order']['Drivers']['Driver']['UpdatedBy']
            except Exception:
                instance.DriverUpdatedBy = ''
            try:
                instance.DriverUpdatedWhen = event['WebHooks']['Order']['Drivers']['Driver']['UpdatedWhen']
            except Exception:
                instance.DriverUpdatedWhen = ''
            try:
                instance.DriverPayAmount = event['WebHooks']['Order']['Drivers']['Driver']['PayAmount']
            except Exception:
                instance.DriverPayAmount = ''
            try:
                instance.DriverFirstName = event['WebHooks']['Order']['Drivers']['Driver']['FirstName']
            except Exception:
                instance.DriverFirstName = ''
            try:
                instance.DriverLastName = event['WebHooks']['Order']['Drivers']['Driver']['LastName']
            except Exception:
                instance.DriverLastName = ''
            try:
                instance.DriverVehicleDescription = event['WebHooks']['Order']['Drivers']['Driver']['VehicleDescription']
            except Exception:
                instance.DriverVehicleDescription = ''
            try:
                instance.DriverVehicleLicensePlate = event['WebHooks']['Order']['Drivers']['Driver']['VehicleLicensePlate']
            except Exception:
                instance.DriverVehicleLicensePlate = ''
            try:
                instance.DriverVehicleLicenseState = event['WebHooks']['Order']['Drivers']['Driver']['VehicleLicenseState']
            except Exception:
                instance.DriverVehicleLicenseState = ''
            try:
                instance.DriverFleet = event['WebHooks']['Order']['Drivers']['Driver']['Fleet']
            except Exception:
                instance.DriverFleet = ''
            try:
                instance.DriverLastReportLat = event['WebHooks']['Order']['Drivers']['Driver']['LastReportLat']
            except Exception:
                instance.DriverLastReportLat = ''
            try:
                instance.DriverLastReportLon = event['WebHooks']['Order']['Drivers']['Driver']['LastReportLon']
            except Exception:
                instance.DriverLastReportLon = ''
            try:
                instance.DriverLastReportTime = event['WebHooks']['Order']['Drivers']['Driver']['LastReportTime']
            except Exception:
                instance.DriverLastReportTime = ''
            try:
                instance.imageid = event['WebHooks']['Order']['Attachments']['Attachment'][0]['AttachmentID']
            except Exception:
                instance.imageid = ''
            
            instance.save()

            statuscodes= [statuscode.get('statusCode', '') for statuscode in event.get('WebHooks', {}).get('Order', {}).get('StatusCodes', {}).get('StatusCode', [])]

            print(statuscodes)


            # Create a dictionary to map the event types
            event_type_mapping = {
                'Placed': 'placed',
                'Confirmed': 'confirmed',
                'Delivered': 'delivered',
                'PickedUp': 'pickedup',
                'StatusCodeAdded': 'statusCodeAdded',
                'Attempted Delivery': 'attempted',
            }

            if instance.CustID == 903726:
                    
                    user = NewUser.objects.get(email = 'user@jointangelo.com')

                    order, created = Order.objects.get_or_create(externalid=instance.Reference1, user_id=user.id)
                    order.deliverystatus = event_type_mapping.get(instance.EventType, 'placed')
                    order.delivery = instance.Delivered
                    order.departed = instance.PickedUp
                    order.podname = instance.Pod
                    order.placed = instance.Confirmed
                    order.podcomments = instance.PodComments
                    order.note = instance.PodComments and instance.Pod
                    order.signature = instance.Signature
                    order.latitude = instance.DriverLastReportLat
                    order.longitude = instance.DriverLastReportLon
                    order.customername = instance.DestName
                    order.customerphone = instance.DestPhone
                    order.customeraddress = instance.DestAddress
                    order.customercity = instance.DestCity
                    order.customerstate = instance.DestState
                    order.customerzip = instance.DestZip
                    order.imageid = instance.imageid

                    status_code_mapping = {
                        'AN': 'Area Not Accesible',
                        'BA': 'Bad Address',
                        'CR': 'Customer Related',
                        'NG': 'Need Gate Code',
                        'NT': 'No Longer Lives There',
                        'UG': 'No Access'
                    }

                    statuscodes = [sc for sc in statuscodes if sc != 'OutsideGeo']

                    if statuscodes:
                        order.deliverystatus = 'attempted'
                        order.statuscode = ' | '.join([f"{sc} - {status_code_mapping.get(sc, sc)}" for sc in statuscodes])

                    order.save()

                    instance.Order = order
                    instance.save()

            

            return JsonResponse({"success": True}, status=200)
        except ValueError as e:
            return JsonResponse({"success": True}, status=400)

