# Suicide Chess
http://suicidechess.org/

## About
Multiplayer Suicide Chess game web application.  
The goal of Suicide Chess is to lose all of your pieces (rather than capture the opponent's king)  
This website lets you play the game with friends or with anyone around the world!

## Team
CMPE 133 Project Spring 2018  
Team Members:
- Sherwyn Sen - Website Engine
- Eric Scaramuzzo  - Suicide Chess Game App
- Junia Ikeh - Website Design
- Joleena Marshall - Templating

## Goals
### Expected - Version 1.0
- [X] Create an account for the site
- [X] ~~Verify themselves via email~~ *implemented Google Login instead as the sole form of authentication*
- [X] Login to and logout from the site
- [ ] Play the Classic variant of Suicide Chess with a random person
    - [X] Backend
    - [X] Game Integration
    - [ ] HTML/CSS
    - [ ] Templating
- [ ] Play the Classic variant of Suicide Chess with a friend via links
    - [X] Backend
    - [X] Game Integration
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

## Build Instructions
**Note:** These instructions only work for Linux or Mac (or anything that can interpret .sh files). Good luck if you have Micro$oft Window$!

### Dependencies
- Python 3.6
- node.js v8

Make sure you can run `node` and `npm` from the terminal.

### Setting up your Environment

1. Create a Python Virtual Environment somewhere. We will refer to the path as `$VIRTUAL_ENV_PATH`. (Please do not make this path inside the same directory as the project).   
`python3.6 -m virtualenv $VIRTUAL_ENV_PATH`
    - Note: If this command does not work, try running `python3.6 -m pip install virtualenv` first.
2. Go into the virtual environment.  
`source $VIRTUAL_ENV_PATH/bin/activate`
    - You should see `($VIRTUAL_ENV_PATH)` before your terminal output now.
3. Install the requirements
    - `pip install -r requirements.txt`

### Building the React App
1. Run `./build_react.sh`

### Running
Make sure you have a file called setenv.sh with all the specified environment variables in `project/__init__.py`  
1. Make sure you are in the virtual environment
    - You should see `($VIRTUAL_ENV_PATH)` before your terminal output.
2. `./run_server.sh` to start the server, and go to the URL the terminal output gives you.
    - Make sure this script is in executable mode.
3. If you want to build the React App and run, use `./build_and_run.sh`


### Testing
1. Make sure you are in the virtual environment
    - You should see `($VIRTUAL_ENV_PATH)` before your terminal output.
2. `./run_tests.sh`  


write all flask tests in tests.py  


### Leaving the virtual environment

`deactivate`

### Folders
- `config` - Flask configuration and Firebase Database rules
- `draft_html` - Rendered HTML documents of which pages are needed
- `project` - Entry for the Flask project (Website Engine)
- `suicide_chess_react` - Entry for the React project (Suicide Chess Game App)
- `uidraft` - screenshot drafts of the UI
