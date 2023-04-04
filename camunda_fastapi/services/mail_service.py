import os
import json
import datetime
import chevron
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


path = "workspace/mails/";

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.send']
flow = InstalledAppFlow.from_client_secrets_file('client_secret_google_api.json', SCOPES)

def resolve(name:str) -> str:
    return path+name

def find_names() -> list:
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    return os.listdir(path)

def find_by_name(name:str) -> dict:
    f = open(resolve(name))
    data = json.load(f)
    f.close()
    return data

def save(mail:dict) -> dict:
    mail["modified"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    json_object = json.dumps(mail, indent=4)
    with open(resolve(mail["name"]), "w") as outfile:
        outfile.write(json_object)
    return mail

def delete(name:str):
    os.remove(resolve(name))

def send_mail(to:str, subject:str, template:str, locale:str, variables:dict):

        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret_google_api.json', SCOPES)
                creds = flow.run_local_server(port=8888)
                print(creds.to_json())
        # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())


        service = build('gmail', 'v1', credentials=creds)
        template = find_by_name(template+'-'+locale.lower())["htmlTemplate"]
        mail = chevron.render(template, variables)
        message = MIMEText(mail, 'html')
        message['to'] = to
        message['subject'] = subject

        create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

        message = (service.users().messages().send(userId="me", body=create_message).execute())