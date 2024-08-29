import json
import requests
from requests.exceptions import HTTPError
import time

from helpers.helper import get_snyk_token

SNYK_TOKEN = get_snyk_token()

restHeaders = {'Content-Type': 'application/vnd.api+json', 'Authorization': f'token {SNYK_TOKEN}'}
v1Headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': f'token {SNYK_TOKEN}'}

def get_org_integrations(orgId, orgName):
    print(f"Collecting organization integrations for {orgName}")
    url = f'https://api.snyk.io/v1/org/{orgId}/integrations'

    try:
        integrationsApiResponse = requests.get(url, headers=v1Headers)
        return integrationsApiResponse.json()
    except HTTPError as exc:
        # Raise an error
        print("Snyk Integrations endpoint failed.")
        print(exc)


def get_snyk_orgs(groupId):
    print("Collecting organization IDs")
    url = f'https://api.snyk.io/rest/groups/{groupId}/orgs?version=2024-05-08&limit=100'
    hasNextLink = True
    orgs = []

    while hasNextLink:
        try:
            orgApiResponse = requests.get(url, headers=restHeaders)
            orgData = orgApiResponse.json()['data']
            orgs.extend(orgData)
        except:
            print("Orgs endpoint call failed.")
            print(orgApiResponse)
        
        # Check if next page exist and set url if it does.  If not, exit and return issuesData
        try:
            orgApiResponse.json()['links']['next']
            url = 'https://api.snyk.io' + orgApiResponse.json()['links']['next']
        except:
            hasNextLink = False
            return orgs