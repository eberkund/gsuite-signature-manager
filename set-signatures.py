import csv
import json
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
from pystache import Renderer

scopes = [
    'https://mail.google.com/'
    'https://www.googleapis.com/auth/gmail.readonly',
]

credentials = ServiceAccountCredentials.from_json_keyfile_name('keyfile.json', scopes)

def change_signature(name, email, position):
    delegated_credentials = credentials.create_delegated(email)
    http_auth = delegated_credentials.authorize(Http())

    gmail = build('gmail', 'v1', http=http_auth)
    results = gmail.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    signature = Renderer().render_path('template.mustache', {
        'name': name,
        'position': position
    })

def main:
    with open('users.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            change_signature(row[0], row[1], row[2])
