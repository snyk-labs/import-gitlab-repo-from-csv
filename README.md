# Create snyk-created-orgs.json based off of Snyk Organization Names

This script will search your GitLab groups for any matching Snyk organization based off of GitLab group mapping in a csv.  If matches are found, it will generate snyk-created-orgs.json which will be used to import repos into Snyk.

## Requirements

Python version 3.9.5

Download [snyk-api-import](https://github.com/snyk/snyk-api-import/releases), make the file executable, and place the file in the root directory of the cloned repo.

## Environment Variables

[GITLAB_TOKEN](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)

[SNYK_TOKEN](https://docs.snyk.io/getting-started/how-to-obtain-and-authenticate-with-your-snyk-api-token)

SNYK_LOG_PATH - This needs to be the full path to the root directory of this repo.

CSV_FILE_PATH - Full path to the csv file with GitLab group data.

## Script Arguments

[SNYK_GROUP_ID](https://docs.snyk.io/snyk-admin/groups-and-organizations/groups/group-general-settings)

## Running
```bash
export SNYK_TOKEN=TYPE-SNYK-TOKEN-HERE
export GITLAB_TOKEN=TYPE-GITLAB-TOKEN-HERE
export CSV_FILE_PATH=FULL-PATH-TO-CSV-File
export SNYK_LOG_PATH=FULL-PATH-TO-ROOT-DIRECTORY
git clone https://github.com/snyk-labs/import-gitlab-repo-from-csv.git
pip install -r requirements.txt
python3 index.py SNYK_GROUP_ID
```

## Example run command

python3 index.py 12345678-1234-1234-1234-123456789012
