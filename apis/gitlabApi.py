import json
import requests

from helpers.helper import get_gitlab_token

GITLAB_TOKEN = get_gitlab_token()

gitlabHeaders = restHeaders = {'Content-Type': 'application/json; charset=utf-8', 'PRIVATE-TOKEN': GITLAB_TOKEN}

def get_gitlab_groups(page, perPage):
    url = f'https://gitlab.com/api/v4/groups'
    gitlabParams = {"page": page,"per_page": perPage}  

    try:
        response = requests.get(url, headers=gitlabHeaders, params=gitlabParams)
        return response.json(), response.headers
    except:
        # Raise an error for bad status codes
        response.raise_for_status()
        print(response.json())

def collect_gitlab_groups():
    print('Collecting GitLab groups')
    page = 1
    perPage = 10
    groupData = []

    while True:
        groups, headers = get_gitlab_groups(page, perPage)
        if not groups:
            print('No groups found')
            # Exit the loop if no groups are returned
            break  

        for group in groups:
            groupData.append(group)

        if 'X-Next-Page' in headers and headers['X-Next-Page']:
            page = int(headers['X-Next-Page'])
        else:
            print('Returning GitLab group data')
            return groupData

def get_gitlab_subgroup(groupId, page, perPage):
    print('Collecting GitLab subgroup')

    url = f'https://gitlab.com/api/v4/groups/{groupId}/subgroups'
    gitlabParams = {"page": page,"per_page": perPage}

    try:
        response = requests.get(url, headers=gitlabHeaders, params=gitlabParams)
        return response.json(), response.headers
    except:
        # Raise an error for bad status codes
        response.raise_for_status()
        print(response.json())

def get_single_gitlab_group(groupId):
    print('Collecting GitLab group')
    url = f'https://gitlab.com/api/v4/groups/{groupId}'

    try:
        response = requests.get(url, headers=gitlabHeaders)
        return response.json()
    except:
        # Raise an error for bad status codes
        response.raise_for_status()
        print(response.json())

def collect_gitlab_subgroups(groupId):
    print('Collecting GitLab groups')
    page = 1
    perPage = 10
    subgroupData = []

    while True:
        subgroups, headers = get_gitlab_subgroup(groupId, page, perPage)
        if not subgroups:
            print('No groups found')
            # Exit the loop if no groups are returned
            break  

        for subgroup in subgroups:
            subgroupData.append(subgroup)

        if 'X-Next-Page' in headers and headers['X-Next-Page']:
            page = int(headers['X-Next-Page'])
        else:
            print('Returning GitLab subgroup data')
            return subgroupData
        