import requests
from dotenv import load_dotenv
import os

load_dotenv()  

FIGMA_TOKEN = os.getenv("FIGMA_TOKEN")
FILE_KEY = os.getenv("FILE_KEY")

headers = {"X-Figma-Token": FIGMA_TOKEN}
url = f"https://api.figma.com/v1/files/{FILE_KEY}"
response = requests.get(url, headers=headers)
data = response.json()

## id 29 has the mr 


if response.status_code == 200:
    data = response.json()
    print("Original Data:", data)

    # Step 2: Edit the value with the name "Minuted Listened Value"
    def update_minuted_listened_value(json_data, new_value):
        # Traverse the JSON to find and update the value
        for key, value in json_data.items():
            if isinstance(value, dict):  # If the value is a nested dictionary, recurse
                update_minuted_listened_value(value, new_value)
            elif isinstance(value, list):  # If the value is a list, iterate through it
                for item in value:
                    if isinstance(item, dict):
                        update_minuted_listened_value(item, new_value)
            elif key == "Minuted Listened Value":  # If the key matches, update the value
                json_data[key] = new_value

    # Update the value
    update_minuted_listened_value(data, "Updated Value")

    print("Updated Data:", data)

    # Step 3: Send the updated JSON back to the API
    update_url = f"https://api.figma.com/v1/files/{FILE_KEY}"
    update_response = requests.put(update_url, headers=headers, json=data)

    if update_response.status_code == 200:
        print("Successfully updated the value on the API.")
    else:
        print("Failed to update the value on the API:", update_response.status_code, update_response.text)
else:
    print("Failed to fetch data from the API:", response.status_code, response.text)