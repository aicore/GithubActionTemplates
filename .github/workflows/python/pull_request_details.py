import os
import sys
import json
from github import Github
# We use https://github.com/PyGithub/PyGithub for github api interfacing

print("current working directory is: ", os.getcwd())

github_info_file = open('./.tmp/github.json', 'r') 
github_details = json.load(github_info_file)

if github_details["event_name"] != "pull_request":
    print("Error! This operation is valid on github pull requests. Exiting")
    sys.exit(1)

print("Pull request submitted by github login: ", github_details['event']['pull_request']['user']['login'])