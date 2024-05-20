from django import forms
from django.contrib.auth.forms import UserCreationForm
from importlib_metadata import email
from .models import *
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.forms import TextInput, Textarea
from address.forms import AddressField, AddressWidget
from address.models import Address
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from multiselectfield.forms.fields import MultiSelectFormField




class UDSCreate(forms.Form):
    csv = forms.FileField()

    class Meta: 
        fields = '__all__'

class QuoteCreate(forms.ModelForm):
    class Meta:
        model = Quote
        pickup = AddressField()
        dropoff = AddressField()
        fields = '__all__'

class AuctionCompleteForm(forms.Form):
    complete = forms.BooleanField(required=False)



class BidAcceptForm(forms.Form):
    accept = forms.BooleanField(label='Accept Bid')

    class Meta:
        model = Bid
        fields = ['accept']

class SupportRequestForm(forms.ModelForm):
    subject = forms.CharField(max_length=200, label="Subject")
    message = forms.CharField(widget=forms.Textarea, label="Message")
    attachment = forms.FileField(required=False, label="Attachment")

    class Meta:
        model = SupportMessage
        fields = ['subject', 'message', 'attachment']


class AuctionCreateForm(forms.ModelForm):
    # Define the quote field with a custom queryset
    quote = forms.ModelChoiceField(
        queryset=Quote.objects.exclude(accepted=False).order_by('-created'),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Select a quote'
    )

    class Meta:
        model = Auction
        fields = ['quote']


class LabelGroupForm(forms.ModelForm):
   user = forms.ModelChoiceField(queryset=NewUser.objects.all())
   from_address = AddressField(required=False, widget=AddressWidget(attrs={'class' : 'text-lg h-10 w-full bg-gray-100 text-black my-2 inline rounded-xl transition ease-in-out px-3'}))
   expected_delivery_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
   csv = forms.FileField()
   ref1col = forms.CharField(label='Reference 1 Column (A-Z)')
   ref2col = forms.CharField(required=False, label='Reference 2 Column (A-Z)')
   ref3col = forms.CharField(required=False, label='Reference 3 Column (A-Z)')
   address1col = forms.CharField(label='Address 1 Column (A-Z)')
   address2col = forms.CharField(label='Address 2 Column (A-Z)')
   citycol = forms.CharField(label='City Column (A-Z)')
   statecol = forms.CharField(label='State Column (A-Z)')
   zipcol = forms.CharField(label='Zip Column (A-Z)')
   namecol = forms.CharField(label='Name Column (A-Z)')
   istrcol = forms.CharField(label='Instruction Column (A-Z)')
   tangelogroupcol = forms.CharField(required=False, label='Tangelo Group')
   tangelonumberscol = forms.CharField(required=False, label='Tangelo Numbers')

   class Meta: 
    model = LabelGroup
    fields = '__all__'


