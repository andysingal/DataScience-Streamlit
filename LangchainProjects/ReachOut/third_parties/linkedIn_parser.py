import os 
import re
import json
import requests
from loguru import logger
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

def linkedIn_scrap(profile_url: str, mock: bool = True) -> Dict:
    """
        Scrapes information from the LinkedIn Profile
        Manually scrap information from the LinkedIn profile.
    """
    if mock:
        # linkedIn_profile_gist_url = "https://gist.githubusercontent.com/rcapdepaula/43b320e5f9ed1656ab047258f428cbc2/raw/51070719fb0b201a718e1819b580d38ac8f37dfb/ricardo.json"
        linkedIn_profile_gist_url = "https://gist.github.com/Jay-Nehra/027f554fea2a018ac8840b93e56181c9"
        try:
            response = requests.get(
                url=linkedIn_profile_gist_url,
                timeout=15
            )
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
    else:
        # I am not attempting to directly connect to the LinkedIn API at the moment. `Proxycurl` can be used to do this bu the alloted tokens are quite less and I do not want to create an account at the moment for this POC. 
        # return "We do not support the LinkedIn API Connections and scraping at the moment. You can set the `mock` flag to access the precollected linkedIn profile data in a publically available gist or supply your own."
        
        # Added the support for the proxycurl LinkedIn api client.
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={"url": profile_url},
            headers=header_dic,
            timeout=10,
        )

    data = response.json()
    
    static_profile_data_dir = 'linkedIn_profile_data'
    filename = 'profile_data.json'
    file_path = os.path.join(static_profile_data_dir, filename)

    data = response.json()

    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    full_name = data.get("full_name", "profile_data")
    filename = re.sub(r'[^\w\s-]', '', full_name).strip().replace(' ', '_') + '.json'

    static_profile_data_dir = 'linkedIn_profile_data'
    file_path = os.path.join(static_profile_data_dir, filename)

    if not os.path.exists(static_profile_data_dir):
        os.mkdir(static_profile_data_dir)

    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Data successfully written to {file_path}")
    return data


if __name__=='__main__':
    profile_data = linkedIn_scrap('https://in.linkedin.com/in/jayant-nehra', False)
    print(profile_data)