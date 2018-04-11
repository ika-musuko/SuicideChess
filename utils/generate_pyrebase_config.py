# this file generates a pyrebase config from a project name and an API key

from sys import argv
if __name__ == "__main__":
    if len(argv) < 3:
        print('''
            generates a firebase config for use with the library "pyrebase"
        
            usage: <firebase_project_name> <firebase_api_key>
            
            get your API key from https://console.cloud.google.com/apis/credentials?project=<firebase_project_name> if you don't already have one
        ''')
        raise SystemExit
    with open("pyrebase_config.py", 'w') as f:
        f.write('config = { "apiKey": "%s", "authDomain" : "%s.firebaseapp.com", "databaseURL" : "https://%s.firebaseio.com", "storageBucket" : "%s.appspot.com" ,"messagingSenderId" : "441451539007" }\n' % (argv[2], argv[1], argv[1], argv[1]))

