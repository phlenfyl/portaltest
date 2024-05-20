from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'orders', views.OrderViewSet, basename='Orders')







urlpatterns = [

    path('', views.index, name="index"),
    path('api/', include(router.urls)),
    path('login/', views.CustomLoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('csv', views.download_csv, name='csv'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('demodashboard', views.DemoDashboard.as_view(), name='demodashboard'),
    path('toggle-automate/<int:report_id>', views.update_automation, name='toggle_automate'),
    
    #dev code  
    path('automation/', views.automations, name='automation'),
    path('report-history/', views.report_history, name='report_history'),
    path('report-templates/', views.report_templates, name='report_templates'),
    path('data-report/', views.data_report, name='data_report'),
    path('download-report/<int:report_id>', views.download_report, name='download_report'),
    path('add-template/', views.add_report_template, name='add_template'),
    path('map/<int:external_id>', views.map, name='map'),
    
    path('csvupload', views.InboundUpload.as_view(), name='csvupload'),
    path('cxtwebhook', views.cxt_webhooks, name='cxtwebhooks'),
    path('esignwebhook', views.esign_webhooks, name='esignwebhooks'),
    path('quote/<pk>/', views.QuoteDetail.as_view(), name='quotedetail'),
    path('rejected', views.ReasonCreate.as_view(), name='rejectedreason'),
    path('carriers/', views.CarrierCreate.as_view(), name='carriers'),
    # path('lastmile', views.LastMileCarrierCreate.as_view(), name='carriers'),
    path('order-detail/', views.get_externalId_order_view, name='order_detail'),
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('adminquote/', views.QuoteCreateView.as_view(), name='adminquote'),
    path('adminquoteaccount/', views.QuoteAccountView.as_view(), name='adminquoteaccount'),
    path('quotedashboard/', views.QuoteDashboard, name='quote_dashboard'),
    # path('carrier/<int:pk>/followup/', views.CarrierFollowUp.as_view(), name='carrier_followup'),
    path('carrierlist/', views.CarrierListView.as_view(), name='carrier_list'),
    path('labelgroup/create/', views.LabelGroupCreateView.as_view(), name='labelgroup_create'),
    path('generate_pdf/<int:group_id>/', views.generate_pdf, name='generate_pdf'),
    path('auction/create/', views.AuctionCreateView.as_view(), name='auction-create'),
    path('carrierfilter/', views.CarrierFilterView.as_view(), name='carrierfilter'),
    path('bid/create/<int:auction_id>/<int:carrier_id>/', views.BidCreateView.as_view(), name='bid-create'),
    path('auctions/', views.AuctionListView.as_view(), name='auction-list'),
    path('auctions/<int:pk>/', views.AuctionDetailView.as_view(), name='auction-detail'),
    path('bid/<int:pk>/', views.BidDetailView.as_view(), name='bid_detail'),
    path('support/', views.SupportRequestView.as_view(), name='support_request'),
    path('confirmation_image/<int:order_id>/', views.confirmation_image, name='confirmation_image'),
    # path('parse-email-text/', views.parse_email_text, name='parse_email_text'),
    path('carrier/<int:pk>/', views.CarrierDetailView.as_view(), name='carrier-detail'),
    path('carrier_group/', views.CarrierGroupListView.as_view(), name='carrier-group-list'),
    path('upload_csv/', views.CarrierCsvUploadView.as_view(), name='carrier_upload_csv'),
    path('upload_uds/', views.UDSOrderCreateView.as_view(), name='uds_upload_csv'),
    path('shipperlist/', views.shipperlist, name='shipperlist'),
    path('carrier/update/<int:pk>/', views.CarrierUpdateView.as_view(), name='carrier_update'),
    path('analytics', views.analytics, name='carrier_update'),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(), 
        name="password_reset_complete"),



]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)