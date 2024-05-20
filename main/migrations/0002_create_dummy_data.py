import json, os
from django.db import migrations
from datetime import datetime
from main.models import Order, NewUser

def load_dummy_orders(apps, schema_editor):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get the directory of the current file
    json_file_path = os.path.join(base_dir, 'dummy_data.json')
    # Read the JSON file with dummy data
    with open(json_file_path, 'r') as f:
        dummy_orders = json.load(f)

    # Get the demo user
    demo_user = NewUser.objects.filter(email='demo@gmail.com').first()

    if demo_user:
        # Create Order objects from dummy data
        for order_data in dummy_orders:
            order_data["user"] = demo_user  # Assign the user to the order
            Order.objects.create(**order_data)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),  # Replace with the actual dependency
    ]

    operations = [
        migrations.RunPython(load_dummy_orders),
    ]
