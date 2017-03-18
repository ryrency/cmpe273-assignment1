'''APP.PY - Read configuration details from  yaml file available in github and 
and display the details on http://<ip>/v1/<filename> in browser'''
import json
import sys
from flask import Flask
from github import Github
import yaml

giturl = sys.argv[1]

app = Flask(__name__)

@app.route("/v1/<file_name>")
def get_message(file_name):
    '''Function to return the message to FLASK
       Input Argument -
            file_name - File given as input from URL'''
    # Split File Name and Extension that is recieved in URI
    file_name_dets = file_name.split('.')

    # Get File contents by accessing the GIT HUB
    file_content = get_file_content(file_name_dets[0])

    # Get the greeting configurations
    greet_config = get_config_details(file_name_dets[1], file_content)
    return greet_config


def get_file_content(file_name):
    '''Function to get data from the input file from Github.com
       Imput Argument -
       file_name - File given as input from URL'''
    git = Github()
    url_words = giturl.split('/')
    user_name = url_words[3]
    repo_name = url_words[4]
    # Change file extension to yml even if the user has entered for json format.
    yml_file_name = file_name+".yml"

    # Get the repository from Github
    repo = git.get_user(user_name).get_repo(repo_name)

    # Get file contents from GITHUB
    file_contents = repo.get_file_contents('/%s' %yml_file_name)
    return file_contents.decoded_content
    
def get_config_details(file_ext,file_content):
    '''
       Function to get configuration details by loading the yaml file 
       and return the message in YML / JSON format as requested by the 
       user in the URL.
       Input Argument - 
       file_ext - File Extension shows the format in which user expects output
       file_content - the greeting to be passed 
    '''
    if file_ext == 'yml':
        greet_configuration = yaml.load(file_content)
        greeting_str = str(greet_configuration)
        greeting_list_1 = greeting_str.split('{')
        greeting_list_2 = greeting_list_1[1].split('}')
        greeting = greeting_list_2[0]
    else:
        greeting = json.dumps(yaml.load(file_content), sort_keys=False, indent=3)

    return greeting

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')




    