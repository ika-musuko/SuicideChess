# Suicide Chess

## Instructions
### Running
Install all of the requirements using pip and the included requirements.txt (preferably to a virtualenv)  

**linux/mac**: use `./run_server.sh`  
**windows**: lol  

make sure you have a file called setenv.sh with all the specified environment variables in project/\_\_init\_\_.py  

### testing
**linux/mac**: use `./run_tests.sh`  
**windows**: lmao  

write all tests in tests.py  

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
