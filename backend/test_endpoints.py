import requests
import json

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzgwMTYxMTIxfQ.-PBgJ7vCFTNMTeDBKvTjR9fgRVc0LIIqFz2Tg72MnKw'
headers = {'Authorization': f'Bearer {token}'}

# Pending
print('=== PENDING ===')
response = requests.get('http://127.0.0.1:8000/api/v1/admin/student-applications', headers=headers)
data = response.json()
print(f'Count: {len(data)}')
for s in data:
    print(f'  - {s["first_name"]} {s["last_name"]}: {s["status"]}')

# Approved
print('\n=== APPROVED ===')
response = requests.get('http://127.0.0.1:8000/api/v1/admin/student-applications-approved', headers=headers)
data = response.json()
print(f'Count: {len(data)}')
for s in data:
    print(f'  - {s["first_name"]} {s["last_name"]}: {s["status"]}')

# Rejected
print('\n=== REJECTED ===')
response = requests.get('http://127.0.0.1:8000/api/v1/admin/student-applications-rejected', headers=headers)
data = response.json()
print(f'Count: {len(data)}')
for s in data:
    print(f'  - {s["first_name"]} {s["last_name"]}: {s["status"]}')
