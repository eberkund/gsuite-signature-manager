#!/usr/bin/env python

from __future__ import print_function
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from pystache import Renderer, parse as parseTemplate
from httplib2 import Http
import csv
import json
import argparse
import json
import os


__version__ = '1.0.1'


parser = argparse.ArgumentParser(description='Change signatures for users',formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''Examples
---------
Do not call API but generate rendered files for each user in current directory:
>python3 set-signatures.py template.mustache --no-keystore -g

Using the credentials in keyfile.json, apply signature to all users in users.csv and writes each users signature to a file in output/:
>python3 set-signatures.py template.mustache -g output/

''')

parser.add_argument('template', metavar='template',
                    type=argparse.FileType('r'),
                   default='signature.mustache',
                   help='The mustache template file for the email')

parser.add_argument('--users', '-u', metavar='users', type=argparse.FileType('r'),
                   help='defaults to users.csv - CSV file with header. an "email" column is mandatory and all values are passed to rendering the template',
                   default='users.csv')

parser.add_argument('--keyfile', '-k', metavar='keyfile',
                    type=argparse.FileType('r'),
                   default='keyfile.json',
                   help='defaults to keyfile.json. The credentials for the GSuite service account with the https://www.googleapis.com/auth/gmail.settings.basic scope')
parser.add_argument('--no-keyfile',
                action='store_false',
                dest='keyfile',
                   help='Disables API calls (use with --generate to only create html templates)')

parser.add_argument('--generate', '-g',
                    metavar='outdir',
                    const='.',
                    nargs='?',
                   help='Output user signatures to given directory or current directory if used without a value ("--generate" or "-g")')


args = parser.parse_args()


with args.template as template_file:
    parsed_template = parseTemplate(template_file.read()) #Avoid reparsing for each email


credentials = None
if args.keyfile:
    scopes = ['https://www.googleapis.com/auth/gmail.settings.basic']
    with args.keyfile as keyfile_reader:
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.load(keyfile_reader), scopes)
else:
    print('No keyfile given, API calls disabled')

def change_signature(email, details):
    templated_signature = Renderer().render(parsed_template, details)
    send_as_body = {
        'signature': templated_signature 
    }

    if credentials and False:
        print('Changing signature for %s' % email)
        delegated_credentials = credentials.create_delegated(email)
        http_auth = delegated_credentials.authorize(Http())
        gmail = build('gmail', 'v1', http=http_auth)
        gmail.users().settings().sendAs().update(
            userId='me',
            sendAsEmail=email,
            body=send_as_body
        ).execute()
    if args.generate:
        outpath = os.path.join(args.generate, email) + '.html'
        print('Writing signature to %s' % outpath)
        with open(outpath,'w') as out:
            out.write(templated_signature)


with args.users as f:
    reader = csv.DictReader(f)
    for row in reader:
        change_signature(row['email'], row)