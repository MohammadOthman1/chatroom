import requests
import json

api_url = "http://localhost:3000/sign-up"  # Replace with the actual URL of your API

#Define the query parameters
def fetching(username, email, password):
    params = {
        "username": username,
        "email": email,
        "password": password,
    }

    #Make a GET request to the API
    response = requests.post(api_url, params=params)
    data = json.loads(response.text)
    print(data)
