# import requests
# import json

# headers = {
#   'Accept': 'application/json',
#   'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMmE4ZGEzZDUtZTQ4Mi00NWJkLWI0NGItM2ZkM2I0ZDhiZTRmIiwib3JnX2lkIjoiZmY3NWEzNmQtZDNjOC00ZDgwLTlhNzUtNTA1OGMzZDE1OTA5Iiwib3JnX3R5cGVfaWQiOiJicm9rZXIiLCJ1c2VyX3JvbGUiOiJhZG1pbiIsImFjY2Vzc190eXBlIjoicmVndWxhciIsImV4cCI6MTY3NDI3OTk0MiwiaWF0IjoxNjc0MTkzNTQyfQ.NQ7mhBd0HpUFNisAABrLgqmafs344x9v1HqIzCe2LO8'
# }

# r = requests.get('https://platform.roserocket.com/api/v1/partner_carriers', headers = headers)

# print(r.json())



from .models import *



c = GeneratedReport.objects.filter(pk = 12)

print(c)


# 0DFFD71B-7B7B-4469-8355-DD4E3226780E
