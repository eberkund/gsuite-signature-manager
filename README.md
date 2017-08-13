# Signature Manager

This script allows administrators to change email signatures en masse using a convenient mustache template.

Tested with Python 2.7, you will need to install depenedencies first listed in the `requirements.txt` file

### Batteries Not Included

Missing from this repository:

- `users.csv` user email addresses, names and job titles
- `keyfile.csv` Google [service account credentials](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) available through [Developer Console](https://console.developers.google.com/iam-admin/serviceaccounts/)
