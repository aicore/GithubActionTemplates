import os
import sys
import json
import subprocess
from github import Github
# we use pygithub https://pygithub.readthedocs.io/en/latest/index.html
# alternatively use github3py https://github3py.readthedocs.io/

print("current working directory is: ", os.getcwd())

github_info_file = open('./.tmp/github.json', 'r') 
github_details = json.load(github_info_file)

commit_info_file = open('./.tmp/commitDetails.json', 'r') 
commit_details = json.load(commit_info_file)

if github_details["event_name"] != "pull_request" or github_details["event_name"] != "pull_request_target":
    print("Error! This operation is valid on github pull requests. Exiting")
    sys.exit(1)

print("Pull request submitted by github login: ", github_details['event']['pull_request']['user']['login'])
print("Number of commits in the pull request: ", len(commit_details))

# Check if current dir is git dir
is_git_dir = subprocess.check_output(
        ['/usr/bin/git', 'rev-parse', '--is-inside-work-tree']).decode('utf-8')
print("Is git dir: ", is_git_dir)

# git status
git_status = subprocess.check_output(
        ['/usr/bin/git', 'status']).decode('utf-8')
print("Git status: ", git_status)

# last n commits
last_n_commit_list = subprocess.check_output(
        ['/usr/bin/git', 'rev-list', '--max-count=10', 'HEAD']).decode('utf-8')
print("last 10 commit ids are: ", last_n_commit_list)

# github logins of all committers
commit_logins = []
commit_id_list = []
files_updated = []
for commit in commit_details:
    commiter_github_login = commit['committer']['login']
    if commiter_github_login not in commit_logins:
        commit_logins.append(commiter_github_login)
    
    commit_id = commit['sha']
    commit_id_list.append(commit_id)
    try:
        files = subprocess.check_output(
        ['/usr/bin/git', 'diff-tree', '--no-commit-id', '--name-only', '-r', commit_id]).decode('utf-8').splitlines()
        for file in files:
            if file not in files_updated:
                files_updated.append(file)
    except subprocess.CalledProcessError as e:
        print("Exception on process, rc=", e.returncode, "output=", e.output)
        sys.exit(1)

print("All github users who made changes to the pull request: ", commit_logins)
print("All commit ids in pull request: ", commit_id_list)
print("All files updated in pull request: ", files_updated)


github_token = github_details['token']
github_repo = github_details['repository']
pr_number = github_details['event']['number']

print("Connecting to Github apis for repo: ", github_repo)
print("Pull Request number: ", pr_number)

g = Github(github_token)
repo = g.get_repo(github_repo)
pr = repo.get_pull(pr_number)

issue = repo.get_issue(pr_number)
comments = issue.get_comments()
COMMENT_STR = 'Hello from github actions.'
already_commented = False
for comment in comments:
    if comment.user.login == 'github-actions[bot]' and comment.body == COMMENT_STR:
        already_commented = True
        break

if not already_commented:
  pr.create_issue_comment('Hello from github actions.')
