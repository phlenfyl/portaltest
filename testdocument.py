import requests

import requests

url = 'https://esignatures.io/api/contracts'
# token = 'd6f3eb1f-4596-4c3f-8141-606fada04c93'
headers = {'Content-Type': 'application/json'}
data = {
    'template_id': 'dfed7052-b1c0-45a8-a880-e5acd45e4875',
    'signature_request_delivery_method': 'embedded',
    'signers': [
        {
            'name': 'Sam Signer',
            'email': 'richard@357company.com'
        }
    ],
    'redirect_url': 'https://www.example.com/thank-you'
}

response = requests.post(url=url, headers=headers, params={'token': token}, json=data)

if response.status_code == 200:
    response_json = response.json()
    sign_page_url = response_json['data']['contract']['signers'][0]['sign_page_url']
    print('SIGN_PAGE_URL:', sign_page_url)
    # Replace the SIGN_PAGE_URL in the iframe code with the actual sign_page_url
else:
    print('Error:', response.text)
