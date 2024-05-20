from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
import socket
socket.gethostbyname('')
from django.template.loader import render_to_string
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save
import requests
from django.dispatch import receiver
import json

from address.models import AddressField
from phonenumber_field.modelfields import PhoneNumberField
import csv
from django.core.mail import send_mail
from datetime import datetime
# from MyMultiSelectField.db.fields import MultiSelectField
from .management.customselect.multiselect import MyMultiSelectField


# Create your models here.

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, company_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, company_name, password, **other_fields)

    def create_user(self, email, user_name, company_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          company_name=company_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

class NewUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=500, null=True)
    user_name = models.CharField(max_length=500)
    company_name = models.CharField(max_length=500)
    position = models.CharField(max_length=500, null=True)
    website = models.CharField(max_length=500, null=True)
    orders = models.CharField(max_length=500, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_demo = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    company_address = AddressField(related_name='Company Address+', blank=True, null=True)
    company_phone = PhoneNumberField(blank=True)
    onboard = models.BooleanField(default=False)

    

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'company_name',]

    def __str__(self):
        return self.email


DELIVERY_STATUS_CHOICES = [
        ('placed', 'Placed'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('pickedup', 'PickedUp'),
        ('statusCodeAdded', 'StatusCodeAdded'),
        ('attempted', 'Attempted Delivery'),
    ]

class Order(models.Model):
    externalid = models.CharField(max_length=500, null=True)
    deliverystatus = models.CharField(choices=DELIVERY_STATUS_CHOICES, max_length=500, null=True)
    statuscode = models.CharField(max_length=500, null=True)
    delivery = models.DateTimeField(null=True)
    estimateddelivery = models.DateTimeField(null=True)
    departed = models.DateTimeField(null=True)
    placed = models.DateTimeField(null=True)
    podname = models.CharField(max_length=500, null=True)
    podcomments = models.TextField(null=True)
    note = models.TextField(null=True)
    signature = models.TextField(null=True)
    latitude = models.CharField(max_length=500, null=True)
    longitude = models.CharField(max_length=500, null=True)
    imageid = models.CharField(max_length=500, null=True)
    confirmationimage = models.TextField(null=True)
    customername = models.CharField(max_length=300, null=True)
    customerphone = models.CharField(max_length=500, null=True)
    customeraddress = models.CharField(max_length=300, null=True)
    customeraddress2 = models.CharField(max_length=300, null=True)
    customercity = models.CharField(max_length=300, null=True)
    customerstate = models.CharField(max_length=300, null=True)
    customerzip = models.CharField(max_length=300, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


    
class GeneratedReport(models.Model):
    
    def user_directory_path(instance, filename):
      # Check if the instance has a user and the user is not None
        if instance.user and hasattr(instance.user, 'id'):
            user_id = instance.user.id
            random_chars = get_random_string(length=4, allowed_chars='0123456789')
            upload_path = f'{user_id}/{random_chars}/{filename}'
        else:
            # Default path or handling for when user is None
            # You can customize this part as needed
            random_chars = get_random_string(length=4, allowed_chars='0123456789')
            upload_path = f'unknown_user/{random_chars}/{filename}'
        return upload_path
    
    REPORT_TYPE_CHOICES = [
        ('csv', 'CSV'),
        ('excel', 'Excel'),
    ]
    
    SCHEDULE_CHOICES = (
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Bi-Weekly', 'Bi-Weekly'),
        ('Monthly', 'Monthly'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null = True) #TODO Should remove null before deployemnt
    report_type = models.CharField(max_length=5, choices=REPORT_TYPE_CHOICES)
    deliverystatus = MyMultiSelectField(min_choices= 1, max_choices=7, max_length=80, choices=DELIVERY_STATUS_CHOICES, null=True)
    schedule = models.CharField(max_length=10, choices=SCHEDULE_CHOICES, default=1, null = True)
    email = models.TextField(null = True)  # Can contain many emails separated by a comma
    subject = models.CharField(max_length=255, null = True)
    description = models.TextField(null = True)
    file = models.FileField(blank=True, null=True, upload_to=user_directory_path)
    is_automated = models.BooleanField(default=False)
    reportorder = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    automate = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null = True)
    
    def __str__(self):
        return self.user.email

class Filters(models.Model):
    
    start_date = models.DateTimeField(null=True, blank=True)
    end_date  = models.DateTimeField(null=True, blank=True)
    customercity = models.CharField(max_length=300, null=True)
    customerstate = models.CharField(max_length=300, null=True)
    deliverystatus = MyMultiSelectField(min_choices= 1, max_choices=7, max_length=80, choices=DELIVERY_STATUS_CHOICES, null=True)
    address = models.CharField(max_length=500, null=True)
    customername = models.CharField(max_length=300, null=True)
    
    class Meta:
        abstract = True
        
class ReportFilter(Filters):
    report = models.OneToOneField(GeneratedReport, on_delete=models.CASCADE, related_name='report_filter')
    def __str__(self):
        return str(self.report.subject)

class TemplatedFilters(Filters):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
    
    
class OrderCSV(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    csv = models.FileField(upload_to='csvs')

    def __str__(self):
        return str(self.user)

class InboundOrderCSV(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    csv = models.FileField(upload_to='csvs')

    def __str__(self):
        return str(self.user)

class WebHook(models.Model):
    Order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='order_webhook')
    EventType = models.CharField(max_length=500, null=True)
    OrderID = models.CharField(max_length=500, null=True)
    CustID = models.CharField(max_length=500, null=True)
    Status = models.CharField(max_length=500, null=True)
    Caller = models.CharField(max_length=500, null=True)
    CustomerBillingGroup = models.CharField(max_length=500, null=True)
    CSR = models.CharField(max_length=500, null=True)
    OrderDate = models.DateTimeField(null=True)
    ReadyTimeFrom = models.CharField(max_length=500, null=True)
    ReadyTimeTo = models.CharField(max_length=500, null=True)
    DueTimeFrom = models.CharField(max_length=500, null=True)
    DueTimeTo = models.CharField(max_length=500, null=True)
    Reference1 = models.CharField(max_length=500, null=True)
    Reference2 = models.CharField(max_length=500, null=True)
    OriginName = models.CharField(max_length=500, null=True)
    OriginAddress = models.CharField(max_length=500, null=True)
    OriginCity = models.CharField(max_length=500, null=True)
    OriginState = models.CharField(max_length=500, null=True)
    OriginZip = models.CharField(max_length=500, null=True)
    OriginPlus4 = models.CharField(max_length=500, null=True)
    OriginPhone = models.CharField(max_length=500, null=True)
    OriginComments = models.CharField(max_length=500, null=True)
    OriginValidated = models.CharField(max_length=500, null=True)
    DestName = models.CharField(max_length=500, null=True)
    DestAddress = models.CharField(max_length=500, null=True)
    DestCity = models.CharField(max_length=500, null=True)
    DestState = models.CharField(max_length=500, null=True)
    DestZip = models.CharField(max_length=500, null=True)
    DestPlus4 = models.CharField(max_length=500, null=True)
    DestPhone = models.CharField(max_length=500, null=True)
    DestComments = models.CharField(max_length=500, null=True)
    DestValidated = models.CharField(max_length=500, null=True)
    Pieces = models.CharField(max_length=500, null=True)
    ParcelType = models.CharField(max_length=500, null=True)
    ParcelLength = models.CharField(max_length=500, null=True)
    ParcelWidth = models.CharField(max_length=500, null=True)
    ParcelHeight = models.CharField(max_length=500, null=True)
    Weight = models.CharField(max_length=500, null=True)
    OrderType = models.CharField(max_length=500, null=True)
    SpecialInst = models.CharField(max_length=500, null=True)
    Distance = models.CharField(max_length=500, null=True)
    Route = models.CharField(max_length=500, null=True)
    RouteStop = models.CharField(max_length=500, null=True)
    IsParent = models.CharField(max_length=500, null=True)
    EmailPod = models.CharField(max_length=500, null=True)
    Workstation = models.CharField(max_length=500, null=True)
    ReadyToDay = models.CharField(max_length=500, null=True)
    DueFromDay = models.CharField(max_length=500, null=True)
    DueToDay = models.CharField(max_length=500, null=True)
    CreatedBy = models.CharField(max_length=500, null=True)
    CreatedWhen = models.CharField(max_length=500, null=True)
    UpdatedBy = models.CharField(max_length=500, null=True)
    UpdatedWhen = models.CharField(max_length=500, null=True)
    RateLockedBy = models.CharField(max_length=500, null=True)
    SettlementStatus = models.CharField(max_length=500, null=True)
    EmailPODChecked = models.CharField(max_length=500, null=True)
    EmailPOPChecked = models.CharField(max_length=500, null=True)
    EmailOrderConfirmationChecked = models.CharField(max_length=500, null=True)
    OriginLat = models.CharField(max_length=500, null=True)
    OriginLon = models.CharField(max_length=500, null=True)
    DestLat = models.CharField(max_length=500, null=True)
    DestLon = models.CharField(max_length=500, null=True)
    DriverPayLockedBy = models.CharField(max_length=500, null=True)
    DispatchFlag = models.CharField(max_length=500, null=True)
    BOL = models.CharField(max_length=500, null=True)
    MasterBOL = models.CharField(max_length=500, null=True)
    OrderCount = models.CharField(max_length=500, null=True)
    OriginCountry = models.CharField(max_length=500, null=True)
    DestCountry = models.CharField(max_length=500, null=True)
    OriginAddress2 = models.CharField(max_length=500, null=True)
    DestAddress2 = models.CharField(max_length=500, null=True)
    RequiredDriverInput = models.CharField(max_length=500, null=True)
    RequiredDriverInputTypeDescription = models.CharField(max_length=500, null=True)
    Signature = models.TextField(null=True)
    AssignedFleet = models.CharField(max_length=500, null=True)
    Barcode = models.CharField(max_length=500, null=True)
    Ordered = models.CharField(max_length=500, null=True)
    Dispatched = models.CharField(max_length=500, null=True)
    Confirmed = models.CharField(max_length=500, null=True)
    AtOrigin = models.CharField(max_length=500, null=True)
    ScannedAtPickup = models.CharField(max_length=500, null=True)
    PickedUp = models.DateTimeField(null=True)
    AtDestination = models.CharField(max_length=500, null=True)
    ScannedAtDelivery = models.CharField(max_length=500, null=True)
    Delivered = models.DateTimeField(null=True)
    Pod = models.CharField(max_length=500, null=True)
    PodComments = models.CharField(max_length=500, null=True)
    PaidDocument = models.CharField(max_length=500, null=True)
    CreatedBy = models.CharField(max_length=500, null=True)
    CreatedWhen = models.CharField(max_length=500, null=True)
    UpdatedBy = models.CharField(max_length=500, null=True)
    UpdatedWhen = models.CharField(max_length=500, null=True)
    DepotScan = models.CharField(max_length=500, null=True)
    LocalName = models.CharField(max_length=500, null=True)
    LocalAddress = models.CharField(max_length=500, null=True)
    LocalAddress2 = models.CharField(max_length=500, null=True)
    LocalCity = models.CharField(max_length=500, null=True)
    LocalState = models.CharField(max_length=500, null=True)
    LocalZip = models.CharField(max_length=500, null=True)
    LocalPlus4 = models.CharField(max_length=500, null=True)
    LocalPhone1 = models.CharField(max_length=500, null=True)
    LocalPhone2 = models.CharField(max_length=500, null=True)
    LocalEmail = models.CharField(max_length=500, null=True)
    LocalContact = models.CharField(max_length=500, null=True)
    ParcelPKID = models.CharField(max_length=500, null=True)
    ParcelPieces = models.CharField(max_length=500, null=True)
    ParcelWeight = models.CharField(max_length=500, null=True)
    ParcelReference = models.CharField(max_length=500, null=True)
    ParcelType = models.CharField(max_length=500, null=True)
    DriverPKID = models.CharField(max_length=500, null=True)
    DriverDriverID = models.CharField(max_length=500, null=True)
    DriverDriverPercent = models.CharField(max_length=500, null=True)
    DriverCreatedBy = models.CharField(max_length=500, null=True)
    DriverCreatedWhen = models.CharField(max_length=500, null=True)
    DriverUpdatedBy = models.CharField(max_length=500, null=True)
    DriverUpdatedWhen = models.CharField(max_length=500, null=True)
    DriverPayAmount = models.CharField(max_length=500, null=True)
    DriverFirstName = models.CharField(max_length=500, null=True)
    DriverLastName = models.CharField(max_length=500, null=True)
    DriverVehicleDescription = models.CharField(max_length=500, null=True)
    DriverVehicleLicensePlate = models.CharField(max_length=500, null=True)
    DriverVehicleLicenseState = models.CharField(max_length=500, null=True)
    DriverFleet = models.CharField(max_length=500, null=True)
    DriverLastReportLat = models.CharField(max_length=500, null=True)
    DriverLastReportLon = models.CharField(max_length=500, null=True)
    DriverLastReportTime = models.CharField(max_length=500, null=True)
    imageid = models.CharField(max_length=500, null=True)

    def __str__(self):
        return str(self.Reference1)

class QuoteAccount(models.Model):
    company = models.CharField(max_length=500, null=True)
    email =  models.CharField(max_length=500, null=True)
    contact = models.CharField(max_length=500, null=True)    
    phone = PhoneNumberField(blank=True)
    address = AddressField(null=True)

    def __str__(self):
        return str(self.company) + ", " +  str(self.email)

class Quote(models.Model):
    created = models.DateTimeField(default=timezone.now) #Time quote was created at
    responded = models.DateTimeField(null=True, blank=True) #Time quote was responded to 
    expires = models.DateTimeField(null=True, blank=True) #Time quote expires
    account = models.ForeignKey(QuoteAccount, on_delete=models.CASCADE, null=True) #Foreignkey to quote account
    dedicated = models.BooleanField(default=False) #Whether or not the load is dedicated or not
    hempinsurance = models.IntegerField(null=True, blank=True) #The value of the load IF hemp is included
    service = models.CharField(max_length=500, null=True) #The service of the load (Sprinter Van, Cargo Truck, etc.)
    commodity = models.CharField(max_length=500, null=True) #The commodity being shipped
    weight = models.CharField(max_length=500, null=True) #The weight of the shipment
    dimensions = models.CharField(max_length=500, null=True) #The dimensions of the shipment
    quantity = models.CharField(max_length=500, null=True) #The quantity of the shipment
    pieces = models.CharField(max_length=500, null=True) #The number of pieces in the load
    pickup = AddressField(related_name='Pickup Address+', blank=True, null=True) #The pickup address of the load
    dropoff = AddressField(related_name='Dropoff Address+', blank=True, null=True) #The dropoff address of the load
    traveltime = models.CharField(max_length=500, null=True) #The Travel time of the load
    cost = models.IntegerField(null=True) #The cost of the load
    ccemails = models.TextField(null=True, blank=True) #Emails to send the quote to
    notes = models.TextField(null=True, blank=True) #Notes on the load
    livequote = models.BooleanField(default=True) #Whether or not the load is live
    accepted = models.BooleanField(null=True) #If the quote was accepted or not
    
    def save(self, *args, **kwargs):
        # Set the expires field only if it's not already set
        if not self.expires:
            self.expires = timezone.now() + timezone.timedelta(days=1)
    
        super(Quote, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.account) + ", $" + str(self.cost)

class RejectedQuote(models.Model):
    quote = models.OneToOneField(Quote, on_delete=models.CASCADE, null=True)
    reason = models.TextField(null=True, verbose_name= _('To enhance our service to you and others, could you please provide us with feedback or suggest any modifications to your quote?'))

    def __str__(self):
        return str(self.quote)
    
class LabelGroup(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, null=True, blank=True,)
    from_address = AddressField(related_name='Group Label Pickup Address+', blank=True, null=True)
    expected_delivery_date = models.DateField(blank=True,)
    csv = models.FileField(upload_to='labelcsvs/', null=True, blank=True,)
    ref1col = models.CharField(max_length=1, null=True, blank=True,)
    ref2col = models.CharField(max_length=1, null=True, blank=True,)
    ref3col = models.CharField(max_length=1, null=True, blank=True,)
    address1col = models.CharField(max_length=1, null=True, blank=True,)
    address2col = models.CharField(max_length=1, null=True, blank=True,)
    citycol = models.CharField(max_length=1, null=True, blank=True,)
    statecol = models.CharField(max_length=1, null=True, blank=True,)
    zipcol = models.CharField(max_length=1, null=True, blank=True,)
    istrcol = models.CharField(max_length=1, null=True, blank=True,)
    namecol = models.CharField(max_length=1, null=True, blank=True,)
    tangelogroupcol = models.CharField(max_length=1, null=True, blank=True,)
    tangelonumberscol = models.CharField(max_length=1, null=True, blank=True,)


    def __str__(self):
        return str(self.user) + " " + str(self.expected_delivery_date)

    
class Label(models.Model):
    group = models.ForeignKey(LabelGroup, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=500, null=True)
    from_address = AddressField(related_name='Label Pickup Address+', blank=True, null=True)
    address1 = models.CharField(max_length=500, null=True)
    address2 = models.CharField(max_length=500, null=True)
    city = models.CharField(max_length=500, null=True)
    state = models.CharField(max_length=500, null=True)
    zip = models.CharField(max_length=500, null=True)
    expected_delivery_date = models.DateField()
    ref1 = models.CharField(max_length=500, null=True)
    ref2 = models.CharField(max_length=500, null=True)
    ref3 = models.CharField(max_length=500, null=True)
    instr = models.CharField(max_length=250, null=True)
    tangelogroup = models.CharField(max_length=500, null=True)
    tangelonumbers = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return str(self.group) + " " + str(self.expected_delivery_date)



# class Carrier(models.Model):
#     company = models.CharField(max_length=500, null=True)
#     email =  models.EmailField()
#     contact = models.CharField(max_length=500, null=True)    
#     phone = PhoneNumberField(blank=True)
#     fax = PhoneNumberField(blank=True)
#     address = AddressField(null=True)
#     mcnumber = models.IntegerField(null=True)
#     usdotnumber = models.IntegerField(null=True)
#     feidnumber = models.IntegerField(null=True)
#     hazmat = models.BooleanField(null=True)
#     hazmatnumber = models.IntegerField(null=True)
#     smartway = models.BooleanField(null=True)
#     techprovider = models.CharField(max_length=500, null=True)

#     ltl = models.BooleanField(null=True)
#     ftl = models.BooleanField(null=True)
#     lastmile = models.BooleanField(null=True)
#     middlemile = models.BooleanField(null=True)
#     transloading = models.BooleanField(null=True)
#     airfreight = models.BooleanField(null=True)
#     flatbeds = models.BooleanField(null=True)
#     otr = models.BooleanField(null=True)
#     refrigerated = models.BooleanField(null=True)
#     hotshots = models.BooleanField(null=True)
#     localpickupanddelivery = models.BooleanField(null=True)
#     expedited = models.BooleanField(null=True)
#     highvalue = models.BooleanField(null=True)
#     drayage = models.BooleanField(null=True)

#     sprinterqty = models.IntegerField(null=True)
#     straughttruckqty = models.IntegerField(null=True)
#     dryvanqty = models.IntegerField(null=True)
#     reeferqty = models.IntegerField(null=True)
#     flatbedqty = models.IntegerField(null=True)
#     warehousesqft = models.IntegerField(null=True)

#     usservice = models.TextField(null=True)
#     canservice = models.TextField(null=True)
#     mexservice = models.TextField(null=True)

#     #certexpiration = models.DateTimeField(null=True, blank=True)

#     w9 = models.FileField(upload_to ='carriers/')
#     insurance = models.FileField(upload_to ='carriers/')
#     operatingauth = models.FileField(upload_to ='carriers/')
#     carrierbroker = models.CharField(max_length=500, null=True)
#     manualbrokercarrier = models.FileField(upload_to ='carriers/', null=True) 


#     sign_page_url = models.CharField(max_length=255, null=True, blank=True)
#     contractsigned = models.BooleanField(default=False)


#     def __str__(self):
#         return str(self.company) + ' ' + str(self.id)
    
class CarrierGroup(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
# class Shipper(models.Model):
#     company = models.CharField(max_length=500, null=True, blank=True, verbose_name='Company')
#     contact = models.CharField(max_length=500, null=True, blank=True, verbose_name='Contact Name')
#     address = AddressField(null=True, blank=True, verbose_name='Company Address')
#     ein = models.IntegerField(blank=True, null=True)


# class ShipperAccounting(models.Model):
#     shipper = models.ForeignKey(Shipper)
#     creditlimit = models.IntegerField(blank=True, null=True)
#     contact = models.CharField(max_length=500, null=True, blank=True, verbose_name='Accounting Contact Name')
#     contactphone = PhoneNumberField(null = True, blank=True, verbose_name='Accounting Phone Number')
#     contactemail = models.EmailField(verbose_name='Accounting Email', null=True, blank=True)

class Carrier(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    company = models.CharField(max_length=500, null=True, blank=True, verbose_name='Company')
    scac = models.CharField(max_length=500, null=True, blank=True, verbose_name='Scac')
    email = models.EmailField(verbose_name='Email')
    contact = models.CharField(max_length=500, null=True, blank=True, verbose_name='Contact Name')
    address = AddressField(null=True, blank=True, verbose_name='Company Address')
    mainphone = PhoneNumberField(blank=True, verbose_name='Main Phone Number')
    mobilephone = PhoneNumberField(blank=True, verbose_name='Mobile Phone Number')
    fax = PhoneNumberField(blank=True, verbose_name='Fax')

    mcnumber = models.IntegerField(blank=True, null=True)
    usdotnumber = models.CharField(max_length= 500, blank=True, null=True)
    feinnumber = models.CharField(max_length= 500, blank=True, null=True)
    techprovider = models.CharField(max_length=500, null=True, blank=True, verbose_name='Tech Provider')
    trackingtech = models.CharField(max_length=500, null=True, blank=True, verbose_name='Tracking Technology')

    ownername = models.CharField(max_length=500, null=True, blank=True, verbose_name='Owner Name')
    ownerphone = PhoneNumberField(blank=True, null=True, verbose_name='Owner Phone Number')
    owneremail = models.EmailField(blank=True, null=True,  verbose_name='Owner Email')

    dispatchname = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dispatch Name')
    dispatchphone = PhoneNumberField(blank=True, null=True, verbose_name='Dispatch Phone Number')
    dispatchemail = models.EmailField(blank=True, null=True,  verbose_name='Dispatch Email')

    accountingname = models.CharField(max_length=500, null=True, blank=True, verbose_name='Accounting Name')
    accountingphone = PhoneNumberField(blank=True, null=True, verbose_name='Accounting Phone Number')
    accountingemail = models.EmailField(blank=True, null=True,  verbose_name='Accounting Email')

    hazmat = models.BooleanField(null=True, blank=True, verbose_name='Hazmat')
    smartway = models.BooleanField(null=True, blank=True, verbose_name='Smartway')
    ltl = models.BooleanField(null=True, blank=True, verbose_name='Less than Load')
    ftl = models.BooleanField(null=True, blank=True, verbose_name='Full Truckload')
    b2b = models.BooleanField(null=True, blank=True, verbose_name='B2B')
    tsa = models.BooleanField(null=True, blank=True, verbose_name='TSA')
    lastmile = models.BooleanField(null=True, blank=True, verbose_name='Last Mile')
    middlemile = models.BooleanField(null=True, blank=True, verbose_name='Middle Mile')
    transloading = models.BooleanField(null=True, blank=True, verbose_name='Transloading')
    airfreight = models.BooleanField(null=True, blank=True, verbose_name='Air Freight')
    liftgates = models.BooleanField(null=True, blank=True, verbose_name='Lift Gates')
    flatbeds = models.BooleanField(null=True, blank=True, verbose_name='Flat Beds')
    otr = models.BooleanField(null=True, blank=True, verbose_name='Over The Road')
    refrigerated = models.BooleanField(null=True, blank=True, verbose_name='Refrigerated')
    hotshots = models.BooleanField(null=True, blank=True, verbose_name='Hot Shots')
    localpickupanddelivery = models.BooleanField(null=True, blank=True, verbose_name='Local Pick up and Delivery')
    expedited = models.BooleanField(null=True, blank=True, verbose_name='Expedited')
    highvalue = models.BooleanField(null=True, blank=True, verbose_name='High Value')
    drayage = models.BooleanField(null=True, blank=True, verbose_name='Drayage')
    whiteglove = models.BooleanField(null=True, blank=True, verbose_name='White Glove')
    residential = models.BooleanField(null=True, blank=True, verbose_name='Residential')
    insidedelivery = models.BooleanField(null=True, blank=True, verbose_name='Inside Delivery')
    medical = models.BooleanField(null=True, blank=True, verbose_name='Medical')
    hemp = models.BooleanField(null=True, blank=True, verbose_name='Hemp')
    airport = models.BooleanField(null=True, blank=True, verbose_name='Airport Recovery')


    lastmileqty = models.IntegerField(null=True, blank=True, verbose_name='Last Mile Quantity')
    tsaqty = models.IntegerField(null=True, blank=True, verbose_name='TSA Mile Quantity')
    automobileqty = models.IntegerField(null=True, blank=True, verbose_name='Automobile Quantity')
    highcubedqty = models.IntegerField(null=True, blank=True, verbose_name='High Cubed Quantity')
    sprinterqty = models.IntegerField(null=True, blank=True, verbose_name='Sprinter Van Quantity')
    straughttruckqty = models.IntegerField(null=True, blank=True, verbose_name='Straight Truck Quantity')
    dryvanqty = models.IntegerField(null=True, blank=True, verbose_name='Dry Van Quantity')
    reeferqty = models.IntegerField(null=True, blank=True, verbose_name='Refrigerated Trailer Quantity')
    flatbedqty = models.IntegerField(null=True, blank=True, verbose_name='Flat Bed Quantity')
    warehousesqft = models.IntegerField(null=True, blank=True, verbose_name='Warehouse Square Feet')
    totaltruckqty = models.IntegerField(null=True, blank=True, verbose_name='Total Truck Quantity')
    is_totaltruckqty_auto = models.BooleanField(default=True, verbose_name='Is Total Truck Quantity Auto Calculated?')


    inductionfacilityloc1 = AddressField(null=True, blank=True, related_name='inductionlocation1', verbose_name='Induction Facility 1')
    inductionfacilityloc1_temp_controlled = models.BooleanField(default=False, verbose_name='Induction Facility Location 1 Temperature Controlled')

    inductionfacilityloc2 = AddressField(null=True, blank=True, related_name='inductionlocation2', verbose_name='Induction Facility 2')
    inductionfacilityloc2_temp_controlled = models.BooleanField(default=False, verbose_name='Induction Facility Location 2 Temperature Controlled')

    inductionfacilityloc3 = AddressField(null=True, blank=True, related_name='inductionlocation3', verbose_name='Induction Facility 3')
    inductionfacilityloc3_temp_controlled = models.BooleanField(default=False, verbose_name='Induction Facility Location 3 Temperature Controlled')

    inductionfacilityloc4 = AddressField(null=True, blank=True, related_name='inductionlocation4', verbose_name='Induction Facility 4')
    inductionfacilityloc4_temp_controlled = models.BooleanField(default=False, verbose_name='Induction Facility Location 4 Temperature Controlled')

    inductionfacilityloc5 = AddressField(null=True, blank=True, related_name='inductionlocation5', verbose_name='Induction Facility 5')
    inductionfacilityloc5_temp_controlled = models.BooleanField(default=False, verbose_name='Induction Facility Location 5 Temperature Controlled')

    coverageradius = models.IntegerField(null=True, blank=True, verbose_name='Coverage Radius')

    usservice = models.TextField(null=True, blank=True, help_text="Please let your value be in single quote closed with []. sample ['AB', 'DC']" ,verbose_name='Domestic Service')
    canservice = models.TextField(null=True, blank=True, help_text="Please let your value be in single quote closed with []. sample ['AB', 'DC']" ,verbose_name='Canada Service')
    mexservice = models.TextField(null=True, blank=True, help_text="Please let your value be in single quote closed with []. sample ['AB', 'DC']" ,verbose_name='Mexico Service')

    w9 = models.FileField(upload_to='carriers/', null=True, blank=True, verbose_name='W-9')
    insurance = models.FileField(upload_to='carriers/', null=True, blank=True, verbose_name='Insurance Agreement')
    operatingauth = models.FileField(upload_to='carriers/', null=True, blank=True, verbose_name='Operating Authority')
    zipcoverage = models.FileField(upload_to='carriers/', null=True, blank=True, verbose_name='Zip Code Coverage Area')
    carrierbroker = models.CharField(max_length=500, null=True, blank=True, verbose_name='Carrier Broker')
    manualcarrierbroker = models.FileField(upload_to='carriers/', null=True, blank=True, verbose_name='Manual Carrier Broker')

    insuranceexp = models.DateField(null=True, blank=True, verbose_name='Insurance Experiation Date')

    group = models.ManyToManyField(CarrierGroup, blank=True)

    courier = models.BooleanField(default=False, verbose_name='Check for Courier')

    # sign_page_url = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Signed Page Url')
    contractsigned = models.BooleanField(default=False, verbose_name='Contract Signed')
    # skip_signal = models.BooleanField(default=False)
    update = models.BooleanField(default = False)

    notes = models.TextField(null=True, blank=True)

    onboarded = models.BooleanField(default=False, verbose_name='Onboarded')
    is_onboarded_auto = models.BooleanField(default=True, verbose_name='Is onboarded auto?')
    
    def missing_fields(self):
        fields = [
            ("w9", self.w9),
            ("contractsigned", self.contractsigned),
            ("insurance", self.insurance),
            ("operatingauth", self.operatingauth),
            ("mcnumber", self.mcnumber),
            ("usdotnumber", self.usdotnumber),
            ("accountingname", self.accountingname),
            ("accountingemail", self.accountingemail)
        ]
        
        missing = [field[0] for field in fields if not field[1]]
        return ", ".join(missing)

    def save(self, *args, **kwargs):
        if self.is_totaltruckqty_auto:
            self.totaltruckqty = (
                (self.flatbedqty or 0) + 
                (self.straughttruckqty or 0) + 
                (self.automobileqty or 0) + 
                (self.sprinterqty or 0) + 
                (self.reeferqty or 0) + 
                (self.dryvanqty or 0)
            )
        else:
            pass

        if self.is_onboarded_auto:
            if self.w9 and self.insurance and self.operatingauth and self.mcnumber and self.usdotnumber and self.accountingname and self.accountingemail:
                self.onboarded = True
        else:
            pass
        super(Carrier, self).save(*args, **kwargs)



    def __str__(self):
        return str(self.company) + ' ' + str(self.id)
    

class PricingProposalFile(models.Model):
    your_model = models.ForeignKey(Carrier, related_name='pricing_proposals', on_delete=models.CASCADE)
    file = models.FileField(upload_to='pricing_proposals/')
    # Any other fields you need, like an upload date, filename, etc.

class PricingAgreementFile(models.Model):
    your_model = models.ForeignKey(Carrier, related_name='pricing_agreements', on_delete=models.CASCADE)
    file = models.FileField(upload_to='pricing_agreements/')


class Auction(models.Model):
    carriers = models.ManyToManyField(Carrier, related_name='auctions')
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.quote) + ' ' + str(self.created_at)

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, related_name='bids', null=True)
    price = models.IntegerField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.carrier) + ' ' + str(self.price)
    
class UDSOrder(models.Model):
    externalid = models.CharField(max_length=500, null=True)
    date = models.DateField(null=True)

    def __str__(self):
        return str(self.externalid) + ' ' + str(self.date)

class SupportMessage(models.Model):
    sender = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    attachment = models.FileField(upload_to='support_messages/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.email} - {self.subject}"


@receiver(post_save, sender=Quote)
def create_order(sender, instance=None, created=False, **kwargs):
    if created:
        context = {}
        context['company'] = instance.account.company
        context['contact'] = instance.account.contact
        context['service'] = instance.service
        context['commodity'] = instance.commodity
        context['weight'] = instance.weight
        context['dimensions'] = instance.dimensions
        context['quantity'] = instance.quantity
        context['pickup'] = instance.pickup
        context['dropoff'] = instance.dropoff
        context['traveltime'] = instance.traveltime
        context['cost'] = instance.cost

        link = 'https://portal.357company.com/quote/' + str(instance.id) + '/'

        context['link'] = link

        outemails = instance.ccemails.split(', ')
        outemails = [instance.account.email] + outemails


        send_mail(
            f"Hey {instance.account.company}! Your quote from The 357 Company is here! - Quote #357{instance.id}",
            render_to_string('quoteemail.txt', context),
            'info@357company.com',
            outemails,
            fail_silently=False
        ) 
        
#Connect the signal to the receiver
post_save.connect(create_order, sender=Quote)




# @receiver(post_save, sender=Carrier)
# def send_agreement(sender, instance=None, created=False, **kwargs):
#     if not instance.skip_signal and not instance.update:
#         datenumber = datetime.today().strftime('%d')
#         dateyear = datetime.today().strftime('%Y')
#         dateyear = dateyear[2:]
#         date = datetime.today().strftime('%Y-%m-%d')

#         url = 'https://esignatures.io/api/contracts'
#         token = 'd6f3eb1f-4596-4c3f-8141-606fada04c93'
#         headers = {'Content-Type': 'application/json'}
#         data = {
#             'template_id': '275adeb5-6a2b-408c-b1cf-ba8424c0126f',
#             'signature_request_delivery_method': 'embedded',
#             'signers': [
#                 {
#                     'name': str(instance.contact),
#                     'email': str(instance.email),
#                     "mobile": str(instance.mobilephone),
#                     "company_name": str(instance.company),
#                     "required_identification_methods": ["email"],
#                     "redirect_url": "https://portal.357company.com/carriers?success=true",
#                 }
#             ],
#               "placeholder_fields": [
#                 {
#                     "api_key": "datenumber",
#                     "value": datenumber
#                 },
#                 {
#                     "api_key": "yearnumber",
#                     "value": dateyear
#                 },
#                 {
#                     "api_key": "carrier",
#                     "value": str(instance.company)
#                 },
#                 {
#                     "api_key": "mcdot",
#                     "value": str(instance.mcnumber)
#                 },
#                 {
#                     "api_key": "date",
#                     "value": date
#                 },
#                 {
#                     "api_key": "carrieraddress",
#                     "value": str(instance.address)
#                 },

#             ],
#         }

#         response = requests.post(url=url, headers=headers, params={'token': token}, json=data)

#         if response.status_code == 200:
#             response_json = response.json()

#             sign_page_url = response_json['data']['contract']['signers'][0]['sign_page_url']
#             docid = response_json['data']['contract']['id']

#             instance.sign_page_url = sign_page_url
#             instance.carrierbroker = docid
#             instance.update = True
#             instance.save()

#             email_body = """
#             Welcome to The 357 Company Partner Network!

#             Required paperwork for payment:
#             Email invoices to accounting@357company.com

#             Please include the following:

#             1. Original Bill of Lading
#             2. A Signed Proof of Delivery on the Bill of Lading
#             3. Your invoice, please reference our Rate Confirmation Number that starts with 357M...(please note: if the rate confirmation number is not referenced on your invoice, it will not be submitted for payment.)
#             4. If requested, please provide pictures of the freight before pickup and at delivery.

#             Special Acknowledgements:
#             Any Double Broker loads will result in a review on Carrier 411 and a reduction in the fee.

#             Payment Information:
#             Payment within (30) days or less after receipt of required paperwork.

#             Quick Pay option available once the required paperwork and POD referenced above are received. Payment will be discounted by 3% of the total agreed amount.
#             """



#             send_mail(
#                 'Thanks for joining our Partner Network!',
#                 email_body,
#                 'info@357company.com',
#                 [str(instance.email)],
#                 fail_silently=False
#             )

#             send_mail(
#                 "A new partner carrier completed onboarding ",
#                 f"{instance.contact} from {instance.company} signed up.",
#                 'info@357company.com',
#                 ['jp@357company.com'],
#                 fail_silently=False
#             )



#         else:
#             print('Error:', response.text)





        

# #Connect the signal to the receiver
# post_save.connect(send_agreement, sender=Carrier)

