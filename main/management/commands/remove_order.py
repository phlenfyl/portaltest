from django.core.management.base import BaseCommand
from django.utils import timezone
from main.models import Order

class Command(BaseCommand):
    help = 'Remove the confirmation image from all orders older than 6 months'

    def handle(self, *args, **kwargs):
        six_months_ago = timezone.now() - timezone.timedelta(days=180)
        orders = Order.objects.filter(delivery__lt=six_months_ago)
        for order in orders:
            order.confirmationimage = None  # replace 'confirmation_image' with your actual field name
            order.save()
        self.stdout.write(self.style.SUCCESS('Successfully removed confirmation images from old orders'))