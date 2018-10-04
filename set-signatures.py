#!/usr/bin/env python

from __future__ import print_function
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from pystache import Renderer
from httplib2 import Http
import csv
import json

__version__ = '1.0.0'

scopes = ['https://www.googleapis.com/auth/gmail.settings.basic']
credentials = ServiceAccountCredentials.from_json_keyfile_name('keyfile.json', scopes)

def change_signature(email, name, title):
    delegated_credentials = credentials.create_delegated(email)
    http_auth = delegated_credentials.authorize(Http())
    gmail = build('gmail', 'v1', http=http_auth)
    send_as_body = {
        'signature': Renderer().render_path('template.mustache', {
            'name': name,
            'title': title
        })
    }

    print('Changing signature for %s' % email)

    gmail.users().settings().sendAs().update(
        userId='me',
        sendAsEmail=email,
        body=send_as_body
    ).execute()

with open('users.csv', 'rb') as f:
    reader = csv.reader(f)
    next(reader, None)
    for row in reader:
        change_signature(row[0], row[1], row[2])
