# Signature Manager

Allows G Suite administrators to change email signatures en masse using a convenient mustache template.

### Setup

Install the dependencies using `pip`,

```
pip install -r requirements.txt
```

You will also need to create,

- `users.csv` user email addresses, names and job titles
- `keyfile.json` Google [service account credentials](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) available through [Developer Console](https://console.developers.google.com/iam-admin/serviceaccounts/)

### Usage

After setup you can just run the script,

```
./set-signatures.py
```
