import requests
from requests.auth import HTTPBasicAuth
import json
import argparse
from  fdm_credentials import *

#fdm_file_policy_name = 'test1'
fdm_filetype = 'PDF'

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

# Print file Policy Content
def print_file_policy(fdm_hostname, token, file_policy_id):
    url = f"https://{fdm_hostname}/api/fdm/v6/policy/filepolicies/{file_policy_id}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}"
    }
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    file_policy = response.json()
    
    print("Policy Content:",json.dumps(file_policy, indent=4))



# Print file Policy Content
def print_file_policies(fdm_hostname, token):
    url = f"https://{fdm_hostname}/api/fdm/v6/policy/filepolicies"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}"
    }
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    file_policies = response.json()['items']
    
    print("Policy Content:",json.dumps(file_policies, indent=4))

# Print file Policy Content
def get_filetype(fdm_hostname, token, filetype):
    url = f"https://{fdm_hostname}/api/fdm/v6/object/filetypes?filter=name~{filetype}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}"
    }

    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    filetypes = response.json()['items']
    print("FileTypes:",json.dumps(filetypes, indent=4))
    

# Create a File Policy
def create_file_policy(fdm_hostname, token, fdm_file_policy_name): 
    url = f"https://{fdm_hostname}/api/fdm/v6/policy/filepolicies"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}"
    }
    # Reference
    # https://developer.cisco.com/docs/ftd-api-reference-v6-ftd-v6-7/addfilepolicy/#example

    payload = {
        "name": fdm_file_policy_name,
        "description": "API Generated Policy",
        "isSystemDefined": False,
        "type": "filepolicy"
    }
  
    response = requests.post(url, headers=headers, json=payload, verify=False)
    print(response.text)
    response.raise_for_status()
    return response.json()


# Add a file blocking rule for PDFs to the specified File Policy
def add_file_blocking_rule(fdm_hostname, token, file_policy_id, filetype_id): 
    url = f"https://{fdm_hostname}/api/fdm/v6/policy/filepolicies/{file_policy_id}/filerules"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}"
    }
    # https://developer.cisco.com/docs/ftd-api-reference-v6-ftd-v6-7/addfilerule/#data-parameters
    # File Type Info:
    # GET /object/filetypes

    payload = {
        "name": "Block PDF Files",
        "description" : "Block PDF Files",
        "applicationProtocols":"ANY",
        "ruleAction": "DETECT_FILES",
        "directionOfTransfer": "ANY",
        "fileTypes": [{
              "name": fdm_filetype,  
              "id": filetype_id,
              "type": "filetype"}],
        "type": "filerule"
    }
    response = requests.post(url, headers=headers, json=payload, verify=False)
    response.raise_for_status()
    return response.json()

# Main function
def main(fdm_file_policy_name):
    try:
        token = authenticate(fdm_hostname, fdm_username, fdm_password)
        print("Token Received.")
        print_file_policies(fdm_hostname, token)

        print(f"Creating new File Policy: {fdm_file_policy_name}")
        result = create_file_policy(fdm_hostname, token, fdm_file_policy_name)
        print(f"Done: {result}")
    

        file_policy_id = get_file_policy_id(fdm_hostname, token, fdm_file_policy_name)
        print(f"ID: {file_policy_id}")
        print_file_policy(fdm_hostname, token, file_policy_id)

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":

    parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,allow_abbrev=False,description="""Create FDM File Policy
    Example: fdm-create-file-policy.py -n policy_name """)
    parser.add_argument("-n",help="Name of the FDM File Policy",required=True)
    args=parser.parse_args()

    main(args.n)