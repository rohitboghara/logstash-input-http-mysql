# Python Client Example for Logstash Input HTTP MySQL

import requests

# Sample configuration
url = 'http://localhost:5044'

# An example payload to send to Logstash
payload = {
    'query': 'SELECT * FROM your_table',
    'database': 'your_database',
    'user': 'your_user',
    'password': 'your_password'
}

try:
    # Sending the request to Logstash
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print('Data sent successfully!')
    else:
        print(f'Failed to send data: {response.status_code} - {response.text}')
except Exception as e:
    print(f'An error occurred: {e}').