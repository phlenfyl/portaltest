# # utils.py
# from django.db.migrations import operations
# from .models import Order, NewUser  # Import the Order model

# class ParseOrderData(operations.base.Operation):

#     def state_forwards(self, app_label, state):
#         for order_data in data:
#             order = Order()
#             order.externalid = order_data["externalid"]
#             order.deliverystatus = order_data["deliverystatus"]
#             order.statuscode = order_data["statuscode"]

#             # Handle date and time fields
#             if order_data.get("delivery"):
#                 order.delivery = datetime.datetime.strptime(order_data["delivery"], "%Y-%m-%dT%H:%M:%S")
#             if order_data.get("estimateddelivery"):
#                 order.estimateddelivery = datetime.datetime.strptime(order_data["estimateddelivery"], "%Y-%m-%dT%H:%M:%S")

#             order.placed = datetime.datetime.strptime(order_data["placed"], "%Y-%m-%dT%H:%M:%S")
#             order.customername = order_data["customername"]
#             order.customeraddress = order_data["customeraddress"]
#             order.customercity = order_data["customercity"]
#             order.customerstate = order_data["customerstate"]
#             order.customerzip = order_data["customerzip"]

#             # Assuming the user with email "demo@gmail.com" exists
#             demo_user = NewUser.objects.get(email="demo@gmail.com")  # Replace with your actual user model
#             order.user = demo_user

#             order.save()

#     def state_backwards(self, app_label, state):
#         # Implement logic to reverse the changes made in state_forwards (optional)
#         pass