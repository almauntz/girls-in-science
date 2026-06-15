#!/usr/bin/env python
import requests
import json

# Test data
data = {
    'first_name': 'Test',
    'last_name': 'Student',
    'email': 'test.direct@example.com',
    'faculty': 'Fakultet informatike',
    'year_of_study': '2. godina',
    'areas_of_interest': 'IT, Data',
    'expectations': 'Learn software development',
    'skills_to_improve': 'Leadership',
    'motivational_message': 'I am very motivated',
    'preferred_session_format': 'Online',
    'session_commitment': 'false',  # Changed to string
    'has_business_idea': 'Ne',
    'consent_data': 'true',  # Changed to string
    'consent_evaluation': 'true'  # Changed to string
}

# Make request
response = requests.post(
    'http://127.0.0.1:8000/api/v1/students/register',
    data=data
)

print(f'Status: {response.status_code}')
if response.status_code != 201:
    try:
        print(f'Response JSON: {json.dumps(response.json(), indent=2)}')
    except:
        print(f'Response Text: {response.text}')
else:
    print(f'Success: {json.dumps(response.json(), indent=2)}')
