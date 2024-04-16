import json

from google.oauth2.service_account import Credentials


def get_credentials(file_name='credentials_config.json'):
    try:
        with open(file_name) as f:
            credentials_info = json.load(f)
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
            return credentials
    except FileNotFoundError:
        print(f"{file_name} not found.")
        return None
