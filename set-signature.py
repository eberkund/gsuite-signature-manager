import json
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
from pystache import Renderer

scopes = [
	'https://mail.google.com/'
    'https://www.googleapis.com/auth/gmail.readonly',
]

# Authenticate with Google
credentials = ServiceAccountCredentials.from_json_keyfile_name('keyfile.json', scopes=scopes)
delegated_credentials = credentials.create_delegated('emargosian@neuronicworks.com')
http_auth = delegated_credentials.authorize(Http())

# Make API call
gmail = build('gmail', 'v1', http=http_auth)
results = gmail.users().labels().list(userId='me').execute()
labels = results.get('labels', [])

if not labels:
    print('No labels found.')
else:
    print('Labels:')
    for label in labels:
        print(label['name'])

template = Renderer().render_path('template.mustache', {
	'name': 'test',
	'position':
})

print template