class Registration(UserCreationForm):

  email = forms.EmailField(label="Your Company Email", max_length=60, widget=forms.TextInput(attrs={'class':'sm:text-xl h-7 my-3 text-black transition ease-in-out w-full bg-gray-100', 'placeholder': 'example@company.com'}))
  name = forms.CharField(label="Your Company Name", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 h-7  text-black transition ease-in-out w-full bg-gray-100'}))
  company_name = forms.CharField(label="Your Company Name", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 h-7  text-black transition ease-in-out w-full bg-gray-100'}))
  orders = forms.CharField(label="How many orders do you chip per month?", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 h-7  text-black transition ease-in-out w-full bg-gray-100'}))
  position = forms.CharField(label="Your Role", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3  h-7 text-black transition ease-in-out w-full bg-gray-100'}))
  company_phone = PhoneNumberField(required=False, widget=PhoneNumberPrefixWidget(initial='US', attrs={'class':'text-lg h-7 w-full bg-gray-100 text-black my-2 inline  transition ease-in-out px-3', 'placeholder': '1234567890'}))
  company_address = AddressField(widget=AddressWidget(attrs={'class' : 'text-lg h-10 w-full bg-gray-100 text-black my-2 h-7 inline  transition ease-in-out px-3'}))
  password1 = forms.CharField(label= 'Password', widget=forms.PasswordInput(attrs={'class':'sm:text-xl my-3  h-7 text-black transition ease-in-out w-full bg-gray-100'}))
  password2 = forms.CharField(label= 'Password Confirmation', widget=forms.PasswordInput(attrs={'class':'sm:text-xl my-3 h-7  text-black transition ease-in-out w-full bg-gray-100'}))



  def __init__(self, *args, **kwargs):
        super(Registration, self).__init__(*args, **kwargs)

        for fieldname in ['email','password1', 'password2']:
            self.fields[fieldname].help_text = None

  class Meta: 
    model = NewUser
    fields = ['email', 'company_name', 'position', 'company_phone', 'company_address', 'password1', 'password2']
    
    
    
class GeneratedReportForm(forms.ModelForm):
    deliverystatus = MultiSelectFormField(max_choices=6, min_choices=1, max_length=80, choices=DELIVERY_STATUS_CHOICES)
    class Meta:
        model = GeneratedReport
        fields = ['report_type','deliverystatus', 'schedule']
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Report Description'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Report Subject'})
        }
        
    def __init__(self, *args, **kwargs):
        super(GeneratedReportForm, self).__init__(*args, **kwargs)
        self.fields['deliverystatus'].required = False
        self.fields['schedule'].required = False
    
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('deliverystatus', css_class ='grid md:grid-cols-2 grid-cols-1'),
                css_class = 'grid'
            ),
        )
    

    # def clean_emailList(self):
    #     emails = self.cleaned_data.get('email')
    #     email_list = [email.strip() for email in emails.split(',') if email.strip()]
        
    #     # Here, add any necessary email validation
    #     return ','.join(email_list)

