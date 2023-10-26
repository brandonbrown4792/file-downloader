import csv
from pathlib import Path
import os
import requests
import urllib.request

mod_path = Path(__file__).parent
relative_path = '../data/media_urls.csv'

# WP blocks user agents from the python requests library, so we pretend we're something else
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36' }

with open((mod_path / relative_path).resolve()) as f:
    csvreader = csv.reader(f)
    next(csvreader)
    file_types = []

    count = 1
    for row in csvreader:
        url = row[2]
        file_pathname = url.partition('wp-content/uploads/')[2]
        file_path = (mod_path / ('../output/' + file_pathname)).resolve()
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        r = requests.get(url, headers=headers)
        print(f"{count}: Status: {r.status_code}, Downloading {url}")
        count += 1
        with open(file_path, 'wb') as outfile:
            outfile.write(r.content)
