import time
import signrequest_client
from signrequest_client.rest import ApiException
from pprint import pprint


default_configuration = signrequest_client.Configuration()
# default_configuration.api_key['Authorization'] = '0357fae09db61bc8fcfd1808faf4b4b3e7ab170e'
default_configuration.api_key_prefix['Authorization'] = 'Token'
signrequest_client.Configuration.set_default(default_configuration)

# api_instance = signrequest_client.DocumentsApi()
# data = signrequest_client.Document(template="https://test357company.signrequest.com/api/v1/templates/c650d17a-9584-458d-b0d3-5fa80da89839/")

# api_response = api_instance.documents_create(data)


import signrequest_client

api_instance = signrequest_client.SignrequestsApi()
data = signrequest_client.SignRequest(
    document="https://signrequest.com/api/v1/documents/6d357537-7340-4294-be8c-538bec8a9451/",
    signers=[
        {
            "email": "richard@357company.com",
        }
    ],
    from_email="richard@357company.com",
)

api_response = api_instance.signrequests_create(data)




print(api_response)





