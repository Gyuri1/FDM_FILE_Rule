import requests
from requests.auth import HTTPBasicAuth
import json
import sys
import argparse
from  fdm_credentials import *

# Disable certificate warnings (not recommended for production use)
requests.packages.urllib3.disable_warnings()

# Authenticate and obtain a token
def authenticate(fdm_hostname, fdm_username, fdm_password):
    url = f"https://{fdm_hostname}/api/fdm/v6/fdm/token"
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'grant_type' : 'password',
        'username' : fdm_username,
        'password': fdm_password
        }
    response = requests.post(url, data=payload, verify=False)
    #Error Checking
    if response.status_code == 400:
        raise Exception("Error Received: {}".format(response.content))
    else:
        access_token = response.json()['access_token']
        return access_token


# Create a File Policy
def delete_file_policy(fdm_hostname, token, fdm_file_policy_id): 
    url = f"https://{fdm_hostname}/api/fdm/v6/policy/filepolicies/{fdm_file_policy_id}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}"
    }
    response = requests.delete(url, headers=headers, verify=False)
    #print(f"Response: {response}")
    response.raise_for_status()
    return response

# Find File Policy ID by name
def get_file_policy_id(fdm_hostname, token, policy_name):
    url = f"https://{fdm_hostname}/api/fdm/v6/policy/filepolicies"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}"
    }
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    file_policies = response.json()['items']
    
    for policy in file_policies:
        if policy['name'] == policy_name:
            return policy['id']
    return None

# Main function
def main(fdm_file_policy_name):
    try:

        token = authenticate(fdm_hostname, fdm_username, fdm_password)
        print("Token Received.")
     

        file_policy_id=get_file_policy_id(fdm_hostname, token,fdm_file_policy_name)
        print(f"ID: {file_policy_id}")

        print(f"Deleting File Policy: {fdm_file_policy_name}")
        result = delete_file_policy(fdm_hostname, token, file_policy_id)
        print(f"Done: {result}") 

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":

    parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,allow_abbrev=False,description="""Delete FDM File Policy
        Example: fdm-delete-file-policy.py -n policy_name """)
    parser.add_argument("-n",help="Name of the FDM File Policy",required=True)
    args=parser.parse_args()

    main(args.n)