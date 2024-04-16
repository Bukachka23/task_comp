import csv
import json

import gspread
import requests
import streamlit as st
from bs4 import BeautifulSoup
from google.oauth2.service_account import Credentials


class WebScraper:
    def __init__(self, url):
        self.url = url
        if 'data' not in st.session_state:
            st.session_state.data = []
        self.data = st.session_state.data
        self.session = requests.session()

    @st.cache(show_spinner=False)
    def scrape_data(self):
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.text, 'lxml')
        people_list = soup.select('div.speakers-list_list.is-4-columns > div.speakers-list_item')

        for person in people_list:
            name = person.select_one('h3.speakers-list_item-heading').text.strip()
            role = person.select_one('div.margin-bottom.margin-small > div:last-child').text.strip()
            img = person.select_one('img.image-absolute')['src']
            social_links = [link['href']
                            for link in person.select('div.w-layout-grid.speakers-list_social-list > a')]
            self.data.append({
                'Name': name,
                'Role': role,
                'Img': img,
                'Social Links': social_links
            })

    def save_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='', buffering=1) as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Role', 'Img', 'Social Links'])
            for item in self.data:
                writer.writerow([item['Name'], item['Role'], item['Img'], ', '.join(item['Social Links'])])

    def upload_to_google_spreadsheet(self, spreadsheet_name, credentials):
        gc = gspread.authorize(credentials)
        sh = gc.open(spreadsheet_name).sheet1
        header = ['Name', 'Role', 'Img', 'Social Links']
        data = [header] + [[item['Name'], item['Role'], item['Img'],
                            ', '.join(item['Social Links'])] for item in self.data]
        sh.update('A1', data)


if __name__ == "__main__":
    scraper = WebScraper('https://interaction24.ixda.org/')
    scraper.scrape_data()
    scraper.save_to_json('people_data.json')
    scraper.save_to_csv('people_data.csv')
    credentials = Credentials.from_service_account_info(
        info={
            "type": "service_account",
            "project_id": "your_project_id",
            "private_key_id": "your_private_key_id",
            "private_key": "your_private_key",
            "client_email": "your_client_email",
            "client_id": "your_client_id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "your_client_x509_cert_url"
        }
    )
    scraper.upload_to_google_spreadsheet('task_scraping', credentials)
