import csv
import json
from io import StringIO

import streamlit as st

from gs_script import WebScraper

st.title('TEST_GSCRAPING')

url = st.text_input('Enter the URL to scrape:', 'https://interaction24.ixda.org/')

scraper = WebScraper(url)


if st.button('Scrape Data'):
    scraper.scrape_data()
    st.success('Data scraped successfully!')

if st.checkbox('Show scraped data'):
    st.write(scraper.data)

if st.download_button('Download JSON', json.dumps(scraper.data, indent=4), "text/json", "people_data.json"):
    st.success('Data saved to JSON file successfully!')

csv_string = StringIO()
csv_writer = csv.writer(csv_string)
csv_writer.writerow(['Name', 'Role', 'Img', 'Social Links'])
for item in scraper.data:
    csv_writer.writerow([item['Name'], item['Role'], item['Img'], ', '.join(item['Social Links'])])
if st.download_button('Download CSV', csv_string.getvalue(), "text/csv", "people_data.csv"):
    st.success('Data saved to CSV file successfully!')

if st.button('Upload Data to Google Spreadsheet'):
    scraper.upload_to_google_spreadsheet('task_scraping')
    st.success('Data uploaded to Google Spreadsheet successfully!')

st.write('''
    <a target="_self" href="https://docs.google.com/spreadsheets/d/1m1w7L36x0wbPXCcZvLndiwnETEGRLDnTLFzWYP8if_Y/edit?usp=sharing">
        <button>
            Go to Google Spreadsheet
        </button>
    </a>
    ''',
         unsafe_allow_html=True
         )
