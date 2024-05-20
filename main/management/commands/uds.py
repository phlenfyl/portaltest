from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import requests
from main.models import UDSOrder
from xml.etree import ElementTree as ET
from datetime import datetime
from django.utils.dateparse import parse_datetime
from main.models import Order, NewUser
import base64
from concurrent.futures import ThreadPoolExecutor
import time
import html
from django.db.models import Count, F, Q
from collections import defaultdict


class Command(BaseCommand):
    help = 'Post data to UDS endpoint for UDSOrders in the given timeframe'

    def encode_image(self, url):
        try:
            response = requests.get(url)
            return base64.b64encode(response.content).decode('utf-8')
        except Exception as e:
            return None

    def parse_and_update_order(self, xml_response, orders):
        xml_response = xml_response.replace('&AMP;', '&amp;') # Add this line to unescape the XML
        tree = ET.ElementTree(ET.fromstring(xml_response))

        # Get the most recent tracking event detail
        tracking_event_detail = tree.find('.//TrackingEventDetail')

        try:
            tracking_number = tree.find('.//TrackingNumber').text
        except Exception as e:
            return


        default_user = NewUser.objects.get(email='user@jointangelo.com')

        if tracking_number in orders:
            order = orders[tracking_number]

        else:
            order = Order(user=default_user, externalid=tracking_number)



        if tracking_event_detail is not None:
            event_status = tracking_event_detail.find('EventStatus').text
            event_datetime = tracking_event_detail.find('EventDateTime').text
            event_description = tracking_event_detail.find('EventDescription').text
            event_location = tracking_event_detail.find('EventLocation')

            # Assign the relevant data to order fields
            order.user = NewUser.objects.get(email='user@jointangelo.com')
            order.deliverystatus = event_description
            order.delivery = parse_datetime(event_datetime) if event_status == "D" else None
            order.customername = event_location.find('ActivityLocationName').text
            order.customeraddress = event_location.find('Address1').text
            order.customeraddress2 = event_location.find('Address2').text if event_location.find('Address2').text else None
            order.customercity = event_location.find('City').text
            order.customerstate = event_location.find('State').text
            order.customerzip = event_location.find('PostalcodePrimaryLow').text

            if event_status == "D":
                # Handle AdditionalLocationInfo and VPOD URL for delivered packages
                additional_location_info = tracking_event_detail.find('AdditionalLocationInfo')
                if additional_location_info is not None:
                    order.podcomments = additional_location_info.text

                vpod_url = tracking_event_detail.find('VPODURL')
                if vpod_url is not None and not order.confirmationimage:
                    encoded_image = vpod_url.text
                    if encoded_image:
                        order.confirmationimage = self.encode_image(encoded_image)

                order.save()


    def handle(self, *args, **kwargs):

        today = datetime.today().date()
        one_week_later = today + timedelta(weeks=1)
        a_week_ago = today - timedelta(weeks=1)

        orders = UDSOrder.objects.filter(
            date__gte = a_week_ago,
            date__lte=one_week_later
        )
        
        externalids = [order.externalid for order in orders]

        orderquery = Order.objects.filter(externalid__in=externalids)

        order_dict = defaultdict()

        for order in orderquery:
            order_dict[order.externalid] = order


        endpoint = "http://www.uniteddeliveryservice.com/uds/manifest/tracking/Vendor/4439"
        headers = {
            "Content-Type": "application/xml"
        }

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            start_time = time.time()

            for i, order in enumerate(orders):
                elapsed_time = time.time() - start_time

                if i % 10 == 0 and elapsed_time < 1:
                    time.sleep(1 - elapsed_time)
                    start_time = time.time()

                xml_body = f"""<?xml version="1.0" encoding="UTF-8"?>
                                <UDSTrackingRequest>
                                    <Validation>
                                        <UserID>357TangeloTracking</UserID>
                                        <Password>utr5HaK7qx9Wf2321</Password>
                                    </Validation>
                                    <TrackingNumber>{order.externalid}</TrackingNumber>
                                </UDSTrackingRequest>"""

                future = executor.submit(requests.post, endpoint, data=xml_body, headers=headers)
                futures.append((future, order))

            for future, order in futures:
                response = future.result()

                if response.status_code == 200:
                    self.parse_and_update_order(response.text, order_dict)

