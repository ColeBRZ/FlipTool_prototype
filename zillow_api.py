## https://www.zillow.com/robots.txt
## robots.txt provides the urls and zpid_text_files
## of all listed homes on zillow.

import http.client
import requests
import time
from random import uniform

conn = http.client.HTTPSConnection("zillow-com1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "XXXPut_your_ownXXX",
    'x-rapidapi-host': "XXXPut_your_ownXXX"
}


def get_home_description(zpid):
    max_retries = 5
    base_delay = 2
    url = f"https://zillow-com1.p.rapidapi.com/property?zpid={zpid}"

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                json_data = response.json()
                description = json_data.get("description")
                if description:
                    return description
                else:
                    print(f"No description found for ZPID {zpid}")
                    return None
            elif response.status_code == 429:
                delay = base_delay * (2 ** attempt)
                print(f"Rate limit reached. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Error: Received status code {response.status_code} for ZPID {zpid}")
                delay = base_delay * (attempt + 1)
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)

        except requests.exceptions.RequestException as e:
            print(f"Request error for ZPID {zpid}: {str(e)}")
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt) * uniform(0.5, 1.5)
                print(f"Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
            else:
                print(f"Max retries reached for ZPID {zpid}. Moving to next ZPID.")
                return None

    return None
