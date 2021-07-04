import os
import sys
import json
from github import Github
# We use https://github.com/PyGithub/PyGithub for github api interfacing

print("current working directory is: ", os.getcwd())

github_info_file = open('./.tmp/github.json', 'r') 
github_details = json.load(github_info_file)

commit_info_file = open('./.tmp/commitDetails.json', 'r') 
commit_details = json.load(commit_info_file)

if github_details["event_name"] != "pull_request":
    print("Error! This operation is valid on github pull requests. Exiting")
    sys.exit(1)

print("Pull request submitted by github login: ", github_details['event']['pull_request']['user']['login'])
print("Number of commits in the pull request: ", len(commit_details))

# github logins of all committers
commit_logins = []
commit_id_list = []
for commit in commit_details:
    commiter_github_login = commit['committer']['login']
    commit_id_list.append(commit['sha'])
    if commiter_github_login not in commit_logins:
        commit_logins.append(commiter_github_login)

print("All github users who made changes to the pull request: ", commit_logins)
print("All commit ids in pull request: ", commit_id_list)