class ReportFilterForm(forms.ModelForm):
    deliverystatus = MultiSelectFormField(max_choices=6, min_choices=1, max_length=80, choices=DELIVERY_STATUS_CHOICES)
    class Meta:
        model = ReportFilter
        fields = ['start_date', 'end_date', 'customercity', 'customerstate', 'deliverystatus', 'address', "customername"]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'customercity': forms.TextInput(attrs={'placeholder': 'Customer City'}),
            'customerstate': forms.TextInput(attrs={'placeholder': 'Customer State'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address'}),
            'customername': forms.TextInput(attrs={'placeholder': 'Customer Name'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(ReportFilterForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].required = False
        self.fields['end_date'].required = False
        self.fields['customercity'].required = False
        self.fields['customerstate'].required = False
        self.fields['deliverystatus'].required = False
        self.fields['address'].required = False
        self.fields['customername'].required = False

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('deliverystatus', css_class ='grid md:grid-cols-2 grid-cols-1'),
                css_class = 'grid'
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("The end date must be after the start date.")
        return cleaned_data


class TemplatedFiltersForm(forms.ModelForm):
    deliverystatus = MultiSelectFormField(max_choices=6, min_choices=1, max_length=80, choices=DELIVERY_STATUS_CHOICES)
    class Meta:
        model = TemplatedFilters
        fields = ['start_date', 'end_date', 'customercity', 'customerstate', 'deliverystatus', 'address', "customername"]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'customercity': forms.TextInput(attrs={'placeholder': 'Customer City'}),
            'customerstate': forms.TextInput(attrs={'placeholder': 'Customer State'}),
            'customerstate': forms.TextInput(attrs={'placeholder': 'Address'}),
            'customername': forms.TextInput(attrs={'placeholder': 'Customer Name'})
        }
        
    def __init__(self, *args, **kwargs):
        super(TemplatedFiltersForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].required = False
        self.fields['end_date'].required = False
        self.fields['customercity'].required = False
        self.fields['customerstate'].required = False
        self.fields['deliverystatus'].required = False
        self.fields['address'].required = False
        self.fields['customername'].required = False
    
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('deliverystatus', css_class ='grid md:grid-cols-2 grid-cols-1'),
                css_class = 'grid'
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("The end date must be after the start date.")
        
        # check if none of the fields are filled
        if not any(cleaned_data.values()):
            raise forms.ValidationError("At least one filter must be filled out.")
        
        return cleaned_data

class CarrierForm(forms.ModelForm):

    STATES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
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
    ('WY', 'Wyoming'),
    )

    PROVINCES = (
    ('AB', 'Alberta'),
    ('BC', 'British Columbia'),
    ('MB', 'Manitoba'),
    ('NB', 'New Brunswick'),
    ('NL', 'Newfoundland / Labrador'),
    ('NS', 'Nova Scotia'),
    ('ON', 'Ontario'),
    ('PE', 'Prince Edward Island'),
    ('QC', 'Quebec'),
    ('SK', 'Saskatchewan'),
    ('NT', 'Northwest Territories'),
    ('NU', 'Nunavut'),
    ('YT', 'Yukon'),
    )

    MEXSTATES = (
    ('AG', 'Aguascalientes'),
    ('BC', 'Baja California'),
    ('BS', 'Baja California Sur'),
    ('CM', 'Campeche'),
    ('CS', 'Chiapas'),
    ('CH', 'Chihuahua'),
    ('CO', 'Coahuila'),
    ('CL', 'Colima'),
    ('DF', 'Federal District'),
    ('DG', 'Durango'),
    ('GT', 'Guanajuato'),
    ('GR', 'Guerrero'),
    ('HG', 'Hidalgo'),
    ('JA', 'Jalisco'),
    ('MX', 'Mexico State'),
    ('MI', 'Michoacán'),
    ('MO', 'Morelos'),
    ('NA', 'Nayarit'),
    ('NL', 'Nuevo León'),
    ('OA', 'Oaxaca'),
    ('PU', 'Puebla'),
    ('QT', 'Querétaro'),
    ('QR', 'Quintana Roo'),
    ('SL', 'San Luis Potosí'),
    ('SI', 'Sinaloa'),
    ('SO', 'Sonora'),
    ('TB', 'Tabasco'),
    ('TM', 'Tamaulipas'),
    ('TL', 'Tlaxcala'),
    ('VE', 'Veracruz'),
    ('YU', 'Yucatán'),
    ('ZA', 'Zacatecas'),
    )

    email = forms.EmailField(
        label="Your Company Email", 
        max_length=60, 
        widget=forms.TextInput(attrs={
            'class':'text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100', 
            'placeholder': 'example@company.com', 
            'x-ref': 'company_email'
        })
    )
    company = forms.CharField(
        label="Your Company Name", 
        widget=forms.TextInput(attrs={
            'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100', 
            'x-ref': 'company_name'
        })
    )
    address = AddressField(
        widget=AddressWidget(attrs={
            'class' : 'text-lg h-10 w-full bg-gray-100 text-black my-2 inline rounded-xl transition ease-in-out px-3', 
            'x-ref': 'address'
        })
    )
    contact = forms.CharField(
        label="Your Name", 
        widget=forms.TextInput(attrs={
            'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100', 
            'x-ref': 'your_name'
        })
    )

    mainphone = PhoneNumberField(required=False, widget=PhoneNumberPrefixWidget(initial='US', attrs={'class':'text-lg h-12 w-full bg-gray-100 text-black mb-0 mt-3 inline rounded-xl transition ease-in-out px-3', 'placeholder': '1234567890'}))
    mobilephone = PhoneNumberField(required=False, widget=PhoneNumberPrefixWidget(initial='US', attrs={'class':'text-lg h-12 w-full bg-gray-100 text-black mb-0 mt-3 inline rounded-xl transition ease-in-out px-3', 'placeholder': '1234567890'}))

    fax = PhoneNumberField(required=False, widget=PhoneNumberPrefixWidget(initial='US', attrs={'class':'text-lg h-12 w-full bg-gray-100 text-black mt-3 mb-0 inline rounded-xl transition ease-in-out px-3', 'placeholder': '1234567890'}))

    scac = forms.CharField(required=False, label="SCAC", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    mcnumber = forms.CharField(required=False, label="MC Number", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    usdotnumber = forms.CharField(required=False, label="US DOT #", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    feinnumber = forms.CharField(required=False, label="FEIN Number", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    hazmat = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    hazmatnumber = forms.IntegerField(required=False, label="HAZMAT #", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    smartway = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    techprovider = forms.CharField(required=False, label="Technology Provider", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    trackingtech = forms.CharField(required=False, label="Tracking Tech", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))


    ownername = forms.CharField(required=False, label="Owner Name", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    ownerphone = PhoneNumberField(required=False, widget=PhoneNumberPrefixWidget(initial='US', attrs={'class':'text-lg h-12 w-full bg-gray-100 text-black mb-0 mt-3 inline rounded-xl transition ease-in-out px-3', 'placeholder': '1234567890'}))
    owneremail = forms.EmailField(required=False,label="Owner Email", max_length=60, widget=forms.TextInput(attrs={'class':'text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100', 'placeholder': 'example@company.com'}))

    dispatchname = forms.CharField(required=False, label="Dispatch Name", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    dispatchphone = PhoneNumberField(required=False, widget=PhoneNumberPrefixWidget(initial='US', attrs={'class':'text-lg h-12 w-full bg-gray-100 text-black mb-0 mt-3 inline rounded-xl transition ease-in-out px-3', 'placeholder': '1234567890'}))
    dispatchemail = forms.EmailField(required=False, label="Dispatch Email", max_length=60, widget=forms.TextInput(attrs={'class':'text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100', 'placeholder': 'example@company.com'}))

    accountingname = forms.CharField(required=False, label="Accounting Name", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    accountingphone = PhoneNumberField(required=False, widget=PhoneNumberPrefixWidget(initial='US', attrs={'class':'text-lg h-12 w-full bg-gray-100 text-black mb-0 mt-3 inline rounded-xl transition ease-in-out px-3', 'placeholder': '1234567890'}))
    accountingemail = forms.EmailField(required=False, label="Accounting Email", max_length=60, widget=forms.TextInput(attrs={'class':'text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100', 'placeholder': 'example@company.com'}))


    ltl = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    ftl = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    lastmile = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    liftgates = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    middlemile = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    transloading = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    airfreight = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    flatbeds = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    otr = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    refrigerated = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    hotshots = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    localpickupanddelivery = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    expedited = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    highvalue = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    drayage = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    whiteglove = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    residential = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    insidedelivery = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    b2b = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    tsa = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    hemp = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    medical = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))
    airport = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))




    lastmileqty = forms.IntegerField(required=False, label="Last Mile Quantity", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    tsaqty = forms.IntegerField(required=False, label="TSA Quantity", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    sprinterqty = forms.IntegerField(required=False, label="Sprinter Van Quantity", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    automobileqty = forms.IntegerField(required=False, label="Automobile Quantity", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    highcubedqty = forms.IntegerField(required=False, label="High Cubed Quantity", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    straughttruckqty = forms.IntegerField(required=False, label="Straight Truck Quantity", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    dryvanqty = forms.IntegerField(required=False, label="Dry Van Quantity", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    reeferqty = forms.IntegerField(required=False, label="Reefer Quantity", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    flatbedqty = forms.IntegerField(required=False, label="Flat Bed Quantity", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    warehousesqft = forms.IntegerField(required=False, label="Warehouse Square Footage", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    totaltruckqty = forms.IntegerField(required=False, label="Total Truck QTY", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    is_totaltruckqty_auto = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))

    inductionfacilityloc1 = AddressField(required=False, widget=AddressWidget(attrs={'class' : 'text-lg h-10 w-full bg-gray-100 text-black my-2 inline rounded-xl transition ease-in-out px-3'}))
    inductionfacilityloc1_temp_controlled = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))

    inductionfacilityloc2 = AddressField(required=False, widget=AddressWidget(attrs={'class' : 'text-lg h-10 w-full bg-gray-100 text-black my-2 inline rounded-xl transition ease-in-out px-3'}))
    inductionfacilityloc2_temp_controlled = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))

    inductionfacilityloc3 = AddressField(required=False, widget=AddressWidget(attrs={'class' : 'text-lg h-10 w-full bg-gray-100 text-black my-2 inline rounded-xl transition ease-in-out px-3'}))
    inductionfacilityloc3_temp_controlled = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))

    inductionfacilityloc4 = AddressField(required=False, widget=AddressWidget(attrs={'class' : 'text-lg h-10 w-full bg-gray-100 text-black my-2 inline rounded-xl transition ease-in-out px-3'}))
    inductionfacilityloc4_temp_controlled = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))

    inductionfacilityloc5 = AddressField(required=False, widget=AddressWidget(attrs={'class' : 'text-lg h-10 w-full bg-gray-100 text-black my-2 inline rounded-xl transition ease-in-out px-3'}))
    inductionfacilityloc5_temp_controlled = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))


    inductionfacilityloc2 = AddressField(required=False, widget=AddressWidget(attrs={'class' : 'text-lg h-10 w-full bg-gray-100 text-black my-2 inline rounded-xl transition ease-in-out px-3'}))

    coverageradius = forms.IntegerField(required=False, label="City Coverage Radius", widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))



    usservice = forms.MultipleChoiceField(required=False, choices=STATES, widget=forms.CheckboxSelectMultiple())
    canservice = forms.MultipleChoiceField(required=False, choices=PROVINCES, widget=forms.CheckboxSelectMultiple())
    mexservice = forms.MultipleChoiceField(required=False,choices=MEXSTATES, widget=forms.CheckboxSelectMultiple())

    w9 = forms.FileField(required=False)
    insurance = forms.FileField(required=False)

    insuranceexp = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    operatingauth = forms.FileField(required=False)
    zipcoverage = forms.FileField(required=False)
    carrierbroker = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'sm:text-xl my-3 rounded-xl text-black transition ease-in-out w-full bg-gray-100'}))
    manualcarrierbroker = forms.FileField(required=False)

    group = forms.ModelMultipleChoiceField(queryset=Quote.objects.all(), required=False)

    # sign_page_url = forms.CharField(required=False)
    # skip_signal = forms.BooleanField(required=False)
    update = forms.BooleanField(required=False)
    contractsigned = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'w-5 h-5 ml-auto text-blue-600 bg-gray-100 border-gray-500 rounded focus:ring-blue-500'}))





    def __init__(self, *args, **kwargs):
        super(CarrierForm, self).__init__(*args, **kwargs)

        for fieldname in ['email']:
            self.fields[fieldname].help_text = None

    class Meta: 
        model = Carrier
        fields = '__all__'




