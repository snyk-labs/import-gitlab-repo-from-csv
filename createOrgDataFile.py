import csv
import time
from apis.gitlabApi import collect_gitlab_subgroups, get_single_gitlab_group
from apis.snykApi import get_org_integrations, get_snyk_orgs
from datetime import datetime, timezone
import json
import sys 
import os

def extractCsvData():
    csv_data = []
    business_unit_and_gitlab_data = []

    # Path to your CSV file
    try:
        print("Found CSV_FILE_PATH environment variable.")
        CSV_FILE_PATH = os.getenv("CSV_FILE_PATH")
    except:
        print("CSV_FILE_PATH environment variable not specified.")

    # Try to open CSV file
    try:
        with open(CSV_FILE_PATH, mode='r') as file:
            # Create a CSV reader object
            csv_reader = csv.reader(file)
            
            # Read the header (if present)
            header = next(csv_reader)
            # print(f'Header: {header}')

            for row in csv_reader:
                csv_data.append(row)
            
    except:
        print(f'Failed to open {CSV_FILE_PATH}')

    business_unit_index = header.index('Business Unit')
    gitLab_group_id_index = header.index('GitLab Group ID')

    # Read each row in the CSV file
    for row in csv_data:
        new_data = {
                "businessUnit" : row[business_unit_index],
                "gitlabGroupId" : row[gitLab_group_id_index]
            }
        business_unit_and_gitlab_data.append(new_data)
    
    return business_unit_and_gitlab_data

# Write snyk-created-orgs.json file
def writeJsonFile(orgDataObject, index):
    print("Writing to json file")
    fileName = f'snyk-created-orgs-{index}.json'
    try:
        with open(fileName, 'w') as json_file:
            json.dump(orgDataObject, json_file, indent=4)
    except:
        print('Failed to create json file.')

def createOrgData(topLevelData, subgroupsData, snykOrgData):
    snykApiImportOrgDataObject = []

    if subgroupsData:
        for index, subgroup in enumerate(subgroupsData):
            if index == 0:
                snykIntegrations = get_org_integrations(snykOrgData['id'], snykOrgData['attributes']['name'])
                newSnykApiImportOrgDataObject = {
                        "name": subgroup['full_path'],
                        "orgId": snykOrgData['id'],
                        "integrations": snykIntegrations,
                        "groupId": sys.argv[1]
                    }
                snykApiImportOrgDataObject.append(newSnykApiImportOrgDataObject)
                newTopLevelSnykApiImportOrgDataObject = {
                        "name": topLevelData['full_path'],
                        "orgId": snykOrgData['id'],
                        "integrations": snykIntegrations,
                        "groupId": sys.argv[1]
                    }
                snykApiImportOrgDataObject.append(newTopLevelSnykApiImportOrgDataObject)
            else:
                snykIntegrations = get_org_integrations(snykOrgData['id'], snykOrgData['attributes']['name'])
                newSnykApiImportOrgDataObject = {
                        "name": subgroup['full_path'],
                        "orgId": snykOrgData['id'],
                        "integrations": snykIntegrations,
                        "groupId": sys.argv[1]
                    }
                snykApiImportOrgDataObject.append(newSnykApiImportOrgDataObject)
    return snykApiImportOrgDataObject

def createOrgDataFile():
    print('Creating orgData file for Snyk Api Import')
    # Get Snyk org data
    snykOrgs = get_snyk_orgs(sys.argv[1])

    csvData = extractCsvData()

    snykApiImportOrgDataObject = []

    count = 1
    for groupData in csvData:
        # Check to see if Business unit is a Snyk organization
        # print(groupData)
        try:
            index = next((i for i, item in enumerate(snykOrgs) if item['attributes']['name'].lower() == groupData['businessUnit'].lower()), -1)
            # print(json.dumps(snykOrgs[index], indent=2))
            topLevelData = get_single_gitlab_group(groupData['gitlabGroupId'])
            subgroupData = collect_gitlab_subgroups(groupData['gitlabGroupId'])
        except:
            print(f"{groupData['businessUnit']} doesn't exist in group.")
            continue
            
        newSubgroupOrgDataObject = createOrgData(topLevelData, subgroupData, snykOrgs[index])
        for orgData in newSubgroupOrgDataObject:
            snykApiImportOrgDataObject = {"orgData": [orgData]}
            writeJsonFile(snykApiImportOrgDataObject, count)
            count = count + 1

# Run app
createOrgDataFile()