# this file generates a pyrebase config from a project name and an API key

from sys import argv
if __name__ == "__main__":
    if len(argv) < 3:
        print("usage: <project_name> <api_key>")
        raise SystemExit
    with open("pyrebase_config.py", 'w') as f:
        f.write('config = { "apiKey": "%s", "authDomain" : "%s.firebaseapp.com", "databaseURL" : "https://%s.firebaseio.com", "storageBucket" : "%s.appspot.com" ,"messagingSenderId" : "441451539007" }\n' % (argv[2], argv[1], argv[1], argv[1]))

