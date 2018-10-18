import requests
import json
import getpass
import os
#import util
#from autoissue import injectNumber
#from urlparse import urljoin


API_URL = 'https://api.github.com'
SETTINGS = 'settings.williames' #settings file
HEADERS = {'Content-type':'application/json'}
TOKEN_KEY = 'auth_token'
USER_NAME = ''

REPO_NAME = "hacktoberfest-free-tshirt"
BRANCH_NAME = "nice-pants"

def getToken():
    val = reviveToken(TOKEN_KEY)
    if val is not None:
        return val

    #generate a token
    username = input('Github username: ')
    USER_NAME = username
    password = getpass.getpass('Github password: ')

    url = API_URL+'/authorizations'
    payload = {'note' : 'auto-hacktoberfest-tshirt', 'scopes' : ['repo']}
    r = requests.post(url, auth = (username, password), data = json.dumps(payload),)

    if r.status_code is requests.codes['created']:
        token = json.loads(r.text or r.content)['token']
        if not storeToken(TOKEN_KEY, token):
            print("Could not write authorization token to settings file. Please add the following line to " + SETTINGS + ":\n" + "auth_token " + token)
        return token
    else:
        print("Failed to generate a new authorization token")
        print (r.text)
        return None

def reviveToken(key):
    if os.path.exists(SETTINGS):
        with open(SETTINGS) as f:
            for line in f:
                if key in line:
                    return line.split(" ", 1)[1].strip(" \n")
    return None

def storeToken(key, value):
    with open(SETTINGS, "a+") as sett: # Will create the file if it does not exist
        sett.write(key + " " + value + "\n")
        return True

    return False

def starMaker(owner,repo):
    url = API_URL + '/user/starred/' + owner + '/' + repo
    url = url + "?access_token=" +getToken()
    try:
        r = requests.put(url)
    except:
        pass

def createNewRepo(name):
    url = API_URL + '/user/repos'
    url = url + "?access_token=" +getToken()
    data = {"name":name}
    try:
        r = requests.post(url,data = json.dumps(data),headers = HEADERS)
    except:
        print("Can't create repo")

def getRepo():
    url = API_URL + '/user/repos'
    url = url + "?access_token=" + getToken()
    try:
        r = requests.get(url)
        response = json.loads(r.content.decode("utf8"))
        for i in response:
            print(i["name"])
    except:
        print("Can't get repo lists")

def getHashFromBranch(BranchName,author,repo):
    url = API_URL + '/repos/%s/%s/branches/%s' % (author,repo,BranchName)
    url = url + "?access_token=" +getToken()
    try:
        r = requests.get(url)
        response = json.loads(r.content.decode('utf-8'))
        return response["commit"]["sha"]
    except:
        print("Cannot access hask from previous branch")


def createBranch(NewBranchName,BranchFrom,author,repo):
    url = API_URL + '/repos/%s/%s/git/refs' % (author,repo)
    HashToBranchFrom = getHashFromBranch(BranchFrom,author,repo)
    data = {
                "ref":'refs/heads/'+NewBranchName,
                "sha":HashToBranchFrom
            }
    url = url + "?access_token=" +getToken()
    #try:
    r = requests.post(url,data = json.dumps(data),headers = HEADERS)
    print(r)
    print(r.content)
    #except:
    #    pass

if __name__ == "__main__":
    print(getToken())
    #starMaker('pk1210','SuperMario')
    #getRepo()
    createBranch("Branch23","master","libe-pachilly","Test-repo")
    #getHashFromBranch("master","libe-pachilly","Test-repo")
