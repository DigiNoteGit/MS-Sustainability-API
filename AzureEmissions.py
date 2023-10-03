import requests
import msal
import json


#requirements:
#1- register the MCFS SDS in your tenant (MCFS onboarding)
#2- Creating a service principal and generate a secret
#3- Grant App.Emission.Read permission to your service principal

# Your Azure AD App/Service Principal Registration details
CLIENT_ID = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
CLIENT_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
TENANT_ID = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
# get your mcfs instance id from it's url in the browser and replace it in the endpoint
# you can replace "demodata" in the endpoint with your billing account id to get your own emssion data. if you leave demodata api will provide some sample data
ENDPOINT = "https://api.mcfs.microsoft.com/api/v1.0/instances/[your mcfs instance id]/enrollments/demodata/emissions"
RESOURCE = "c3163bf1-092f-436b-b260-7ade5973e5b9"  # This is the universal id of MCFS SDS enterprise app!

# Create a confidential client application
app = msal.ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)

# Acquire token for the resource
result = app.acquire_token_for_client(scopes=[f"{RESOURCE}/.default"])

if "access_token" in result:
    # Use the token to call the API
    headers = {
        'Authorization': f"Bearer {result['access_token']}",
        'Ocp-Apim-Subscription-Key': '[your MCFS API key ]',
    }
    response = requests.get(ENDPOINT, headers=headers)

    data = response.json()['value']
    # Grouping total emissions by date and sub-service (you can build your own data model)
    grouped_data = {}
    for entry in data:
        date = entry['dateKey']
        subservice = entry['subService']
        emission = entry['totalEmissions']  #unit is metric tons of carbon dioxide equivalent (mtCO2e)

        if date not in grouped_data:
            grouped_data[date] = {}
        
        if subservice not in grouped_data[date]:
            grouped_data[date][subservice] = 0
        
        grouped_data[date][subservice] += emission

    # Convert the result to JSON format
    
    result_json = json.dumps(grouped_data, indent=4)
    print(result_json)


else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))