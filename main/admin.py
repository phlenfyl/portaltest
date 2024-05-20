from django.contrib import admin

# Register your models here.

from .models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea
from address.forms import AddressField, AddressWidget

from django.contrib import admin
from django.contrib.admin import AdminSite

admin.site.site_header = "357 Admin Portal"
admin.site.site_title = "357 Admin Portal"
admin.site.index_title = "Welcome to 357 Admin Portal"





class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email', 'company_name',)
    list_filter = ('email','company_name', 'is_active', 'is_staff','is_demo',)
    ordering = ('-start_date',)
    list_display = ('email', 'company_name',
                    'is_active', 'is_staff', 'is_demo')
    fieldsets = (
        (None, {'fields': ('email', 'company_name', 'company_address', 'company_phone', 'onboard')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_demo', 'user_permissions')}),
    )
    formfield_overrides = {
        NewUser.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
        AddressField: {'widget': AddressWidget(attrs={"style": "width: 500px;"})}
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'company_name', 'company_address', 'company_phone', 'password1', 'password2', 'is_active', 'is_staff', 'is_demo',)}
         ),
    )

class OrderAdmin(admin.ModelAdmin):
    list_display = ['externalid', 'deliverystatus']
    search_fields = ['externalid']

class PricingProposalInline(admin.TabularInline):
    model = PricingProposalFile
    extra = 1  # Number of empty forms displayed

class PricingAgreementInline(admin.TabularInline):
    model = PricingAgreementFile
    extra = 1

class CarrierModelAdmin(admin.ModelAdmin):
    inlines = [PricingProposalInline, PricingAgreementInline]
    
    

@admin.register(GeneratedReport)
class GeneratedReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'report_type', 'email', 'subject', 'description', 'automate')
    search_fields = ('user__username', 'subject', 'email')
    list_filter = ('report_type', 'automate')

@admin.register(ReportFilter)
class ReportFilterAdmin(admin.ModelAdmin):
    list_display = ('report', 'start_date', 'end_date', 'customercity', 'customerstate', 'deliverystatus')
    search_fields = ('report__subject', 'customercity', 'customerstate')
    list_filter = ('deliverystatus',)

@admin.register(TemplatedFilters)
class ReportFilterAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'customercity', 'customerstate', 'deliverystatus')
    search_fields = ('user__email', 'customercity', 'customerstate')
    list_filter = ('deliverystatus',)


admin.site.register(NewUser, UserAdminConfig)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderCSV)
admin.site.register(InboundOrderCSV)
admin.site.register(WebHook)
admin.site.register(Quote)
admin.site.register(QuoteAccount)
admin.site.register(Carrier, CarrierModelAdmin)
admin.site.register(RejectedQuote)
admin.site.register(LabelGroup)
admin.site.register(Label)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(SupportMessage)
admin.site.register(CarrierGroup)
admin.site.register(UDSOrder)










