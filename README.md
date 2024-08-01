# SDA Excellent Planner

## Setup

### Google Cloud API

1. Firstly, you need to setup your Google Cloud API 
2. Create new app
3. Create a service account for the app
4. Get service account key (json file) - don't forget to later add the path to `.env` (`secret/google-auth.json`)

### Share calendar with your account

- Run this script with filled in correct data, which will share service account's calendar with your main account
```python
from oauth2client.service_account import ServiceAccountCredentials

main_account_email = '<FILL_IN>'
service_account_key_file = '<FILL_IN>'

creds = ServiceAccountCredentials.from_json_keyfile_name(
    service_account_key_file, ['https://www.googleapis.com/auth/calendar']
)
service = build("calendar", "v3", credentials=creds)
created_rule = service.acl().insert(calendarId=calendar_id, body=rule).execute()
print(f"Calendar shared with {main_account_email}. ACL Rule ID: {created_rule.get('id')}")
```

### Environment variables

- Create `.env` file from `template.env` and fill all variables

### Install dependencies

```sh
poetry install
```

## Run

- Just run
```sh
poetry run python src/main.py
```
- This will fetch all necessary data from specified sheets and create new events in Google Calendars based on them
