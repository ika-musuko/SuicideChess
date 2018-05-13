# Suicide Chess

Team Members:
- Joleena Marshall
- Junia Ikeh
- Sherwyn Sen
- Eric Scaramuzzo

## Instructions
**Note:** These instructions only work for Linux or Mac (or anything that can interpret .sh files). Good luck if you have Micro$oft Window$!

### Dependencies
- Python 3.6
- node.js v8

Make sure you can run `node` and `npm` from the terminal.

### Setting up your Environment

1. Create a Python Virtual Environment somewhere. We will refer to the path as `$VIRTUAL_ENV_PATH`  
`python3.6 -m virtualenv $VIRTUAL_ENV_PATH`
    - Note: If this command does not work, try running `python3.6 -m pip install virtualenv` first.
2. Install the requirements

### Running

`./run_server.sh`  

make sure you have a file called setenv.sh with all the specified environment variables in project/\_\_init\_\_.py  

### testing
`./run_tests.sh`  

write all flask tests in tests.py  

### reading the code
start reading from backend.py and follow the imports

## Goals
### Expected - Version 1.0
- [X] Create an account for the site
- [X] ~~Verify themselves via email~~ *implemented Google Login instead as the sole form of authentication*
- [X] Login to and logout from the site
- [ ] Play the Classic variant of Suicide Chess with a random person
    - [X] Backend
    - [ ] Game Integration
    - [ ] HTML/CSS
    - [ ] Templating
- [ ] Play the Classic variant of Suicide Chess with a friend via links
    - [X] Backend
    - [ ] Game Integration
    - [ ] HTML/CSS
    - [ ] Templating

### Desired - Version 2.0
- [ ] View and edit their own Profile Settings 
    - [X] Backend
    - [ ] HTML/CSS
    - [ ] Templating
- [ ] Receive email notifications for when the opponent moves
- [ ] View other player’s profiles
    - [X] Backend
    - [ ] HTML/CSS
    - [ ] Templating
- [ ] Forfeit from a game
    - [ ] Backend
    - [ ] HTML/CSS
    - [ ] Templating

### Optional (Ambitious) - Version 3.0
- [X] Google Sign-In
- [ ] User ranking based on their game performance
    - [X] Backend
    - [ ] HTML/CSS
    - [ ] Templating
- [X] ~~Limit the opponent of a friend game to a specific user~~ *implemented invite links with access codes*
- [ ] Play Blitz games
    - [ ] Backend
    - [ ] HTML/CSS
    - [ ] Templating
- [ ] Anonymous users would be able to play and join blitz games
- [ ] Write profile bios
    - [X] Backend
    - [ ] HTML/CSS
    - [ ] Templating
- [ ] Receive browser notifications upon opponent move
