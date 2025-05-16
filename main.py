import requests
import pandas as pd
from config import API_KEY # Assuming config.py contains your API key and other configurations
import logging
from pprint import pprint

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='msba_app.log', filemode='w')
logger = logging.getLogger(__name__)

def get_data_from_api(api_url, params):
    try:
        response = requests.get(api_url, params)
        response.raise_for_status()
        pprint(response.json())   # Pretty print the JSON response for debugging
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error: {e}")
        logger.error(response.text)
        print(f"API request failed: {e}")
        return None

def create_dataframe(json_data):
    if json_data:
        return pd.json_normalize(json_data['articles']) #pd.DataFrame(json_data)
    else:
        return pd.DataFrame()
    
api_key = API_KEY # referencing the API key from config.py
api_url = "https://newsapi.org/v2/top-headlines"  # Example endpoint


params = {
    "country": 'us',  # Example parameter: Get top headlines from the US
    "apiKey": api_key,
}
json_data = get_data_from_api(api_url, params)
df = create_dataframe(json_data)

if not df.empty:
    print(df.head())

else:
    print("No data retrieved or DataFrame is empty.")