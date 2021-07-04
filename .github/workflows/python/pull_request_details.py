import os

print("current working directory is: ", os.getcwd())

with open('./.tmp/github.json', 'r') as f:
    print(f.read())