class CarrierGroupForm(forms.ModelForm):
    class Meta:
        model = CarrierGroup
        fields = ['name']

class UploadCSVForm(forms.Form):
    user = forms.ModelChoiceField(required=False, queryset=NewUser.objects.all(), widget = forms.HiddenInput())
    file = forms.FileField(required=False)

    class Meta: 
      model = InboundOrderCSV
      fields = ['csvs']


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote

        fields = ['accepted']
        widgets = {
            'accepted': forms.RadioSelect(),
        }

class OrderDetailForm(forms.Form):
    external_id = forms.CharField(max_length=50)



class EmailTextForm(forms.Form):
    email_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 80}), label='Email Text')

def clean_phone_number(phone_number):
    if phone_number:
        phone_number = phone_number.replace('(', '')
        phone_number = phone_number.replace(')', '')
        phone_number = phone_number.replace(' ', '')
        phone_number = phone_number.replace('-', '')
        phone_number = '+1' + phone_number
    return phone_number


class CarrierDetailForm(forms.ModelForm):
    update = forms.BooleanField(initial=False, required=False, widget=forms.HiddenInput())

    class Meta:
        model = Carrier
        fields = ['company', 'email', 'contact', 'address', 'mainphone', 'mobilephone', 'fax', 'mcnumber', 'usdotnumber', 'feinnumber', 'techprovider', 'trackingtech', 'ownername', 'ownerphone', 'owneremail', 'dispatchname', 'dispatchphone', 'dispatchemail', 'accountingname', 'accountingphone', 'accountingemail', 'hazmat', 'smartway', 'ltl', 'ftl', 'b2b', 'tsa', 'lastmile', 'middlemile', 'transloading', 'airfreight', 'flatbeds', 'otr', 'refrigerated', 'hotshots', 'localpickupanddelivery', 'expedited', 'highvalue', 'drayage', 'whiteglove', 'residential', 'insidedelivery', 'medical', 'hemp', 'airport', 'lastmileqty', 'tsaqty', 'automobileqty', 'highcubedqty', 'sprinterqty', 'straughttruckqty', 'dryvanqty', 'reeferqty', 'flatbedqty', 'warehousesqft', 'totaltruckqty', 'is_totaltruckqty_auto', 'inductionfacilityloc1', 'inductionfacilityloc1_temp_controlled', 'inductionfacilityloc2', 'inductionfacilityloc2_temp_controlled', 'inductionfacilityloc3', 'inductionfacilityloc3_temp_controlled', 'inductionfacilityloc4', 'inductionfacilityloc4_temp_controlled', 'inductionfacilityloc5', 'inductionfacilityloc5_temp_controlled', 'coverageradius', 'usservice', 'canservice', 'mexservice', 'w9', 'insurance', 'operatingauth', 'zipcoverage', 'carrierbroker', 'manualcarrierbroker', 'insuranceexp', 'group', 'courier', 'contractsigned', 'update', 'notes', 'onboarded', 'is_onboarded_auto']



class CarrierUploadCSVForm(forms.Form):
    csv_file = forms.FileField()
    group = forms.ModelMultipleChoiceField(queryset=CarrierGroup.objects.all(), required=False)

    def clean_csv_file(self):
        f = self.cleaned_data['csv_file']

        if not str(f).endswith('.csv'):
            raise forms.ValidationError("Must be a CSV file")

        return f

    def save(self, commit=True):
        f = self.cleaned_data['csv_file']
        group = self.cleaned_data['group']
        reader = csv.reader(f.read().decode('utf-8').splitlines())

        # Skip header row
        next(reader)

        for row in reader:

            print(row)
            
            address_data = {
                'raw': f"{row[5]}, {row[3]}, {row[2]} {row[4]}",
                'locality': row[3],  # City
                'postal_code': row[4],  # ZIP
                'state': row[2],  # State
            }

            addr = Address(raw=address_data['raw'])
            addr.save()
            
            carrier_data = {
                'company': row[1],
                'email': row[10],
                'contact': row[15],
                'mainphone': clean_phone_number(row[8]),
                'mobilephone': clean_phone_number(row[9]),
                'hazmat': True if row[7] == 'Yes' else False if row[7] == 'No' else None,
                'totaltruckqty': row[6],
                'usdotnumber': row[11],
                'mcnumber': int(row[12][2:]),
                'skip_signal': True,
            }

            # Create Carrier object
            carrier = Carrier(**carrier_data)

            carrier.address = addr

            carrier.save()

            carrier.group.set(group)

            carrier.save()


class FilterForm(forms.Form):
    DELIVERY_STATUS_CHOICES = DELIVERY_STATUS_CHOICES
    start_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'date'}))
    end_date = forms.DateTimeField(required=False,  widget=forms.DateTimeInput(attrs={'type': 'date'}))
    customercity = forms.CharField(max_length=300, required=False)
    customerstate = forms.CharField(max_length=300, required=False)
    deliverystatus = MultiSelectFormField(max_choices=6, min_choices=1, max_length=80, choices=DELIVERY_STATUS_CHOICES, required= False)
        
        
    
    